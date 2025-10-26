"""Batch OCR command line interface for DeepSeek-OCR."""

from __future__ import annotations

import argparse
import concurrent.futures
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

import mlx.core as mx
from huggingface_hub import snapshot_download
from PIL import Image
from transformers import AutoTokenizer
from transformers.tokenization_utils_base import PreTrainedTokenizerBase

from deepseek_ocr_mlx import (
    DeepSeekOCRPreprocessor,
    GenerationConfig,
    generate,
    save_ocr_outputs,
)
from deepseek_ocr_mlx.load import load as load_model, load_config

SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
DEFAULT_PROMPT = "<image>\n<|grounding|>Convert the document to markdown."
DEFAULT_MODEL_ID = "deepseek-ai/DeepSeek-OCR"


@dataclass
class Task:
    source: Path
    destination: Path


@dataclass
class WorkerState:
    tokenizer: PreTrainedTokenizerBase
    preprocessor: DeepSeekOCRPreprocessor
    model: object
    gen_config: GenerationConfig
    prompt: str


_WORKER_STATE: Optional[WorkerState] = None


def _discover_images(root: Path, suffixes: Iterable[str]) -> List[Task]:
    root = root.resolve()
    tasks: List[Task] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in suffixes:
            continue
        relative = path.relative_to(root)
        destination = relative.with_suffix("")
        tasks.append(Task(source=path, destination=destination))
    return tasks


def _init_worker(
    model_id: str,
    prompt: str,
    max_new_tokens: int,
    temperature: float,
    stop_on_eos: bool,
) -> None:
    global _WORKER_STATE

    model_dir = Path(snapshot_download(model_id))
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    config = load_config(model_dir)
    preprocessor = DeepSeekOCRPreprocessor(tokenizer, config)
    model = load_model(model_dir, lazy=False)
    mx.eval(model.parameters())

    eos_ids_attr = getattr(tokenizer, "eos_token_ids", None)
    if isinstance(eos_ids_attr, int):
        stop_ids = [eos_ids_attr]
    elif eos_ids_attr:
        stop_ids = list(eos_ids_attr)
    else:
        stop_ids = []

    if stop_on_eos and not stop_ids and tokenizer.eos_token_id is not None:
        stop_ids = [tokenizer.eos_token_id]

    gen_config = GenerationConfig(
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        eos_token_id=tokenizer.eos_token_id if stop_on_eos else None,
        stop_token_ids=stop_ids if stop_on_eos else None,
        skip_special_tokens=False,
    )

    _WORKER_STATE = WorkerState(
        tokenizer=tokenizer,
        preprocessor=preprocessor,
        model=model,
        gen_config=gen_config,
        prompt=prompt,
    )


def _process_task(task: Task, output_root: Path) -> tuple[Path, bool, str]:
    if _WORKER_STATE is None:
        return task.source, False, "Worker state not initialised"

    state = _WORKER_STATE
    try:
        with Image.open(task.source) as img:
            image = img.convert("RGB")

        batch = state.preprocessor.prepare_single(state.prompt, [image])
        result = generate(state.model, state.tokenizer, batch, state.gen_config)

        destination_dir = output_root / task.destination
        markdown = save_ocr_outputs(image, result.text, destination_dir)
        return task.source, True, markdown
    except Exception as exc:  # pragma: no cover - defensive path
        return task.source, False, str(exc)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DeepSeek-OCR batch CLI")
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing images to OCR.",
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        help="Directory where results will be written.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL_ID,
        help="Hugging Face model identifier (default: %(default)s).",
    )
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Prompt to prepend before each image (default: %(default)s).",
    )
    parser.add_argument(
        "--extensions",
        nargs="*",
        default=sorted(SUPPORTED_SUFFIXES),
        help="File extensions to include (default: common image types).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=min(os.cpu_count() or 1, 2),
        help="Number of parallel workers (default: %(default)s).",
    )
    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=1024,
        help="Maximum tokens to generate per image (default: %(default)s).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature (default: %(default)s).",
    )
    parser.add_argument(
        "--no-stop",
        action="store_true",
        help="Do not stop on EOS tokens.",
    )
    parser.add_argument(
        "--combine",
        action="store_true",
        help="After processing, write a combined.md aggregating all results (rewriting image paths).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    input_dir = args.input_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    if not input_dir.exists() or not input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")

    extensions = {
        ext.lower() if ext.startswith(".") else f".{ext.lower()}"
        for ext in args.extensions
    }
    tasks = _discover_images(input_dir, extensions)
    if not tasks:
        print("No matching images found.")
        return

    print(f"Found {len(tasks)} images. Using {args.workers} worker(s).")

    output_dir.mkdir(parents=True, exist_ok=True)

    with concurrent.futures.ProcessPoolExecutor(
        max_workers=args.workers,
        initializer=_init_worker,
        initargs=(
            args.model,
            args.prompt,
            args.max_new_tokens,
            args.temperature,
            not args.no_stop,
        ),
    ) as executor:
        futures = {
            executor.submit(_process_task, task, output_dir): task for task in tasks
        }

        failures: List[tuple[Path, str]] = []
        successes: List[tuple[Task, str]] = []
        for future in concurrent.futures.as_completed(futures):
            task = futures[future]
            try:
                _, success, message = future.result()
            except Exception as exc:  # pragma: no cover
                failures.append((task.source, str(exc)))
                print(f"[FAIL] {task.source}: {exc}")
                continue

            if success:
                print(f"[OK]   {task.source}")
                if args.combine:
                    successes.append((task, message))
            else:
                failures.append((task.source, message))
                print(f"[FAIL] {task.source}: {message}")

    if args.combine and successes:
        def _rewrite_image_paths(md: str, base_prefix: str = "") -> str:
            import re

            # Replace variations like (images/0.jpg) or (./images/0.jpg)
            pattern = re.compile(r"\]\((?:\./)?images/([^)]+)\)")
            return pattern.sub(lambda m: f"]({base_prefix}images/{m.group(1)})", md)

        parts: List[str] = ["# Batch OCR"]
        # Sort by input path for determinism
        for task, md in sorted(successes, key=lambda x: str(x[0].source)):
            subdir = task.destination.as_posix()
            md_rewritten = _rewrite_image_paths(md, base_prefix=f"{subdir}/")
            parts.append(f"\n\n## {task.source.name}\n\n{md_rewritten.strip()}\n")
        combined = "\n---\n".join(parts).strip() + "\n"
        (output_dir / "combined.md").write_text(combined, encoding="utf-8")

    if failures:
        print("\nCompleted with errors:")
        for path, reason in failures:
            print(f" - {path}: {reason}")
    else:
        print("\nAll tasks completed successfully.")


if __name__ == "__main__":
    main()

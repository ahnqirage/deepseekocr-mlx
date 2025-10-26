# DeepSeek OCR

## Install

```sh
uv sync
```

## Run

### Single image

```sh
python run_demo.py
```

### Batch images

```sh
python ocr.py input_folder output_folder --workers 3
```

To also create a single combined markdown with fixed image paths:

```sh
python ocr.py input_folder output_folder --workers 3 --combine
```

### PDF

#### Single PDF

```sh
python process_pdf.py assets/ocr-guide-to-testing.pdf test_pdf --workers 3
```

#### Multiple PDFs

```sh
python process_pdf.py pdf_dir/ output_dir
```

Notes:

- For PDFs, two combined files are written automatically:
  - `output_dir/<pdf_stem>/combined.md` with links relative to the PDF folder
  - `output_dir/<pdf_stem>.md` with links that also include the PDF folder prefix

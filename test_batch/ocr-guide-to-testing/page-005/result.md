## Test scripts  


## Test scripts are specifically applicable to software testing.  


A test script is a set of instructions that are performed on the code or system, which is being tested, to replicate user actions and investigate whether it performs as expected. A simple example of a test script to save a current file that has been saved before in a word processor could be:  



<table><tr><td>Step</td><td>Action</td><td>Result</td></tr><tr><td>1</td><td>Click on the file option of the main menu bar.</td><td>A drop down menu appears, one of the options is &#x27;Save&#x27;.</td></tr><tr><td>2</td><td>Click on the &#x27;Save&#x27; option from the drop down menu.</td><td>The disk whirs and the date/time stamp of the file in explorer matches the time that the file was saved.</td></tr></table>  


There are two methods of executing test scripts:  


1. Manual testing, within which test scripts are more commonly known as test cases, uses a set of conditions or variables under which a tester will determine whether a software system is operating correctly or not.  


2. Automated testing which can involve:  


A small piece of code written in a programming language which is used to test an area of functionality of a software system, Short, data- driven programs that contain extensive parameters. Keyword- driven or table- driven testing using reusable steps.  


The last two elements can also be used within manual testing.  


## The advantages of automated testing over manual testing using scripts  


Tests can be executed without the need for human intervention. Tests can be carried out much faster and are easily repeatable so are worth considering if a test is required to be executed several times.  


## The disadvantages of automated testing over manual testing using scripts  


Tests can be carried out much faster and are easily repeatable so are worth considering if a test is required to be executed several times.The disadvantages of automated testing over manual testing using scripts- Tests scripts can be poorly written and breakdown during use.- Ideally, it is helpful if a human tests the system at some point, as a trained manual tester can observe if the system being tested is misbehaving without being prompted or directed, whereas automated tests can only examine what they have been programmed to look at.- Manual testers can discover new bugs while ensuring that old bugs do not reappear, while an automated test can only ensure the latter.  


The ideal situation is to employ both manual and automatic types of testing with both using test scripts. This offers the best results by automating tests that are needed to be done frequently and that can be easily checked by a machine; and using manual testing to run new test scripts initially which can then be added to the automated test suite.

# cpp_stresst

This is a package to help stress test your C++ solutions to problems.

You should have your directory structured like this:

- C++ solution
- Test Folder
	- 1.in
	- 1.out

All test cases should have a file with the same name ending with `.in` and a file ending with `.out` for input and output, respectively.

To test your solution on `stdin`/`stdout`, run this command.

`c_stresst [SOLUTION FILE] [TEST FOLDER]`

If you ever forget this command, simply type this into your terminal:
`c_stresst --help`

Only supported on linux systems (tested on Ubuntu), uses g++ to compile.
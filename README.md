cctime
======

A simple tool for measuring compilation time.

This tool was originally created to measure compiler performance of clang.

single file example
===================

Suppose you have a cpp file called foo.cpp which you compile with g++ using:

	$ g++ -c foo.cpp

To take 5 samples and output the results to foo.csv use:

	$ cctime.py -n 5 foo.csv g++ -c foo.cpp
	$ cat foo.csv

If you want to compare gcc 4.6 to gcc 4.7 try:

	$ cctime.py -n 5 --ref=g++-4.6 foo.csv g++-4.7 -c foo.cpp
	$ cat foo.csv


cmake example
=============

Here's an example that shows building llvm using cmake and capturing the time to compile each cpp file:

1. Create a new build directory

		$ mkdir timed_build
		$ cd timed_build

2. Run cmake with CXX set to cctime
		
		$ cmake \
			-DCMAKE_CXX_COMPILER=path/to/cctime.py \
			-DCMAKE_CXX_COMPILER_ARG1="-n=5 /path/to/output.csv /path/to/clang++" \
			/path/to/llvm_src
		# clear the csv file which will now include results from cmake test compiles
		$ rm /path/to/output.csv

3. Run make to generate the results
		
		$ make
		
	or you can use VERBOSE=1 to see how cctime.py is invoked:

		$ make VERBOSE=1

4. Go have a beer because it's going to take a while to compile llvm 5 times.

		$ cat /path/to/output.csv


If you want to run again just make clean and clear the existing csv file:

		$ make clean
		$ rm /path/to/output.csv
		$ make

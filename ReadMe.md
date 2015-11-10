# Description

This is the repository for the code of the 2nd Part of the project of _**Comparison of Search Algorithms**_.

This set of program implements a modified AC3 who can also handle with multi-nary constraints (not just ternary), and a Backtracking Search who supports all the variable binding and inference techniques introduced in the class.

Basically, three kinds of puzzles are implemented in this set of program, which include CrossMath, Futoshiki and Sudoku as the additional work. The author says ‘basically’ here, because all these puzzles generated by the program are only guaranteed to have solutions but not just have one solution, which usually is a strict requirement for the standard puzzles.

# Author
Pei Xu, 5186611, xuxx0884 at umn.edu

# License
MIT

# Files
The complete code contains 8 file beside the readme file:

  1. _**PC.py**_ is the library file of a **modified AC3**.
  
  This file provides a modified AC class who has a path consistency function using the modified PC1, the function who can handle binary, ternary and more than ternary constraints. So the author calls it PC not AC.
  
  The PC class is originated by the author.

  A unit test about the class PC() will run automatically if you run this file.
    
  2. _**BT.py**_ is the library file of **Backtracking Search**.
  
  It has a class BT() that realizes Backtracking Search supporting random, MRV, degree heuristic or MRV+degree as variable binding technique, and MAC or Forward-Checking as inference technique, and supports using PC or not for preprocess.
  
  MAC and degree heuristic here could consider the situation where multi-nary constraints exist.
  
  We know, the difference in the order of the function arc_reduce or revise handling constraints could lead to a difference in the results; and in AC3 or the like, the mentioned function should be called several times in order to obtain the final result. In my program, the class BT() could try to optimize  the order of constraints handled via PC() class before beginning search in order to improve efficiency.
  
  Originated!
    
  3. _**CrossMath.py**_ is the implement for **CrossMath** puzzles.

  This file provides four functions who can randomly generate a solve puzzle in the format of string and according to the given size, who can sparse the string and return a dictionary containing all related binary or multi-nary constraints, who can print a puzzle board into the command window or terminal, and who can solve a puzzle in the given string format via BT() class mentioned above.

  Due to the support of PC() class, the solver of this puzzle in the file can solve the CrossMath whose size is more than 3x3.
  
  Originated!
    
  4. _**Futoshiki.py**_ is the implement for **Futoshiki** puzzles.

  Basically, this file is similar to the above one but is to deal with the Futoshiki puzzle.
  
  Originated!

  5. _**Sudoku.py**_ is the implement for **Sudoku** puzzles.
  
  This file’s function is like the above two but is to handle the Sudoku puzzle who is considered as the additional work for this project.
  
  Originated!

   **The above three files can be run who will randomly generate a corresponding puzzle with random size. You can solve it yourself or just press ‘enter’ key for inspecting two solutions, one of which is obtained during generating the puzzle and one of which is gotten via Backtracking Search.**

    
  6. _**test.py**_ is the **main** program basically.
  
  This file provides some brief introduction to this set of program; and can solve **all** the test puzzles provided in the class GitHub, and a randomly generated Sudoku which is considered as the additional work for my striving for an A.

  This file solves the Crypt and Kenken via manually calling the class BT() due to no implement for these two kinds of puzzle in this set of program. 
  
    
   Originated of course.
  
  7. _**algComprison.py**_ is the real **main** testing program for this project.
  
  This file will automatically do some tests via solving certain kinds of but randomly generated puzzles through Backtracking Search using different variable binding or inference technique according to the given input argument, record related performance of the search algorithms, and write it into a log file. This file is semi-finished due to incompleteness of the code whose function is to analyze the generated log file.

   Run this file for details.
   
   Originated!

  8. _**p2test 04.10.24 2015-11-09.log**_ is a testing log who recoded a 250-case test's results the author ran on the night of Nov. 8th.

# Algorithms
In this program, a class who can support node consistency, arc consistency and party consistency is implement and named as PC. For the sake of compatibility, it supports an implement for arc_reduce or revise function in AC3 for dealing with binary constraints, which also is handleable via the function for multi-nary constraints. So, basically, it handles arc consistency via AC3 if you directly set binary constraints not multi-nary constraints for the variables, and handles multi-nary in the way a little like PC1 not the same. 

In this program, 4 kinds of variable binding techniques and 2 kinds of inference employed by backtracking are implemented. They are
 
    Variable Binding Techniques: Random (really random), MRV, Degree Heuristic, and MRV+Degree
    
    Inference Techniques: MAC, and Forward Checking

And, backtracking search provided via this program supports to use the class PC to do some preprocess work before doing search. (Of course, you can turn it down.)

# Metrics:
   4 kinds of data will be recorded for analyzing the performance of backtracking using different variable binding or/and inference technique.

  1. The amount of times a search algorithm assigns a value to any variable during solving a puzzle.

  2. The amount of times a search algorithm does inference.

  3. The amount of times a search algorithm finds an unassigned variable.

  4. The running time for solving a puzzle will be record and used for comparison of these algorithms' overall time complexity.

# Usage

Environment:

    Python 3.4
  
Please run '_**python test.py**_' to see how the program solves the given test puzzles.

Attention: it may take a pretty long time to solve the Puzzle 10 or 11 of Crypt.

Run '_**python Futoshiki.py**_', '_**python CrossMath.py**_' or '_**python Sudoku.py**_' to see how this program generates a random solveable puzzle and solves it.

Or, you can run '_**python p2test.py -h**_’ to see how the program automatically does tests for this project.

# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "15:23, Nov. 7th, 2015"
""" This is the test file for solving the test puzzles provided in GitHub."""

import time
import CrossMath, Futoshiki, Sudoku
import BT

if __name__ == '__main__':
  print('Author: %s'%__author__)
  print('Copyright: %s'%__copyright__)
  print('License: %s'%__license__)
  
  print('\nThis file shows the solution for the provided test cases on GitHub.\n')
  print('All solutions shown by this file will be obtained via Backtracking Search using MRV + Degree and MAC for the sake of getting solutions as fast as possible.\n')
  print('Backtracking Search implemented by this set of program supports MRV, Degree, Random and MRV+Degree as the technique for selecting variables to bind, and MAC and Forward Checking as the technique for inference.')
  print('Backtracking Search here uses a modified AC3 which can handle with multinary constraints and maintain path consistency via PC1.')
  print('No implement for KenKen or Crypt is supported by this set of program. But Backtracking Search implemented by this set of program is able to handle these two puzzles quite well.')
  print('As additional work, the Sudoku puzzle is implemented by this set of program for the comparison of backtracking search\'s performance when preprocessed via AC3 to that when not.\n')
  print('An automatically testing program named algComparison.py is a component of this set of program. This program can automatically generate solvable puzzles, then solve these puzzles via Backtracking Search using different combinations of variable-binding or inference technique, and record some metrics into a log file for analysis and comparison of these algorithms. Run this file to see more details.\n')
  
  
  print('Test will start in 2 second.')
  time.sleep(2)
  
  print('\n======= CrossMath Test =======')
  print("The implement of Backtracking is able to handle CrossMath puzzles even with more than ternary constraints.\n")
  games = ['.++.+*.=/.<+-.>*-.^=/.+=.-=.v==15,24,14,3,12,4', '.<+*.>*+.^=+.++.--.v=*.<-=.>*=.==24,6,24,24,5,24', '.+*.+/.=+./-.++.=+.*=.-=.==17,8,25,10,7,18', './-.-+.^=-.-+.+-.v=/.<-=.>/=.==2,6,1,7,4,1', '.^--.++.=/.v-*.+-.=-./=.+=.==8,7,7,5,10,0']
  for i in range(5):
    print('Puzzle %d:' % (i+1))
    CrossMath.printGame(games[i])
    print('Solution:')
    result = CrossMath.solveByBT(games[i])
    CrossMath.printGame(CrossMath.convert2str(games[i], result['solution']))
    for r in result:
      if r != 'solution':
        print(r + ': ' + str(result[r]))
    print("++++++++++++++++++++++++++++")

  
  print('\n======= Futoshiki Test =======')
  games = ['..<....<^..1...3<...', '2..<..>......^...<.<.', '.>....^..^..^.3....v.v<3.v...2..<.', '...>..<.^5<.......<.....>^.v..<.^.^.........>...']
  for i in range(4):
    print('Puzzle %d:' % (i+1))
    Futoshiki.printGame(games[i])
    print('Solution:')
    result = Futoshiki.solveByBT(games[i])
    Futoshiki.printGame(Futoshiki.convert2str(games[i], result['solution']))
    for r in result:
      if r != 'solution':
        print(r + ': ' + str(result[r]))
    print("++++++++++++++++++++++++++++")

  print('\n======= KenKen Test =======')
  print("No implement for Kenken in this set of program.\nBut the implement of Backtracking is able to handle KenKen puzzles.\n")
  print('Puzzle 1')
  cons = ['[8,*,A1,A2,B1]','[5,+,A3,A4]','[2,/,B2,C2]','[4,*,B3,C3]','[8,+,B4,C4,D4]','[2,-,C1,D1]','[1,-,D2,D3]']
  for c in cons:
    print('  ' + c)
  
  bt = BT.BT()
  default_domain = [i for i in range(1, 5)]
  variables = [i+j for i in 'ABCD' for j in '1234']
  for v in variables:
    bt.set_domain(v, default_domain)
    
  for i in 'ABCD':
    for j in '1234':
      current_var = i + j
      for k in range(int(j)+1, 5):
        bt.set_binary_cons(current_var, i+str(k), lambda x,y: x != y)
  for i in '1234':
    for j in range(len('ABCD')):
      current_var = 'ABCD'[j] + i
      for k in range(j+1, 3):
        bt.set_binary_cons(current_var, 'ABCD'[k] + i, lambda x,y: x != y)  
  
  bt.set_multinary_cons(['A1', 'A2', 'B1'], lambda x: x['A1'] * x['A2'] * x['B1'] == 8)
  bt.set_multinary_cons(['B4', 'C4', 'D4'], lambda x: x['B4'] + x['C4'] + x['D4'] == 8)
  
  bt.set_binary_cons('A3', 'A4', lambda x,y: x+y == 5)
  bt.set_binary_cons('B2', 'C2', lambda x,y: x/y == 2 or y/x == 2)
  bt.set_binary_cons('B3', 'C3', lambda x,y: x*y == 4)
  bt.set_binary_cons('C1', 'D1', lambda x,y: abs(x-y) == 2)
  bt.set_binary_cons('D2', 'D3', lambda x,y: abs(x-y) == 1)

  result = bt.do_search()
  solution = result['solution']
  itera = 0
  output = ''
  for i in variables:
    itera = itera + 1
    output = output + i + ': ' + str(solution[i])
    if itera % 4 == 0:
      print(output)
      output = ''
    else:
      output = output + ', '
  for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")
  

  print('Puzzle 2')
  cons = ['[7,+,A1,A2,B2]','[1,-,A3,B3]','[4,*,A4,B4]','[4,*,B1,C1]','[4,+,C2,C3,D3]','[1,-,C4,D4]','[1,-,D1,D2]']
  for c in cons:
    print('  ' + c)
  
  bt = BT.BT()
  default_domain = [i for i in range(1, 5)]
  variables = [i+j for i in 'ABCD' for j in '1234']
  for v in variables:
    bt.set_domain(v, default_domain)
    
  for i in 'ABCD':
    for j in '1234':
      current_var = i + j
      for k in range(int(j)+1, 5):
        bt.set_binary_cons(current_var, i+str(k), lambda x,y: x != y)
  for i in '1234':
    for j in range(len('ABCD')):
      current_var = 'ABCD'[j] + i
      for k in range(j+1, 3):
        bt.set_binary_cons(current_var, 'ABCD'[k] + i, lambda x,y: x != y)  
  
  bt.set_multinary_cons(['A1', 'A2', 'B2'], lambda x: x['A1'] + x['A2'] + x['B2'] == 7) 
  bt.set_multinary_cons(['C2', 'C3', 'D3'], lambda x: x['C2'] + x['C3'] + x['D3'] == 4)
  
  bt.set_binary_cons('A3', 'B3', lambda x,y: abs(x-y) == 1)
  bt.set_binary_cons('A4', 'B4', lambda x,y: x*y == 4)
  bt.set_binary_cons('B1', 'C1', lambda x,y: x*y == 4)
  bt.set_binary_cons('C4', 'D4', lambda x,y: abs(x-y) == 1)
  bt.set_binary_cons('D1', 'D2', lambda x,y: abs(x-y) == 1)
  
  result = bt.do_search()
  solution = result['solution']
  itera = 0
  output = ''
  for i in variables:
    itera = itera + 1
    output = output + i + ': ' + str(solution[i])
    if itera % 4 == 0:
      print(output)
      output = ''
    else:
      output = output + ', '
  for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")
  
  
  print('Puzzle 3')
  cons = ['[1,-,A1,A2]','[1,-,A3,A4]','[5,-,A5,A6]','[2,-,A7,B7]','[10,+,B1,C1,D1]','[4,*,B2,B3]','[42,*,B4,C4]','[3,/,B5,C5]','[10,+,B6,C6]','[2,/,C2,C3]','[5,+,C7,D7]','[12,+,D2,E2,E3]','[3,/,D3,D4]','[10,+,D5,E5]','[20,*,D6,E6]','[7,*,E1,F1]','[8,*,E4,F4]','[2,/,E7,F7]','[1,-,F2,F3]','[10,*,F5,F6]','[16,+,G1,G2,G3]','[1,-,G4,G5]','[2,/,G6,G7]']
  for c in cons:
    print('  ' + c)
  
  bt = BT.BT()
  default_domain = [i for i in range(1, 8)]
  variables = [i+j for i in 'ABCDEFG' for j in '1234567']
  for v in variables:
    bt.set_domain(v, default_domain)
    
  for i in 'ABCDEFG':
    for j in '1234567':
      current_var = i + j
      for k in range(int(j)+1, 8):
        bt.set_binary_cons(current_var, i+str(k), lambda x,y: x != y)
  for i in '1234567':
    for j in range(len('ABCDEFG')):
      current_var = 'ABCDEFG'[j] + i
      for k in range(j+1, 7):
        bt.set_binary_cons(current_var, 'ABCDEFG'[k] + i, lambda x,y: x != y)  
  
  bt.set_multinary_cons(['B1', 'C1', 'D1'], lambda x: x['B1'] + x['C1'] + x['D1'] == 10)
  bt.set_multinary_cons(['D2', 'E2', 'E3'], lambda x: x['D2'] + x['E2'] + x['E3'] == 12)
  bt.set_multinary_cons(['G1', 'G2', 'G3'], lambda x: x['G1'] + x['G2'] + x['G3'] == 16)
  
  bt.set_binary_cons('A1', 'A2', lambda x,y: abs(x-y) == 1)
  bt.set_binary_cons('A3', 'A4', lambda x,y: abs(x-y) == 1)
  bt.set_binary_cons('A5', 'A6', lambda x,y: abs(x-y) == 5)
  bt.set_binary_cons('A7', 'B7', lambda x,y: abs(x-y) == 2)
  bt.set_binary_cons('B2', 'B3', lambda x,y: x * y == 4)
  bt.set_binary_cons('B4', 'C4', lambda x,y: x * y == 42)
  bt.set_binary_cons('B5', 'C5', lambda x,y: x / y == 3 or y / x == 3)
  bt.set_binary_cons('B6', 'C6', lambda x,y: x + y == 10)
  bt.set_binary_cons('C2', 'C3', lambda x,y: x / y == 2 or y / x == 2)
  bt.set_binary_cons('C7', 'D7', lambda x,y: x + y == 5)
  bt.set_binary_cons('D3', 'D4', lambda x,y: x / y == 3 or y / x == 3)
  bt.set_binary_cons('D5', 'E5', lambda x,y: x + y == 10)
  bt.set_binary_cons('D6', 'E6', lambda x,y: x * y == 20)
  bt.set_binary_cons('E1', 'F1', lambda x,y: x * y == 7)
  bt.set_binary_cons('E4', 'F4', lambda x,y: x * y == 8)
  bt.set_binary_cons('E7', 'F7', lambda x,y: x / y == 2 or y / x == 2)
  bt.set_binary_cons('F2', 'F3', lambda x,y: abs(x-y) == 1)
  bt.set_binary_cons('F5', 'F6', lambda x,y: x * y == 10)
  bt.set_binary_cons('G4', 'G5', lambda x,y: abs(x-y) == 1)
  bt.set_binary_cons('G6', 'G7', lambda x,y: x / y == 2 or y / x == 2)
  
  result = bt.do_search()
  solution = result['solution']
  itera = 0
  output = ''
  for i in variables:
    itera = itera + 1
    output = output + i + ': ' + str(solution[i])
    if itera % 7 == 0:
      print(output)
      output = ''
    else:
      output = output + ', '
  for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")


  print('\n======= All tests have passed =======')
  
  print('All solutions shown by this file were obtained via Backtracking Search using MRV + Degree and MAC for the sake of getting solutions as fast as possible.\n')
  print('Backtracking Search implemented by this set of program supports MRV, Degree, Random and MRV+Degree as the technique for selecting variables to bind, and MAC and Forward Checking as the technique for inference.')
  print('Backtracking Search here uses a modified AC3 which can handle with multinary constraints and maintain path consistency via PC1. It works well for more than ternary constraints. Run CrossMath.py and see how the search solves 4x4 CrossMath')
  print('No implement for KenKen or Crypt is supported by this set of program. But Backtracking Search implemented by this set of program is able to handle these two puzzles quite well.')
  print('As additional work, the Sudoku puzzle is implemented by this set of program for the comparison of backtracking search\'s performance when preprocessed via AC3 to that when not.\n')
  print('An automatically testing program named algComparison.py is a component of this set of program. This program can automatically generate solvable puzzles, then solve these puzzles via Backtracking Search using different combinations of variable-binding or inference technique, and record some metrics into a log file for analysis and comparison of these algorithms. Run this file to see more details.\n')
  
  # Important things need to say three times !!!
  print('As additional work, the Sudoku puzzle is implement in Sudoku.py.')
  print('As additional work, the Sudoku puzzle is implement in Sudoku.py.')
  print('As additional work, the Sudoku puzzle is implement in Sudoku.py.')
  
  print('\nHere is a random 9x9 example.')
  game, board = Sudoku.generateGame(9)
  Sudoku.printGame(game)
  print('Solution')
  Sudoku.printGame(Sudoku.convert2str(game, Sudoku.solveByBT(game)['solution']))
  print('\nIf you would like, you can run CrossMath.py, Futoshiki.py or Sudoku.py for playing these puzzles. Have a good day!')
  

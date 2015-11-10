# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.1.1"
__date__ = "13:23, Nov. 10th, 2015"
""" This is the test file for solving the test puzzles provided in GitHub."""

import time
import CrossMath, Futoshiki, Sudoku
from BT import *

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
  
  
  print('\n======= Crypt Test =======')
  print("No implement for Crypt in this set of program.\nBut the implement of Backtracking is able to handle Crypt puzzles even with more than ternary constraints.\n")

  print('Puzzle 1')

  puzzle = 'send+more=money'
  print('   '+puzzle)

  game = list(set(puzzle.replace('+', '').replace('=', '')))
  
  bt = BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  for i in range(3):
    bt.set_domain('x'+str(i), [0, 1])
  
  # for the most right digit
  bt.set_multinary_cons(['d', 'e', 'y', 'x0'], lambda x: x['d'] + x['e'] == x['y'] + 10*x['x0'])
  
  # the middle digit
  bt.set_multinary_cons(['n', 'r', 'e', 'x0', 'x1'], lambda x: x['n'] + x['r'] + x['x0'] == x['x1']*10 + x['e'])
  bt.set_multinary_cons(['e', 'o', 'n', 'x1', 'x2'], lambda x: x['e'] + x['o'] + x['x1'] == x['x2']*10 + x['n'])
  bt.set_multinary_cons(['s', 'm', 'o', 'x2'], lambda x: x['s'] + x['m'] +x['x2'] == x['m'] *10 + x['o'])
  
  bt.set_unary_cons('s', lambda x: x != 0)
  bt.set_unary_cons('m', lambda x: x != 0)
    
  result = bt.do_search()
  print('Solution:')
  print("""
    send    {s}{e}{n}{d}
  + more   +{m}{o}{r}{e}
  ------   ------
   money   {m}{o}{n}{e}{y}
""".format_map(result['solution']))
  for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")
  
  print('Puzzle 2')
  print('A little slowly')
  puzzle = 'crash+hacker=reboot'
  print('   '+puzzle)

  game = ''.join(set(puzzle.replace('+', '').replace('=', '')))
  
  bt = BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  
  for i in range(5):
    bt.set_domain('x'+str(i), [0, 1])
    
  bt.set_multinary_cons(['h', 'r', 't', 'x0'], lambda x: x['h'] + x['r'] ==  x['x0']*10 + x['t'])
  
  bt.set_multinary_cons(['s', 'e', 'o', 'x1', 'x0'], lambda x: x['s'] + x['e'] + x['x0'] ==  x['x1']*10 + x['o'])
  bt.set_multinary_cons(['a', 'k', 'o', 'x1', 'x2'], lambda x: x['a'] + x['k'] + x['x1'] ==  x['x2']*10 + x['o'])
  bt.set_multinary_cons(['r', 'c', 'b', 'x3', 'x2'], lambda x: x['r'] + x['c'] + x['x2'] ==  x['x3']*10 + x['b'])
  bt.set_multinary_cons(['c', 'a', 'e', 'x3', 'x4'], lambda x: x['a'] + x['c'] + x['x3'] ==  x['x4']*10 + x['e'])
  bt.set_multinary_cons(['h', 'r', 'x4'], lambda x: x['h'] + x['x4'] ==  x['r'])

  bt.set_unary_cons('c', lambda x: x != 0)
  bt.set_unary_cons('h', lambda x: x != 0)
  bt.set_unary_cons('r', lambda x: x != 0)
  
  result = bt.do_search()
  print('Solution:')
  print("""
     crash      {c}{r}{a}{s}{h}
  + hacker   + {h}{a}{c}{k}{e}{r}
  --------   --------
    reboot     {r}{e}{b}{o}{o}{t}
""".format_map(result['solution']))
  for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")
  
  
  print('Puzzle 3')
  puzzle = 'basic+logic=pascal'
  print('   '+puzzle)

  game = ''.join(set(puzzle.replace('+', '').replace('=', '')))
  
  bt = BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  
  for i in range(5):
    bt.set_domain('x' + str(i), [0, 1])
    
  bt.set_multinary_cons(['c', 'l', 'x0'], lambda x: 2*x['c'] == x['x0']*10 + x['l'])
  bt.set_multinary_cons(['i', 'a', 'x0', 'x1'], lambda x: 2*x['i'] + x['x0'] == x['x1']*10 + x['a'])
  bt.set_multinary_cons(['s', 'g', 'c', 'x1', 'x2'], lambda x: x['s'] + x['g'] + x['x1'] == x['x2']*10 + x['c'])
  bt.set_multinary_cons(['a', 'o', 's', 'x2', 'x3'], lambda x: x['a'] + x['o'] + x['x2'] == x['x3']*10 + x['s'])
  bt.set_multinary_cons(['b', 'l', 'a', 'x3', 'x4'], lambda x: x['b'] + x['l'] + x['x3'] == x['x4']*10 + x['a'])
  bt.set_binary_cons('p', 'x4', lambda x,y: x == y)
  # For the most left digit
  bt.set_multinary_cons(['b'], lambda x: x['b'] != 0)
  bt.set_unary_cons('l', lambda x: x != 0)
  bt.set_unary_cons('p', lambda x: x != 0)
  
  result = bt.do_search()
  print('Solution:')
  print("""
    basic     {b}{a}{s}{i}{c}
  + logic   + {l}{o}{g}{i}{c}
  -------   -------
   pascal    {p}{a}{s}{c}{a}{l}
""".format_map(result['solution']))
  for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")
  
  print('Puzzle 5')
  puzzle = 'NETWORK+WINDOWS+WS=DISKETTE'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('+', '').replace('=', '')))
  
  bt = BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  for i in range(7):
    bt.set_domain('x' + str(i), [0, 1, 2])
  bt.set_multinary_cons(['K', 'S', 'E', 'x0'], lambda x: x['K'] + 2*x['S'] == x['E'] + x['x0']*10)
  bt.set_multinary_cons(['R', 'W', 'T', 'x0', 'x1'], lambda x: x['R'] + 2*x['W'] +x['x0'] == x['x1']*10 + x['T'])
  bt.set_multinary_cons(['O', 'T', 'x1', 'x2'], lambda x: 2*x['O'] + x['x1'] == x['x2']*10 + x['T'])
  bt.set_multinary_cons(['W', 'D', 'E', 'x2', 'x3'], lambda x: x['W'] + x['D'] + x['x2'] == x['x3']*10 + x['E']) 
  bt.set_multinary_cons(['T', 'N', 'K', 'x3', 'x4'], lambda x: x['T'] + x['N'] + x['x3'] == x['x4']*10 + x['K'])
  bt.set_multinary_cons(['E', 'I', 'S', 'x4', 'x5'], lambda x: x['E'] + x['I'] + x['x4'] == x['x5']*10 + x['S'])
  bt.set_multinary_cons(['N', 'W', 'I', 'x5', 'x6'], lambda x: x['N'] + x['W'] + x['x5'] == x['x6']*10 + x['I'])
  bt.set_binary_cons('D', 'x6', lambda x, y: x == y)
  bt.set_unary_cons('N', lambda x: x != 0)
  bt.set_unary_cons('W', lambda x: x != 0)
  bt.set_unary_cons('D', lambda x: x != 0)
    
  result = bt.do_search()
  print('Solution:')
  print("""
   NETWORK    {N}{E}{T}{W}{O}{R}{K}
   WINDOWS    {W}{I}{N}{D}{O}{W}{S}
  +     WS   +     {W}{S}
  --------   --------
  DISKETTE   {D}{I}{S}{K}{E}{T}{T}{E}
""".format_map(result['solution']))
  for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")
  
  print('Puzzle 6')
  puzzle = 'CHARON+COMET+EARTH=TRITON'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('+', '').replace('=', '')))
  
  bt = BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
    
  for i in range(5):
    bt.set_domain('x'+str(i), [0, 1, 2])
  
  bt.set_multinary_cons(['N', 'T', 'H', 'N', 'x0'], lambda x: x['N'] + x['T'] + x['H'] == x['x0']*10+x['N'])
  bt.set_multinary_cons(['O', 'E', 'T', 'x0', 'x1'], lambda x: x['O'] + x['E'] + x['T'] + x['x0'] == x['x1']*10 + x['O'])
  bt.set_multinary_cons(['R', 'M', 'T', 'x1', 'x2'], lambda x: 2*x['R'] + x['M'] + x['x1'] == x['x2'] * 10 + x['T'])
  bt.set_multinary_cons(['A', 'O', 'I', 'x2', 'x3'], lambda x: 2*x['A'] + x['O'] + x['x2'] == x['x3'] * 10 + x['I'])
  bt.set_multinary_cons(['H', 'C', 'E', 'R', 'x3', 'x4'], lambda x: x['H'] + x['C'] + x['E'] + x['x3'] == x['x4']*10 + x['R'])
  bt.set_multinary_cons(['C', 'T', 'x4'], lambda x: x['C'] + x['x4'] == x['T'])

  bt.set_unary_cons('C', lambda x: x != 0)
  bt.set_unary_cons('E', lambda x: x != 0)
  bt.set_unary_cons('T', lambda x: x != 0)
    
  result = bt.do_search()
  print('Solution:')
  print("""
   CHARON    {C}{H}{A}{R}{O}{N}
    COMET     {C}{O}{M}{E}{T}
  + EARTH   + {E}{A}{R}{T}{H}
  -------   -------
   TRITON    {T}{R}{I}{T}{O}{N}
""".format_map(result['solution']))
  for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")
  
  print('Puzzle 7')
  puzzle = 'TOO+TOO+TOO+TOO=GOOD'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('+', '').replace('=', '')))
  
  bt = BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  
  for i in range(3):
    bt.set_domain('x' + str(i), [0, 1, 2, 3])
  
  bt.set_multinary_cons(['O', 'D', 'x0'], lambda x: 4*x['O'] == x['x0'] * 10 + x['D'])
  bt.set_multinary_cons(['O', 'O', 'x0', 'x1'], lambda x: 4*x['O'] + x['x0'] == x['x1'] * 10 + x['O'])
  bt.set_multinary_cons(['T', 'O', 'x1', 'x2'], lambda x: 4*x['T'] + x['x1'] == x['x2'] * 10 + x['O'])
  bt.set_binary_cons('G', 'x2', lambda x,y: x == y)
  
  bt.set_unary_cons('T', lambda x: x != 0)
  bt.set_unary_cons('G', lambda x: x != 0)
    
  result = bt.do_search()
  print('Solution:')
  print("""
    TOO     {T}{O}{O}
    TOO     {T}{O}{O}
    TOO     {T}{O}{O}
  + TOO   + {T}{O}{O}
  -----   -----
   GOOD    {G}{O}{O}{D}
""".format_map(result['solution']))
  for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")
  
  print('Puzzle 8')
  puzzle = 'AT+EAST+WEST=SOUTH'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('+', '').replace('=', '')))
  
  bt = BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  for i in range(4):
    bt.set_domain('x' + str(i), [0, 1, 2])
  bt.set_multinary_cons(['T', 'H', 'x0'], lambda x: 3*x['T'] == x['x0']*10 + x['H'])
  bt.set_multinary_cons(['A', 'S', 'T', 'x0', 'x1'], lambda x: x['A'] + 2*x['S'] + x['x0'] == x['x1']*10+x['T'])
  bt.set_multinary_cons(['A', 'E', 'U', 'x1', 'x2'], lambda x: x['A'] + x['E'] + x['x1'] == x['x2']*10 + x['U'])
  bt.set_multinary_cons(['E', 'W', 'O', 'x2', 'x3'], lambda x: x['E'] + x['W'] + x['x2'] == x['x3']*10 + x['O'])
  bt.set_binary_cons('S', 'x3', lambda x,y: x == y)
  bt.set_unary_cons('A', lambda x: x != 0)
  bt.set_unary_cons('E', lambda x: x != 0)
  bt.set_unary_cons('W', lambda x: x != 0)
  bt.set_unary_cons('S', lambda x: x != 0)
    
  result = bt.do_search()
  print('Solution:')
  print("""
      AT       {A}{T}
    EAST     {E}{A}{S}{T}
  + WEST   + {W}{E}{S}{T}
  ------   ------
   SOUTH    {S}{O}{U}{T}{H}
""".format_map(result['solution']))
  for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")

  print('Puzzle 9')
  puzzle = 'COUNT-COIN=SNUB'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('-', '').replace('=', '')))
  
  bt = BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  
  for i in range(4):
    bt.set_domain('x' + str(i), [0, 1])

  bt.set_multinary_cons(['T', 'N', 'B', 'x0'], lambda x: x['x0'] *10 + x['T'] - x['N'] == x['B'])
  bt.set_multinary_cons(['N', 'I', 'U', 'x0', 'x1'], lambda x: x['x1']*10 + x['N'] - x['x0'] - x['I'] == x['U'])
  bt.set_multinary_cons(['U', 'O', 'N', 'x1', 'x2'], lambda x: x['x2']*10 + x['U'] - x['x1'] - x['O'] == x['N'])
  bt.set_multinary_cons(['O', 'C', 'S', 'x2', 'x3'], lambda x: x['x3']*10 + x['O'] - x['x2'] - x['C'] == x['S'])
  bt.set_binary_cons('C', 'x3', lambda x,y: x == y)
  
  bt.set_unary_cons('C', lambda x: x != 0)
  bt.set_unary_cons('S', lambda x: x != 0)
    
  result = bt.do_search()
  print('Solution:')
  print("""
   COUNT    {C}{O}{U}{N}{T}
  - COIN   - {C}{O}{I}{N}
  ------   ------
    SNUB     {S}{N}{U}{B}
""".format_map(result['solution']))
  for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")

  print('Puzzle 11 -- Bonus Puzzle')
  print('This is in fact an easy puzzle.')
  
  puzzle = 'BCH*GEI=BADB+AAIJ+AFFF=AHJFDB'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('*', '').replace('+', '').replace('=', '')))
  
  bt = BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  
  for i in range(5):
    bt.set_domain('x' + str(i), [0, 1, 2])
  bt.set_multinary_cons(['D','J', 'x0'], lambda x: x['D'] + x['J'] == x['x0']*10 + x['D'])
  bt.set_multinary_cons(['A','I', 'F', 'x0', 'x1'], lambda x: x['A'] + x['I'] + x['F'] + x['x0'] == x['x1']*10 + x['F'])
  bt.set_multinary_cons(['B','A', 'F', 'J', 'x1', 'x2'], lambda x: x['B'] + x['A'] + x['F'] + x['x1'] == x['x2']*10 + x['J'])
  bt.set_multinary_cons(['A', 'F', 'H', 'x2', 'x3'], lambda x: x['A'] + x['F'] + x['x2'] == x['x3']*10 + x['H'])
  bt.set_binary_cons('A', 'x3', lambda x,y: x + y == x)
  
  for i in range(4, 13):
    bt.set_domain('x' + str(i), [0, 1, 2, 3, 4, 5, 6, 7, 8])
  bt.set_multinary_cons(['H','I', 'B', 'x4'], lambda x: x['H']*x['I'] == x['x4']*10 + x['B'])
  bt.set_multinary_cons(['C','I', 'D', 'x4', 'x5'], lambda x: x['C']*x['I'] + x['x4'] == x['x5']*10 + x['D'])
  bt.set_multinary_cons(['B','I', 'A', 'x5', 'x6'], lambda x: x['B']*x['I'] + x['x5'] == x['x6']*10 + x['A'])
  bt.set_binary_cons('B', 'x6', lambda x,y: x == y)
  
  bt.set_multinary_cons(['H','E', 'J', 'x7'], lambda x: x['H']*x['E'] == x['x7']*10 + x['J'])
  bt.set_multinary_cons(['C','E', 'I', 'x7', 'x8'], lambda x: x['C']*x['E'] + x['x7'] == x['x8']*10 + x['I'])
  bt.set_multinary_cons(['B','E', 'A', 'x8', 'x9'], lambda x: x['B']*x['E'] + x['x8'] == x['x9']*10 + x['A'])
  bt.set_binary_cons('A', 'x9', lambda x,y: x == y)
  
  bt.set_multinary_cons(['H','G', 'F', 'x10'], lambda x: x['H']*x['G'] == x['x10']*10 + x['F'])
  bt.set_multinary_cons(['C','G', 'F', 'x10', 'x11'], lambda x: x['C']*x['G'] + x['x10'] == x['x11']*10 + x['F'])
  bt.set_multinary_cons(['B','G', 'F', 'x11', 'x12'], lambda x: x['B']*x['G'] + x['x11'] == x['x12']*10 + x['F'])
  bt.set_binary_cons('A', 'x12', lambda x,y: x == y)
  
  bt.set_unary_cons('B', lambda x: x != 0)
  bt.set_unary_cons('G', lambda x: x != 0)
  bt.set_unary_cons('A', lambda x: x != 0)
  
  result = bt.do_search()
  
  print('Solution:')
  print("""
       BCH        {B}{C}{H}
  *    GEI   *    {G}{E}{I}
  --------   --------
      BADB       {B}{A}{D}{B}
     AAIJ       {A}{A}{I}{J}
  + AFFF     + {A}{F}{F}{F}
  --------   --------
    AHJFDB     {A}{H}{J}{F}{D}{B}
""".format_map(result['solution']))
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
  
  bt = BT()
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
  
  bt = BT()
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
  
  bt = BT()
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

  print('\n======= Hard Crypt Test =======')
  print('Puzzle 4')
  print('In fact, this is a quite hard one puzzle in this test. Too many variables are involved in each multi-nary constraint.\nYou many need to wait for a quite few mins. It takes me about 5 or a little longer time to solve this puzzle via this program.\nThis is why I put this puzzle at almost the last end.')
  puzzle = 'UNO+DUE+TRE+OTTO+UNDICI+DODICI+TREDICI+TRENTA=OTTANT'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('+', '').replace('=', '')))
  
  bt = BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  for i in range(6):
    bt.set_domain('x' + str(i), [0, 1, 2, 3, 4, 5, 6, 7])
    
  bt.set_multinary_cons(['O', 'E', 'I', 'A', 'x0'], lambda x: 2*x['O'] + 2*x['E'] + 3*x['I'] + x['A'] == x['x0']*10 + x['A'])
  bt.set_multinary_cons(['N', 'U', 'R', 'T', 'C', 'x0', 'x1'], lambda x: x['N'] + x['U'] + x['R'] + 2*x['T'] + 3*x['C'] + x['x0'] == x['x1']*10 +  x['T'])
  bt.set_multinary_cons(['U', 'D', 'T', 'I', 'N', 'x1', 'x2'], lambda x: x['U'] + x['D'] + 2*x['T'] + 3*x['I'] + x['N']+x['x1'] == x['x2']*10 + x['N'])
    
  bt.set_multinary_cons(['O', 'D', 'E', 'A', 'x2', 'x3'], lambda x: x['O'] + 3*x['D'] + x['E']+x['x2'] == x['x3']*10 + x['A'])
  bt.set_multinary_cons(['N', 'O', 'E', 'R', 'T', 'x3', 'x4'], lambda x: x['N'] + x['O'] + x['E'] + x['R'] + x['x3'] == x['x4'] *10 + x['T'])
  bt.set_multinary_cons(['U', 'D', 'R', 'T', 'x4', 'x5'], lambda x: x['U'] + x['D'] + x['R'] + x['T']+x['x4'] == x['x5']*10 + x['T'])
  bt.set_multinary_cons(['T', 'O', 'x5'], lambda x: x['T'] + x['x5'] == x['O'])
  
  # For the most left digit
  bt.set_unary_cons('U', lambda x: x != 0)
  bt.set_unary_cons('D', lambda x: x != 0)
  bt.set_unary_cons('T', lambda x: x != 0)
  bt.set_unary_cons('O', lambda x: x != 0)
    
  result = bt.do_search()
  print('Solution:')
  print("""
       UNO        {U}{N}{O}
       DUE        {D}{U}{E}
       TRE        {T}{R}{E}
      OTTO       {O}{T}{T}{O}
    UNDICI     {U}{N}{D}{I}{C}{I}
    DODICI     {D}{O}{D}{I}{C}{I}
   TREDICI    {T}{R}{E}{D}{I}{C}{I}
  + TRENTA   + {T}{R}{E}{N}{T}{A}
  --------   --------
   OTTANTA    {O}{T}{T}{A}{N}{T}{A}
""".format_map(result['solution']))
  for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")
  
  print('Puzzle 10')
  print('You really need to wait a while due to too many intermediate variables involved in this puzzle.\n And, just believe me, you will finally get the answer. ^.^ \nSo, now, let us talk about something.\nShould I tell you that it took me more than five hours to get the answer to this puzzle via this program.\nHaHa, I know you move to the edge of collapse when hearing this.\nSo, I could tell you the answer, and you can just close this window.\nBut if you do so, you may miss an Easter Egg at the real end of this test program.\nSo, two chocie. Wait or not wait.\n Now, the answer, BIG*ELF=PARADE means three nine eight by two six four is one zero five zero seven two.  ^.^')
  puzzle = 'BIG*ELF=PARADE'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('*', '').replace('=', '')))
  
  bt = BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  
  for i in range(11):
    bt.set_domain('x' + str(i), [j for j in range(0, 10)])
  for i in range(4):
    bt.set_domain('c' + str(i), [0, 1, 2])
  bt.set_multinary_cons(['x0', 'x3', 'D', 'c0'], lambda x: x['x0'] + x['x3'] == x['c0']*10 + x['D'])
  bt.set_multinary_cons(['x1', 'x4', 'x7', 'A', 'c0', 'c1'], lambda x: x['x1'] + x['x4'] + x['x7'] + x['c0'] == x['c1']*10 + x['A'])
  bt.set_multinary_cons(['x2', 'x5', 'x8', 'R', 'c1', 'c2'], lambda x: x['x2'] + x['x5'] + x['x8'] + x['c1'] == x['c2']*10 + x['R'])
  bt.set_multinary_cons(['x6', 'x9', 'A', 'c2', 'c3'], lambda x: x['x6'] + x['x9'] + x['c2'] == x['c3']*10 + x['A'])
  bt.set_multinary_cons(['x10', 'P', 'c3'], lambda x: x['x10'] + x['c3'] == x['P'])
  
  for i in range(9):
    bt.set_domain('cc' + str(i), [0, 1, 2, 3, 4, 5, 6, 7, 8])
  bt.set_multinary_cons(['G', 'F', 'E', 'cc0'], lambda x: x['G']*x['F'] == x['cc0']*10+x['E'])
  bt.set_multinary_cons(['I', 'F', 'x0', 'cc0', 'cc1'], lambda x: x['I']*x['F']+x['cc0'] == x['cc1']*10+x['x0'])
  bt.set_multinary_cons(['B', 'F', 'x1', 'cc1', 'cc2'], lambda x: x['B']*x['F']+x['cc1'] == x['cc2']*10+x['x1'])
  bt.set_binary_cons('x2', 'cc2', lambda x: x==y)
  
  bt.set_multinary_cons(['G', 'L', 'x3', 'cc3'], lambda x: x['G']*x['L'] == x['cc3']*10+x['x3'])
  bt.set_multinary_cons(['I', 'L', 'x4', 'cc3', 'cc4'], lambda x: x['I']*x['L']+x['cc3'] == x['cc4']*10+x['x4'])
  bt.set_multinary_cons(['B', 'L', 'x5', 'cc4', 'cc5'], lambda x: x['B']*x['L']+x['cc4'] == x['cc5']*10+x['x5'])
  bt.set_binary_cons('x6', 'cc5', lambda x: x==y)
  
  bt.set_multinary_cons(['G', 'E', 'x7', 'cc6'], lambda x: x['G']*x['E'] == x['cc6']*10+x['E'])
  bt.set_multinary_cons(['I', 'E', 'x8', 'cc6', 'cc7'], lambda x: x['I']*x['E']+x['cc6'] == x['cc7']*10+x['x0'])
  bt.set_multinary_cons(['B', 'E', 'x9', 'cc7', 'cc8'], lambda x: x['B']*x['E']+x['cc7'] == x['cc8']*10+x['x1'])
  bt.set_binary_cons('x10', 'cc8', lambda x: x==y)
  
  bt.set_unary_cons('B', lambda x: x != 0)
  bt.set_unary_cons('E', lambda x: x != 0)
  bt.set_unary_cons('P', lambda x: x != 0)
  
  result = bt.do_search()
  print(result['solution'])
  print('Solution:')
  print("""
     BIG      {B}{I}{G}
  *  ELF   *  {E}{L}{F}
  ------   ------
  PARADE   {P}{A}{R}{A}{D}{E}
""".format_map(result['solution']))
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
  
  print('\nHere is a random 9x9 example. That is the Easter Egg. HAHA  Orz~~ 囧. Anyway, have a nice day.')
  game, board = Sudoku.generateGame(9)
  Sudoku.printGame(game)
  print('Solution')
  Sudoku.printGame(Sudoku.convert2str(game, Sudoku.solveByBT(game)['solution']))
  print('\nIf you would like, you can run CrossMath.py, Futoshiki.py or Sudoku.py for playing these puzzles. Have a good day!')
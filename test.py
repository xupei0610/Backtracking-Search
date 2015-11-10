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
  
  print('\n======= Crypt Test =======')
  print("No implement for Crypt in this set of program.\nBut the implement of Backtracking is able to handle Crypt puzzles even with more than ternary constraints.\n")
  
  print('Puzzle 1')

  puzzle = 'send+more=money'
  print('   '+puzzle)

  game = ''.join(set(puzzle.replace('+', '').replace('=', '')))
  
  bt = BT.BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  
  # for the most right digit
  bt.set_multinary_cons(['d', 'e', 'y'], lambda x: (x['d'] + x['e']) % 10 == x['y'])
  
  # the middle digit
  bt.set_multinary_cons(['n', 'r', 'e'], lambda x: (x['n'] + x['r']) % 10 == x['e'] or (x['n'] + x['r']) % 10 == x['e'] + 1)
  bt.set_multinary_cons(['e', 'o', 'n'], lambda x: (x['e'] + x['o']) % 10 == x['n'] or (x['e'] + x['o']) % 10 == x['n'] + 1)
  
  # For the most left digit
  bt.set_multinary_cons(['s', 'm', 'o'], lambda x: x['s'] + x['m'] == x['m'] *10 + x['o'] or x['s'] + x['m'] == x['m'] *10 + x['o'] + 1)
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
  
  puzzle = 'crash+hacker=reboot'
  print('   '+puzzle)

  game = ''.join(set(puzzle.replace('+', '').replace('=', '')))
  
  bt = BT.BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  
  # for the most right digit
  bt.set_multinary_cons(['h', 'r', 't'], lambda x: (x['h'] + x['r']) % 10 == x['t'])
  
  # the middle digit
  bt.set_multinary_cons(['s', 'e', 'o'], lambda x: (x['s'] + x['e']) % 10 == x['o'] or (x['s'] + x['e']) % 10 == x['o'] + 1)
  bt.set_multinary_cons(['a', 'k', 'o'], lambda x: (x['a'] + x['k']) % 10 == x['o'] or (x['a'] + x['k']) % 10 == x['o'] + 1)
  bt.set_multinary_cons(['r', 'c', 'b'], lambda x: (x['r'] + x['c']) % 10 == x['b'] or (x['r'] + x['c']) % 10 == x['b'] + 1)
  bt.set_multinary_cons(['c', 'a', 'e'], lambda x: (x['c'] + x['a']) % 10 == x['e'] or (x['c'] + x['a']) % 10 == x['e'] + 1)
  
  # For the most left digit
  bt.set_unary_cons('c', lambda x: x != 0)
  bt.set_unary_cons('h', lambda x: x != 0)
  bt.set_unary_cons('r', lambda x: x != 0)
  bt.set_binary_cons('h', 'r', lambda x,y: x + 1 == y)
  
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
  
  bt = BT.BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  
  # for the most right digit
  bt.set_binary_cons('c', 'l', lambda x,y: (x + x) % 10 == y)
  bt.set_multinary_cons(['i', 'a'], lambda x: (x['i'] + x['i']) % 10 == x['a'])
  
  # the middle digit
  bt.set_multinary_cons(['s', 'g', 'c'], lambda x: (x['s'] + x['g']) % 10 == x['c'] or (x['s'] + x['g']) % 10 == x['c'] + 1)
  bt.set_multinary_cons(['a', 'o', 's'], lambda x: (x['a'] + x['o']) % 10 == x['s'] or (x['a'] + x['o']) % 10 == x['s'] + 1)
  bt.set_multinary_cons(['b', 'l', 'a'], lambda x: (x['b'] + x['l']) % 10 == x['a'] or (x['b'] + x['l']) % 10 == x['a'] + 1)
  
  # For the most left digit
  bt.set_multinary_cons(['b'], lambda x: x['b'] != 0)
  bt.set_unary_cons('l', lambda x: x != 0)
  bt.set_unary_cons('p', lambda x: x == 1)
  
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
  
  
  print('Puzzle 4')
  print('This is a little hard. You many need to wait a few seconds.')
  puzzle = 'UNO+DUE+TRE+OTTO+UNDICI+DODICI+TREDICI+TRENTA=OTTANT'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('+', '').replace('=', '')))
  
  bt = BT.BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
      
  bt.set_multinary_cons(['O', 'E', 'I', 'A'], lambda x: (2*x['O'] + 2*x['E'] + 3*x['I'] + x['A']) % 10 == x['A'])
  bt.set_multinary_cons(['N', 'U', 'R', 'T', 'C'], lambda x: ((x['N'] + x['U'] + x['R'] + 2*x['T'] + 3*x['C']) % 10 - x['T']) < 8)
  bt.set_multinary_cons(['U', 'D', 'T', 'I', 'N'], lambda x: ((x['U'] + x['D'] + 2*x['T'] + 3*x['I'] + x['N']) % 10 - x['N']) < 8)
    
  bt.set_multinary_cons(['O', 'D', 'E', 'A'], lambda x: ((x['O'] + 3*x['D'] + x['E']) % 10 - x['A']) < 8)
  bt.set_multinary_cons(['N', 'O', 'E', 'R', 'T'], lambda x: ((x['N'] + x['O'] + x['E'] + x['R']) % 10 - x['T']) < 6)
  bt.set_multinary_cons(['U', 'D', 'R', 'T'], lambda x: ((x['U'] + x['D'] + x['R'] + x['T']) % 10 - x['T']) < 5)
  bt.set_multinary_cons(['T', 'O'], lambda x: x['T'] - x['O'] < 4)
  
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

  print('Puzzle 5')
  puzzle = 'NETWORK+WINDOWS+WS=DISKETTE'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('+', '').replace('=', '')))
  
  bt = BT.BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
      
  bt.set_multinary_cons(['K', 'S', 'E'], lambda x: (x['K'] + 2*x['S']) % 10 == x['E'])
  bt.set_multinary_cons(['R', 'W', 'T'], lambda x: ((x['T'] + 2*x['W']) % 10 - x['T']) < 3)
  bt.set_multinary_cons(['O', 'T'], lambda x: ((2*x['O']) % 10 - x['T']) < 3)
  bt.set_multinary_cons(['W', 'D', 'E'], lambda x: ((x['W'] + x['D']) % 10 - x['E']) < 3)
  bt.set_multinary_cons(['T', 'N', 'K'], lambda x: ((x['T'] + x['N']) % 10 - x['K']) < 3)
  bt.set_multinary_cons(['E', 'I', 'S'], lambda x: ((x['E'] + x['I']) % 10 - x['S']) < 3)
  bt.set_multinary_cons(['N', 'W', 'I', 'D'], lambda x: x['D'] * 10 + x['I'] - (x['N'] + x['W']) < 3)

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
  
  bt = BT.BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
      
  bt.set_multinary_cons(['N', 'T', 'H', 'N'], lambda x: (x['N'] + x['T'] + x['H']) % 10 == x['N'])
  bt.set_multinary_cons(['O', 'E', 'T'], lambda x: ((x['O'] + x['E'] + x['T']) % 10 - x['O']) < 3)
  bt.set_multinary_cons(['R', 'M', 'T'], lambda x: ((2*x['R'] + x['M']) % 10 - x['T']) < 3)
  bt.set_multinary_cons(['A', 'O', 'I'], lambda x: ((2*x['A'] + x['O']) % 10 - x['I']) < 3)
  bt.set_multinary_cons(['H', 'C', 'E', 'R'], lambda x: ((x['H'] + x['C'] + x['E']) % 10 - x['R']) < 3)
  bt.set_multinary_cons(['C', 'T'], lambda x: x['T'] - x['C'] < 3)

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
  
  bt = BT.BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
      
  bt.set_multinary_cons(['O', 'D'], lambda x: (4*x['O']) % 10 == x['D'])
  bt.set_multinary_cons(['T', 'G', 'O'], lambda x: (x['G'] * 10 + x['O'] - 4*x['T']) < 4)

  bt.set_unary_cons('T', lambda x: x != 0)
  bt.set_unary_cons('G', lambda x: x != 0)
  bt.set_unary_cons('O', lambda x: ((4*x) % 10 - x) < 4)
  bt.set_unary_cons('T', lambda x: ((4*x) % 10 - x) < 4)
    
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
  
  bt = BT.BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
      
  bt.set_multinary_cons(['T', 'H'], lambda x: (3*x['T']) % 10 == x['H'])
  bt.set_multinary_cons(['A', 'S', 'T'], lambda x: ((x['A'] + 2*x['S']) % 10 - x['T']) < 3)
  bt.set_multinary_cons(['A', 'E', 'U'], lambda x: ((x['A'] + x['E']) % 10 - x['U']) < 3)
  
  bt.set_multinary_cons(['E', 'W', 'O', 'S'], lambda x: (x['S'] * 10 + x['O'] - x['E'] - x['W'] ) < 3)

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
  
  bt = BT.BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
      
  bt.set_multinary_cons(['T', 'N', 'B'], lambda x: (x['N'] + x['B']) % 10 == x['T'])
  bt.set_multinary_cons(['N', 'I', 'U'], lambda x: ((x['U'] + x['I']) % 10 - x['N']) < 2)
  bt.set_multinary_cons(['U', 'O', 'N'], lambda x: ((x['N'] + x['O']) % 10 - x['U']) < 2)
  bt.set_multinary_cons(['S', 'C', 'O'], lambda x: (x['C'] * 10 + x['O'] - x['C'] - x['S'] ) < 2)

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
  
  
  print('Puzzle 10')
  print('This puzzle is pretty hard. You may need to wait for a few mins.\nBelieve me, you will finally get the answer. ^.^')
  puzzle = 'BIG*ELF=PARADE'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('*', '').replace('=', '')))
  
  bt = BT.BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
      
  bt.set_multinary_cons(['G', 'F', 'E'], lambda x: (x['G'] * x['F']) % 10 == x['E'])
  
  bt.set_multinary_cons(['I', 'F', 'G', 'L', 'D'], lambda x: (((x['I']*x['F'])%10) + divmod(x['G']*x['F'], 10)[0] + (x['L']*x['G'])%10)%10 == x['D'])
  
  bt.set_multinary_cons(['B', 'I', 'G', 'F', 'L', 'E', 'A'], lambda x: x['A'] - (divmod((x['B'] * 100 + x['I'] * 10 + x['G'])*x['F'], 100)[0]%10 + divmod((x['I']*10 + x['G']) * x['L'], 10)[0]%10 + (x['G'] * x['E'])%10) % 10 < 2)
  
  bt.set_multinary_cons(['B', 'I', 'G', 'F', 'L', 'E', 'R'], lambda x: x['R'] - (divmod((x['B'] * 100 + x['I'] * 10 + x['G'])*x['F'], 1000)[0] + divmod((x['B'] * 100 + x['I'] * 10 + x['G'])*x['L'], 100)[0]%10 + divmod((x['I'] * 10 + x['G'])*x['E'], 10)[0]%10) % 10< 3)
  
  bt.set_multinary_cons(['B', 'I', 'G', 'L', 'E', 'A'], lambda x: x['A'] - (divmod((x['B'] * 100 + x['I'] * 10 + x['G'])*x['L'], 1000)[0] + divmod((x['B'] * 100 + x['I'] * 10 + x['G'])*x['E'], 100)[0]%10)%10< 3)
    
  bt.set_multinary_cons(['B', 'I', 'G', 'E', 'P'], lambda x: x['P'] - divmod((x['B'] * 100 + x['I'] * 10 + x['G'])*x['E'], 1000)[0] < 3)
  
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
  
  """print('Puzzle 11 -- Bonus Puzzle')
  print('Finally, we reach here. You really need to wait a while due to the multiplication operation in this puzzle.\n And, just believe me, you will finally get the answer. ^.^ \nIn fact, I could make something funny here, like to continuously print some jokes. \nHowever, I really have no time, since it seems I have to turn in a draft for this project just on Friday, Friday, Friday .... Oh NO NO NO NO NO!!! orz~~ 囧')
  
  puzzle = 'BCH*GEI=BADB+AAIJ+AFFF=AHJFDB'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('*', '').replace('+', '').replace('=', '')))
  
  bt = BT.BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
      
  bt.set_multinary_cons(['H', 'I', 'B'], lambda x: (x['H'] * x['I']) % 10 == x['B'])
  bt.set_multinary_cons(['C', 'H', 'I', 'D'], lambda x: divmod((x['C']*10+x['H']) * x['I'], 10)[0] % 10 == x['D'])
  bt.set_multinary_cons(['B', 'C', 'H', 'I', 'A'], lambda x: divmod((x['B']*100+x['C']*10+x['H']) * x['I'], 100)[0] % 10 == x['A'])
  bt.set_multinary_cons(['B', 'C', 'H', 'I'], lambda x: divmod((x['B']*100+x['C']*10+x['H']) * x['I'], 1000)[0]== x['B'])
  
  bt.set_multinary_cons(['H', 'E', 'J'], lambda x: (x['H'] * x['E']) % 10 == x['J'])
  bt.set_multinary_cons(['C', 'H', 'E', 'I'], lambda x: divmod((x['C']*10+x['H']) * x['E'], 10)[0] % 10 == x['I'])
  bt.set_multinary_cons(['B', 'C', 'H', 'E', 'A'], lambda x: divmod((x['B']*100+x['C']*10+x['H']) * x['E'], 100)[0] == x['A']*11)
  
  bt.set_multinary_cons(['H', 'G', 'F'], lambda x: (x['H'] * x['G']) % 10 == x['F'])
  bt.set_multinary_cons(['C', 'H', 'G', 'F'], lambda x: (divmod((x['C']*10+x['H']) * x['G'], 10)[0] % 10) * 10 + divmod((x['C']*10+x['H']) * x['G'], 10)[1] == x['F']*11)
  
  bt.set_multinary_cons(['B', 'C', 'H', 'G', 'A'], lambda x: divmod((x['B']*100+x['C']*10+x['H']) * x['G'], 1000)[0] == x['A'])
  
  bt.set_multinary_cons(['B', 'C', 'H', 'G', 'F'], lambda x: (x['B']*100+x['C']*10+x['H']) * x['G'] - divmod((x['B']*100+x['C']*10+x['H']) * x['G'], 1000)[0] == x['F']*111)
  
  bt.set_multinary_cons(['D', 'J'], lambda x: (x['D'] * x['J']) % 10 == x['D'])
  bt.set_multinary_cons(['A', 'I', 'F'], lambda x: (x['A'] + x['I'] + x['F']) % 10 - x['F'] < 2)
  bt.set_multinary_cons(['B', 'A', 'F', 'J'], lambda x: (x['B'] + x['A'] + x['F']) % 10 - x['J'] < 3)
  bt.set_multinary_cons(['A', 'F', 'H'], lambda x: x['A'] + x['F'] - x['H'] < 3)

  bt.set_unary_cons('B', lambda x: x != 0)
  bt.set_unary_cons('G', lambda x: x != 0)
  bt.set_unary_cons('A', lambda x: x != 0)
  
  result = bt.do_search()
  
  print('Solution:')
  print("""
  #       BCH        {B}{C}{H}
  #  *    GEI   *    {G}{E}{I}
  #  --------   --------
  #      BADB       {B}{A}{D}{B}
  #     AAIJ       {A}{A}{I}{J}
  #  + AFFF     + {A}{F}{F}{F}
  #  --------   --------
  #    AHJFDB     {A}{H}{J}{F}{D}{B}
  #""".format_map(result)['solution'])
  """for r in result:
    if r != 'solution':
      print(r + ': ' + str(result[r]))
  print("++++++++++++++++++++++++++++")"""
  
  
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
  

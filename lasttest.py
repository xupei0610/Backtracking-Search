import time
import CrossMath, Futoshiki, Sudoku
from BT import *
  
if __name__ == '__main__':

  print('Puzzle 10')
  print('You really need to wait a while due to the multiplication operation in this puzzle.\n And, just believe me, you will finally get the answer. ^.^ \nIn fact, I could make something funny here, like to continuously print some jokes. \nHowever, I really have no time, since it seems I have to turn in a draft for this project just on Friday, Friday, Friday .... Oh NO NO NO NO NO!!! orz~~ 囧. ^.^')
  puzzle = 'BIG*ELF=PARADE'
  print("   " + puzzle)

  game = ''.join(set(puzzle.replace('*', '').replace('=', '')))
  
  bt = BT()
  default_domain = [i for i in range(0, 10)]
  
  for i in range(len(game)):
    bt.set_domain(game[i], default_domain)
    for j in range(i+1, len(game)):
      bt.set_binary_cons(game[i], game[j], lambda x,y: x != y)
  for i in range(9):
    bt.set_domain('x' + str(i), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
  bt.set_multinary_cons(['G', 'F', 'E', 'x0'], lambda x: x['G'] * x['F'] == x['0'] * 10 + x['E'])
  
  bt.set_multinary_cons(['I', 'F', 'G', 'L', 'D', 'x0', 'x1', 'x3'], lambda x: \
  x['I']*x['F']+x['x0'] + x['G']*x['L'] == (x['x1'] + x['x3'])*10 + x['D'] )
  bt.set_multinary_cons(['B', 'F', 'I', 'L', 'G', 'E', 'x1', 'x3', 'x2', 'x4', 'x6'], lambda x: \
  x['B']*x['F']+x['x1'] + x['I']*x['L']+x['x3'] + x['G']*x['E'] == (x['x2'] + x['x4'] + x['6'])*10 + x['A'] )
  bt.set_multinary_cons(['B', 'L', 'I', 'E', 'R', 'x5', 'x7', 'x2', 'x4', 'x6'], lambda x: \
  x['x2'] + x['B']*x['L']+x['x4'] + x['I']*x['E']+x['x6'] == (x['x5'] + x['x7'])*10 + x['R'] )
  bt.set_multinary_cons(['B', 'E', 'A', 'x5', 'x7', 'x8'], lambda x: \
  x['x5'] + x['B']*x['E']+x['x7'] == x['x8']*10 + x['A'] )
  
  bt.set_binary_cons('P', 'x8', lambda x,y: x==y)
  
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
  
  bt = BT()
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
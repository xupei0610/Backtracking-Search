# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "16:00, Nov. 7th, 2015"
""" This is the library file of the part 2 that belong to the project of Comparison of Search Algorithms.
This file supplies an implement for Sudoku game. This program only works for square Sudoku games with square regions. It works well for a standard database format of 9x9 Sudoku game like '4...3.......6..8..........1....5..9..8....6...7.2........1.27..5.3....4.9........'. For the bigger game, ',' should be used to between two numbers or '.'s.
 This file supplies three functions.
The function generateGame(size) could generate a solvable Sudoku game randomly in the format of string. Any game generated via this function has but not necessarily only has one solution.
The function parseGame(game_str) could return a list composed by constraints to each row and col according to the given string that represents a game.
The function printGame(game_str) could print the game board according to the given string that represent a game.
Attention: No legality check to the input game_str in the latter two function (TODO maybe)."""

import random, sys
import BT

def generateGame(size):
  """ Generate a string that represents a size by size Sudoku game with sqrt(size) by sqrt(size) regions. A standard Sudoku usually should have and only have one solution. Games generated via this function only is guaranteed solvable.
  Return game_str, solution  where
    game_str is a string where . represents a slot with unknown number and a digit number represents a slot with a known number, and ',' will be used between two numbers if more than one digit numbers appear.
    solution is a string shown one solution to the game represented by game_str."""
  region_size = int(size**0.5)
  
  # Generate a modified Latin Square suitable for Sudoku, namely the square whose sub regions are also latin squares.
  latin = set(i for i in range(1, size+1))
  
  # Increase the system's limit on recurion times for the low efficiency of the below function
  sys.setrecursionlimit(2000000)
  def generate_modified_latin_square():
    board = [random.sample([i for i in range(1, size+1)], size)]
    latin = set(i for i in range(1, size+1))
    col = []
    regions = []
    for i in range(size):
      col.append([board[0][i]])
      if i < region_size:
        regions.append(board[0][i*region_size:(i+1)*region_size])
      else:
        regions.append([])
    for i in range(size-1):
      board.append([])
      for j in range(size):
        x_pos = divmod(i+1, region_size)[0]
        y_pos = divmod(j, region_size)[0]
        region_id = x_pos * region_size + y_pos
        candidate = list(latin.difference(set(col[j]).union(set(board[i+1])).union(set(regions[region_id]))))
        if candidate:
          board[i+1].append(random.choice(candidate))
          col[j].append(board[i+1][j])
          regions[region_id].append(board[i+1][j])
        else:
          return generate_modified_latin_square()
    return board

  board = generate_modified_latin_square()

  # Randomly remove numbers from the game grid until the amount of remaining numbers is between 3*region_size and 3*game_size 
  not_need_removed = random.randint(3*region_size, 3*size)
  not_removed_vars = []
  def random_remove_nums():
    var = (random.randint(0, size-1), random.randint(0, size-1))
    if var in not_removed_vars:
      return random_remove_nums()
    else:
      return var
    
  for i in range(not_need_removed):
    not_removed_vars.append(random_remove_nums())
  
  # Construct the solution and the game into a string respectively
  board_str = ''
  game_str = ''
  for i in range(size):
    board_str = board_str + ',' + ','.join([str(k) for k in board[i]])
    for j in range(size):
      if (i, j) not in not_removed_vars:
        board[i][j] = '.'
    game_str = game_str + ',' + ','.join([str(k) for k in board[i]])

  board_str = str(board_str[1:])
  game_str = str(game_str[1:])
  if size <= 9:
    board_str = board_str.replace(',', '')
    game_str = game_str.replace(',', '')
    
  return game_str, board_str

def parseGame(game_str):
  """ Parse the game string and return the constraints according the given game string.
  Return {size: game_size, region_size: region_size, variables: {var_name:n, ....}} where n represents a unary constraint that the variable whose name is var_name should be n, and var_name is formatted as var_n1_n2 where n1 and n2 are numbers that respectively represents the row and the column where the slot represented by this variable is at."""

  total_squares = len(game_str)
  game_size = int(total_squares ** 0.5)
  region_size = int(game_size ** 0.5)

  results = {}
  if ',' in game_str:
    game_str = game_str.split(',')
  
  for i in range(len(game_str)):
    x_pos, y_pos = divmod(i, game_size)
    x_pos = x_pos + 1
    y_pos = y_pos + 1
    var_name = construct_var_name(x_pos, y_pos)
    results[var_name] = []
    if game_str[i] != '.':
      results[var_name].append(int(game_str[i]))
    if y_pos < game_size:
      for j in range(y_pos+1, game_size+1):
        results[var_name].append([construct_var_name(x_pos, j), '!='])
    if x_pos < game_size:
      for j in range(x_pos+1, game_size+1):
        results[var_name].append([construct_var_name(j, y_pos), '!='])
    r_x_pos = x_pos % region_size
    r_y_pos = y_pos % region_size
    if r_x_pos == r_y_pos:
      if r_x_pos != 0:
        for j in range(y_pos+1, y_pos+1+region_size-r_y_pos):
          for k in range(x_pos+1, x_pos+1+region_size-r_x_pos):
            results[var_name].append([construct_var_name(k, j), '!='])

  res = {'variables':results, 'size':game_size, 'region_size': region_size}
  return res

def construct_var_name(row, col): 
  """ Construct the variable name to represent a slot at the puzzle grid."""
  return 'var_' + str(row) + '_' + str(col)
  
def printGame(game_str):
  """ Print the board for a game according to the given game string."""

  game_str = game_str.replace('.', '▤')
  if ',' in game_str:
    game_str = game_str.split(',')
  total_squares = len(game_str)
  game_size = int(total_squares ** 0.5)
  region_size = int(game_size ** 0.5)
  
  max_unit_width = len(str(game_size))
  
  r = ''
  for i in range(total_squares):
    r = r + game_str[i] + ' ' * (max_unit_width - len(game_str[i]))
    if (i+1) % game_size == 0:
      r = r + '\n'
    elif (i+1) % region_size == 0:
      r = r + ' | '
    else:
      r = r + ' '
    if i+1 < total_squares and (i+1) % (game_size * region_size) == 0:
      r = r + (('-'*max_unit_width + ' ')*region_size + '  ') * region_size + '\n'

  print(r)

def solveByBT(game_str, v_binding_method = 'MRV+DH', inference_method = 'MAC', preprocess_by_PC = True):
  """A Sudoku solver calling Backtracking Search and use the constraints parsed by the function parseGame().
  Return a solution string if a solution is found; or an empty string otherwise."""

  game_inform = parseGame(game_str)
  default_domain = [i for i in range(1, game_inform['size']+1)]
  
  bt_search = BT.BT()

  # Set up Futoshiki game for Backtracking Search
  for i in game_inform['variables']:
    bt_search.set_domain(i, default_domain)
    for c in game_inform['variables'][i]:
      if isinstance(c, int):
        bt_search.set_unary_cons(i, eval('lambda x: x==' + str(c)))
      else:
        bt_search.set_binary_cons(i, c[0], eval('lambda x,y: x' + c[1] + 'y'))

  return bt_search.do_search(v_binding_method, inference_method, preprocess_by_PC)
  
def convert2str(game_str, variable_dict):
  if variable_dict:
    size = int(len(variable_dict)**0.5)
    solution = ''
    for i in range(1, size + 1):
      for j in range(1, size + 1):
        solution = solution + str(variable_dict[construct_var_name(i,j)])
    return solution
  else:
    return None

if __name__ == "__main__":
  print(__file__)
  print('Author: %s'%__author__)
  print('Copyright: %s'%__copyright__)
  print('License: %s'%__license__)
  print('Version: %s'%__version__)
  print("\nThis is the library file of the part 2 that belong to the project of Comparison of Search Algorithms.\nThis file supplies an implement for Sudoku game. This program only works for square Sudoku games with square regions. It works well for a standard database format of 9x9 Sudoku game like\n '4...3.......6..8..........1....5..9..8....6...7.2........1.27..5.3....4.9........'.\nFor the bigger game, ',' should be used to between two numbers or '.'s.\nThis file supplies three functions.\nThe function generateGame(size) could generate a solvable Sudoku game randomly in the format of string. Any game generated via this function has but not necessarily only has one solution.\nThe function parseGame(game_str) could return a list composed by constraints to each row and col according to the given string that represents a game.\nThe function printGame(game_str) could print the game board according to the given string that represent a game.\nAttention: No legality check to the input game_str in the latter two function (TODO maybe).\n")
  
  game_str, board_str = generateGame(random.choice([4, 9]))

  print('You can try this:\n(or re-run this file to try another game that may have different size or/and difficulty)\n')
  printGame(game_str)

  input('\nPress \'enter\' or \'return\' to show the solution.')
 
  print('\nSolution:\n')
  printGame(board_str)
  print('The above solution is obtained when generating the game.')
  print('The below solution is obtained via Backtracking Search.\n')
  printGame(convert2str(game_str, solveByBT(game_str)['solution']))
  
  print('Games generated here may have multiple solutions.\nHence, the above two solutions may be different.\n')
  
# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "20:50, Nov. 6th, 2015"
""" This is the library file of the part 2 that belong to the project of Comparison of Search Algorithms.
This file supplies an implement for Futoshiki game. The maximum game size supported is 9x9; otherwise an illegal result may be returned via the function parseGame() or printGame(). 
This file supplies three functions.
The function generateGame(size) could generate a solvable Futoshiki game randomly in the format of string. Any game generated via this function has but not necessarily only has one solution.
The function parseGame(game_str) could return a list composed by constraints to each inequality according to the given string that represents a game.
The function printGame(game_str) could print the game board according to the given string that represent a game.
Attention: No legality check to the input game_str in the latter two function (TODO maybe)."""

import random, sys
import BT

def generateGame(size):
  """ Generate a string that represents a size by size Futoshiki game. A standard Futoshiki usually should have and only have one solution. Games generated via this function only is guaranteed solvable.
  Return game_str, solution  where
    game_str is a string where . represents a slot with unknown number, a digit number represents a slot with a known number, > or < represents that the left number should be greater or smaller than the right number, and ^ or v represents that the left number should be smaller or greater than the corresponding number in the next row; and
    solution is a string shown one solution to the game represented by game_str."""
  
  # Generate a Latin square as the basic board.
  sys.setrecursionlimit(2000000) # It is not an efficient way to generate the Latin square.
  board = generate_latin_square(size)
  
  # Randomly assign inequal signs into the board. The amount of inequal signs is between game size and 2 * game size, including game_size and 2*game_size)
  no_neq_signs = random.randint(size, 2*size)
  inequs = {}
  def random_select():
    row = random.randint(0, size-2)
    col = random.randint(0, size-2)
    if row == size - 1 and col == size - 1:
      return random_select()
    if row == size - 1:
      target_row = row
      target_col = col + 1
    elif col == size - 1:
      target_row = row + 1
      target_col = col
    else:
      target = random.randint(0, 1)
      if target:
        target_row = row + 1
        target_col = col
      else:
        target_row = row
        target_col = col + 1
      var_name = str(row) + '_' + str(col)
      target_var_name = str(target_row) + '_' + str(target_col)
      if var_name in inequs:
        for x in inequs[var_name]:
          if x[0] == target_var_name:
            return random_select()
      return [row, col, target_row, target_col]
      
  for i in range(no_neq_signs):
    res = random_select()
    if board[res[0]][res[1]] > board[res[2]][res[3]]:
      if res[0] == res[2]:
        sign = '>'
      else:
        sign = 'v'
    else:
      if res[0] == res[2]:
        sign = '<'
      else:
        sign = '^'
    var_name = str(res[0])+'_'+str(res[1])
    if var_name not in inequs:
      inequs[var_name] = []
    inequs[var_name].append([str(res[2])+'_'+str(res[3]), sign])

  # Randomly remove numbers from the board until the amount of remaining numbers is between 0 and game size (including 0 and game size)
  no_concealed_slots = size*size - random.randint(0, size)
  not_concealed_vars = []
  def random_conceal_slot():
    var_name = str(random.randint(0, size-1))+'_'+str(random.randint(0, size-1))
    if var_name in not_concealed_vars:
      return random_conceal_slot()
    else:
      return var_name

  for i in range(no_concealed_slots):
    not_concealed_vars.append(random_conceal_slot())
  
  # Construct the solution into a string 
  board_str = ''
  for i in range(size):
    for j in range(size):
      var_name = str(i)+'_'+str(j)
      board_str = board_str + str(board[i][j])
      if var_name in inequs:
        for x in inequs[var_name]:
          board_str = board_str + x[1]
  
  # Construct the game into a string
  game_str = ''
  for i in range(size):
    for j in range(size):
      var_name = str(i)+'_'+str(j)
      if var_name not in not_concealed_vars:
        game_str = game_str + str(board[i][j])
      else:
        game_str = game_str + '.'
      if var_name in inequs:
        for x in inequs[var_name]:
          game_str = game_str + x[1]
  
  return game_str, board_str

def parseGame(game_str):
  """ Parse the game string and return the constraints according the given game string.
  Return {size: game_size, variables: {var_name:[n, [var_name2, relation]], ....}} where n represents a unary constraint that the variable whose name is var_name should be n, relation (> or < or !=) represents a binary constraint that the variable whose name is var_name > or < or != the variable whose name is var_name2, and var_name is formatted as var_n1_n2 where n1 and n2 are numbers that respectively represents the row and the column where the slot represented by this variable is at.
  """
  game_size = len(game_str.replace('>','').replace('<','').replace('v', '').replace('^', '')) ** 0.5
  if game_size != int(game_size):
    raise TypeError('Supplied Game Information Is Illegal.')  
  game_size = int(game_size)
  rn = 0
  results = {}
  for i in game_str:
    x_pos, y_pos = divmod(rn, game_size)
    if i in ['>', '<', '^', 'v']:
      if y_pos == 0:
        y_pos = game_size
      else:
        x_pos = x_pos + 1
      left_var = construct_var_name(x_pos, y_pos)
      if i in ['>', '<']:
        sign = i
        target_var = construct_var_name(x_pos, y_pos+1)
      else:
        if i == '^':
          sign = '<'
        else:
          sign = '>'
        target_var = construct_var_name(x_pos+1, y_pos)
      for j in range(len(results[left_var])):
        if isinstance(results[left_var][j], list) and results[left_var][j][0] == target_var:
          results[left_var][j][1] = sign
          break
    else:
      rn = rn + 1
      x_pos = x_pos + 1
      y_pos = y_pos + 1
      var_name = construct_var_name(x_pos, y_pos)
      results[var_name] = []
      if i.isdigit():
          results[var_name].append(int(i))
      if y_pos < game_size:
        for j in range(y_pos+1, game_size+1):
          results[var_name].append([construct_var_name(x_pos, j), '!='])
      if x_pos < game_size:
        for j in range(x_pos+1, game_size+1):
          results[var_name].append([construct_var_name(j,y_pos), '!='])

  # add the only remaining variable into the parse results
  results[construct_var_name(game_size, game_size)] = []
  
  # Other game information
  res = {'variables':results, 'size':game_size}
  
  return res
    
def printGame(game_str):
  """ Print the board for a game according to the given game string."""
  game_size = len(game_str.replace('>','').replace('<','').replace('v', '').replace('^', '')) ** 0.5
  if game_size != int(game_size):
    raise TypeError('Supplied Game Information Is Illegal.')  
  game_size = int(game_size)
  rn = 0
  for i in game_str.replace('.', '▤'):
    if i == '>' or i == '<':
      r1 = r1[:-2] + i + ' '
    elif i == 'v' or i == '^':
      if rn % game_size == 0:
        r2 = r2[:-2] + i
      else:
        r2 = r2[:-4] + i + '   '
    else:
      if rn % game_size == 0:
        if 'r1' in locals():
          print(r1)
          print(r2)
        r1 = ''
        r2 = ''
      rn = rn+1
      if rn % game_size == 0:
        r1 = r1 + i
        r2 = r2 + ' '
      else:
        r1 = r1 + i + '   '
        r2 = r2 + '    '
  print(r1)

def generate_latin_square(size):
  """ This function return a two-dimensional list that represents a Latin square.
  It is a simple but not very efficient way to generate a Latin square."""
  board = [random.sample([i for i in range(1, size+1)], size)]
  latin = set(i for i in range(1, size+1))
  col = []
  for i in range(size):
    col.append([board[0][i]])
  for i in range(size-1):
    board.append([])
    for j in range(size):
      candidate = list(latin.difference(set(col[j]).union(set(board[i+1]))))
      if candidate:
        board[i+1].append(random.choice(candidate))
        col[j].append(board[i+1][j])
      else:
        return generate_latin_square(size)
  return board

def construct_var_name(row, col):
  """ Construct the variable name to represent a slot at the puzzle grid."""
  return 'var_' + str(row) + '_' + str(col)


def solveByBT(game_str, v_binding_method = 'MRV+DH', inference_method = 'MAC', preprocess_by_PC = True):
  """A Futoshiki solver calling Backtracking Search and use the constraints parsed by the function parseGame().
  Return a solution string if a solution is found; or None otherwise."""
  
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
    rn = 0
    for i in game_str:
      if i == '.':
        x, y = divmod(rn, size)
        solution = solution + str(variable_dict[construct_var_name(x+1, y+1)])
        rn = rn + 1
      else:
        if i.isdigit():
          rn = rn + 1
        solution = solution + i
    return solution
  else:
    return None


if __name__ == "__main__":

  print(__file__)
  print('Author: %s'%__author__)
  print('Copyright: %s'%__copyright__)
  print('License: %s'%__license__)
  print('Version: %s'%__version__)
  print("This is the library file of the part 2 that belong to the project of Comparison of Search Algorithms.\nThis file supplies an implement for Futoshiki game. The maximum game size supported is 9x9; otherwise an illegal result may be returned via the function parseGame() or printGame().\nThis file supplies three functions.\nThe function generateGame(size) could generate a solvable Futoshiki game randomly in the format of string. Any game generated via this function has but not necessarily only has one solution.\nThe function parseGame(game_str) could return a list composed by constraints to each inequality according to the given string that represents a game.\nThe function printGame(game_str) could print the game board according to the given string that represent a game.\nAttention: No legality check to the input game_str in the latter two function (TODO maybe).\n")
  
  game_str, board_str = generateGame(random.randint(4, 8))

  print('You can try this:\n(or re-run this file to try another game that may have different size or/and difficulty)\n')
  
  printGame(game_str)
  
  input('\nPress \'enter\' or \'return\' to show the solution.')
 
  print('\nSolution:\n')
  printGame(board_str)
  
  print('The above solution is obtained when generating the game.')
  print('The below solution is obtained via Backtracking Search.\n')
  
  printGame(convert2str(game_str, solveByBT(game_str)['solution']))
  
  print('Games generated here may have multiple solutions.\nHence, the above two solutions may be different.\n')

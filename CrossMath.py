# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "03:34, Nov. 7th, 2015"
""" This is the library file of the part 2 that belong to the project of Comparison of Search Algorithms.
This file supplies an implement for Cross-Math game.
This file supplies three functions.
The function generateGame(size) could generate a solvable CrossMath game randomly in the format of string. Any game generated via this function has but not necessarily only has one solution.
The function parseGame(game_str) could return a list composed by constraints to each row and col according to the given string that represents a game.
The function printGame(game_str) could print the game board according to the given string that represent a game.
Attention: No legality check to the input game_str in the latter two function (TODO maybe)."""

# TODO bracket support

import random
import BT

def generateGame(size):
  """ Generate a string that represents a size by size CrossMath game. A standard CrossMath usually should have and only have one solution. Games generated via this function only is guaranteed solvable.
  Return game_str, solution where
    game_str is a string composed by dot, operation signs and some numbers split by ',' at the end of the string. A pair of operation signs decorate a dot that represent a slot in the game, the slot who is located at the left to the first operation sign and the above to the second operation sign. the numbers are the results of each row and column from top to right and then left to right.
    solution is a string composed by numbers and operation signs. A pair of operation signs decorate the number at the front of them.
  e.g. A game like the below can be presented via game_str = '.<++.^+*.=/.+-.*-.=/.+=.-=.==15,24,14,3,12,4' where <, >, ^, v represent brackets
                  ^
          <▤  +  ▤> +  ▤  = 15
           +   *        /   
           ▤  +  ▤  *  ▤  = 24
           -     -v     /   
           ▤  +  ▤  -  ▤  = 14
           =     =      =   
           3     12     4
  Its solution is '4<++3>^+*8=/5+-7v*-2=/6+=9-=1==15,24,14,3,12,4'."""
  # Generate a square as the basic board. 
  board = random.sample([i for i in range(1, size*size+1)], size*size)
  
  # Randomly assign opertation signs between two slots.
  signs = ''
  divisible = []
  for i in range(size):
    for j in range(size-1):
      res = board[i*size+j] / board[i*size+j+1]
      if res == int(res):
        divisible.append(True)
      else:
        divisible.append(False)
  for i in range(size):
    for j in range(size-1):
      res = board[j*size+i] / board[j*size+i+size]
      if res == int(res):
        divisible.append(True)
      else:
        divisible.append(False)

  operation_signs = ['+', '-', '*']
  for i in range(2*size*(size-1)):
    if divisible[i] == True and random.randint(0, 1) == 1:
      signs = signs + '/'
    else:
      signs = signs + random.choice(operation_signs)

    
  # Calculate the result for each column and row according to the assigned operation signs.
  start = 0
  game_results = []
  for i in range(size):
    equation = ''
    end = start + size - 1
    sign = signs[start:end]
    start = end
    for j in range(size-1):
      equation = equation + str(board[i*size+j]) + sign[j]
    equation = equation + str(board[i*size+j+1])
    game_results.append(str(int(eval(equation))))
  start = size*(size-1)
  for i in range(size):
    equation = ''
    end = start + size - 1
    sign = signs[start:end]
    start = end
    for j in range(size - 1):
      equation = equation + str(board[j*size+i]) + sign[j]
    equation = equation + str(board[(j+1)*size+i])
    game_results.append(str(int(eval(equation))))

  # Construct the solution and game into a string respectivley
  board_str = ''
  game_str = ''
  for i in range(size*size):
    x_pos, y_pos = divmod(i, size)
    
    if y_pos == size - 1:
      right = '='
    else:
      right = signs[i-x_pos]
    if x_pos == size - 1:
      bottom = '='
    else:
      bottom = signs[size*(size-1) + (size-1)*y_pos + x_pos]
    board_str = board_str + str(board[x_pos*size+y_pos]) + right + bottom
    game_str = game_str + '.' + right + bottom
  board_str = board_str + ','.join(game_results)
  game_str = game_str + ','.join(game_results)
  
  # TODO maybe add some bracket

  return game_str, board_str
  

def parseGame(game_str):
  """ Parse the game string and return the constraints according the given game string.
  Return {size:game_size, variables: {var_name:[var_name, '!=']}, constraints: [[pos, id, relation, result], ...]} where
  size is the game size, variables contains all variables' name and its binary constraint, and constraints is the constraints on each row and column.
  In constraints, pos == 'row' or 'col', id is a digit string that represents which row or col this constraint is aimed at, relation is a string composed by '+', '-', 'x' and '/' that represents the operation between the squares at this row or col, and result is a digit string that represents the result of the operation."""
  index_pos = game_str.index('==')
  
  # In CrossMath game, all squares are unknown. Therefore, only operation signs need to be parsed.
  tmp_game_signs = game_str[:index_pos+2].replace('.', '')
  for i in range(10):
    tmp_game_signs = tmp_game_signs.replace(str(i), '')

  game_results = game_str[index_pos+2:].split(',')
  game_size = int(len(game_results) / 2)

  dealt = 0
  game_signs = ['' for i in range(game_size*game_size*2)]
  for i in tmp_game_signs:
    if i in ['<', '>', '^', 'v']:
      if i == '<':
        game_signs[dealt] = '('
      if i == '>':
        game_signs[dealt] = ')'
      if i == '^':
        game_signs[dealt+1] = '('
      if i == 'v':
        game_signs[dealt+1] = ')'
    else:
      game_signs[dealt] = game_signs[dealt] + i
      dealt = dealt + 1

  result = []
  for i in range(game_size):
    relation = ''
    relation2 = ''
    for j in range(game_size):
      relation = relation + game_signs[i*2*game_size+j*2]
      relation2 = relation2 + game_signs[j*2*game_size+i*2+1]
    result.append(['row', str(i+1), relation[:-1], game_results[i]])
    result.append(['col', str(i+1), relation2[:-1], game_results[game_size+i]])
  
  variables = {}
  for i in range(game_size*game_size-1):
    row, col = divmod(i, game_size)
    row = row + 1
    col = col + 1
    var_name = construct_var_name(row, col)
    variables[var_name] = []
    for j in range(i+1, game_size*game_size):
      row, col = divmod(j, game_size)
      variables[var_name].append([construct_var_name(row+1, col+1), '!='])

  variables[construct_var_name(game_size, game_size)] = []
  return {'size': game_size, 'variables': variables, 'constraints': result}


def construct_var_name(row, col):
  """ Construct the variable name to represent a slot at the puzzle grid."""
  return 'var_' + str(row) + '_' + str(col)

def printGame(game_str):
  """ Print the board for a game according to the given game string."""
  
  index_pos = game_str.index('==')

  game_squares = game_str[:index_pos].replace('.', '▤').replace('+', ',').replace('-', ',').replace('*', ',').replace('/', ',').replace('=', ',').replace('^', ',').replace('<', ',').replace('>', ',').replace('^', ',').replace('v', ',').split(',')
  
  while '' in game_squares:
    game_squares.remove('')
  
  game_results = game_str[index_pos+2:].split(',')

  game_size = int(len(game_results) / 2)
  
  max_unit_width = len(str(len(game_results)))
    
  tmp_game_signs = game_str[:index_pos+2].replace('.', '').replace('*', '×').replace('/', '÷')
  for i in range(10):
    tmp_game_signs = tmp_game_signs.replace(str(i), '')
  dealt = 0
  r0 = ''
  
  bracket = False
  game_signs = []
  for i in tmp_game_signs:
    if i not in ['<', '>', '^', 'v']:
      game_signs.append(i)
    else:
      bracket = True

  for i in tmp_game_signs:
    
    if dealt % 2 == 0:
      x_pos, y_pos = divmod(int(dealt/2), game_size)
    else:
      x_pos, y_pos = divmod(int((dealt-1)/2), game_size)
    
    if i in ['<', '>', '^', 'v']:
      if i == '<':
        game_squares[x_pos * game_size + y_pos] = '<' + game_squares[x_pos * game_size + y_pos]
      elif i == '>':
        game_squares[x_pos * game_size + y_pos] = game_squares[x_pos * game_size + y_pos] + '>'
      elif i == 'v':
        game_signs[(x_pos * game_size + y_pos +1)*2-1] = game_signs[(x_pos * game_size + y_pos+1)*2-1] + 'v'
      elif i == '^':
        if x_pos == 0:
          r0 = r0 + ' ' * (max_unit_width * (y_pos + 1) + 3 * y_pos + 1) + '^'
        else:
          game_signs[((x_pos-1) * game_size + y_pos +1)*2-1] = game_signs[((x_pos-1) * game_size + y_pos +1)*2-1] + '^'
    else:
      dealt = dealt + 1
  r = ['' for i in range(game_size * 2)]
  for i in range(game_size*game_size):
    x_pos, y_pos = divmod(i+1, game_size)
    if y_pos == 0:
      x_pos = x_pos - 1  
    r[x_pos*2] = r[x_pos*2] + game_squares[i] + ' ' * (max_unit_width - len(game_squares[i]) + 2) + game_signs[i*2] + ' '
    if bracket == True:
      r[x_pos*2+1] = r[x_pos*2+1]
      space = ' ' * (max_unit_width - len(game_signs[i*2+1]) + 1)
    else:
      space = ' ' * max_unit_width
    r[x_pos*2+1] = r[x_pos*2+1] + game_signs[i*2+1]  + space + '   '
    if y_pos == 0:
      r[x_pos*2] = r[x_pos*2] + game_results[x_pos]
      if r0 != '':
        print(r0)
        r0 = ''
      
  for x in r:
    print(x)
  r1 = ''
  for i in range(game_size):
    if len(game_results[game_size+i]) < max_unit_width+3:
      space = ' ' * (max_unit_width+4-len(game_results[game_size+i]))
    else:
      space = ' '
    r1 = r1 + game_results[game_size+i] + space
  print(r1)


def solveByBT(game_str, v_binding_method = 'MRV+DH', inference_method = 'FC', preprocess_by_PC = True):
  """A Futoshiki solver calling Backtracking Search and use the constraints parsed by the function parseGame().
  Return a solution string if a solution is found; or None otherwise."""
  
  game_inform = parseGame(game_str)
  default_domain = [i for i in range(1, game_inform['size']*game_inform['size']+1)]
  
  bt_search = BT.BT()

  game_size = game_inform['size']
  # Set up Futoshiki game for Backtracking Search
  for i in game_inform['variables']:
    bt_search.set_domain(i, default_domain)
    for c in game_inform['variables'][i]:
      bt_search.set_binary_cons(i, c[0], eval('lambda x,y: x' + c[1] + 'y'))
    for c in game_inform['constraints']:
      var_names = []
      if c[0] == 'row':
        for j in range(1, game_size+1):
          var_names.append(construct_var_name(c[1], j))
      else:
        for j in range(1, game_size+1):
          var_names.append(construct_var_name(j, c[1]))
      equ = ''
      handled_num = 0
      bracket = False
      for j in range(len(c[2])):
        if c[2][j] == '(':
          equ = equ + c[2][j] + 'x[\'' + var_names[handled_num] + '\']'
          bracket = True
          handled_num = handled_num + 1
        elif c[2][j] == ')':
          equ = equ + ')'
        else:
          if bracket == True:
            equ = equ + c[2][j] + 'x[\'' + var_names[handled_num] + '\']'
          else:
            equ = equ + 'x[\'' + var_names[handled_num] + '\']' + c[2][j]
          handled_num = handled_num + 1
      if handled_num < game_size:
        equ = equ + 'x[\'' + var_names[handled_num] + '\']'
      equ = equ + '==' + c[3]
      bt_search.set_multinary_cons(var_names, eval('lambda x:' + equ))
  
  return bt_search.do_search(v_binding_method, inference_method, preprocess_by_PC)

def convert2str(game_str, variable_dict):
  if variable_dict:
    solution = ''
    rn = 0
    for i in game_str:
      if i == '.':
        x, y = divmod(rn, int(len(variable_dict)**0.5))
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
  print("\nThis is the library file of the part 2 that belong to the project of Comparison of Search Algorithms.\nThis file supplies an implement for Cross-Math game.\nThis file supplies three functions.\nThe function generateGame(size) could generate a solvable CrossMath game randomly in the format of string. Any game generated via this function has but not necessarily only has one solution.\nThe function parseGame(game_str) could return a list composed by constraints to each row and col according to the given string that represents a game.\nThe function printGame(game_str) could print the game board according to the given string that represent a game.\nAttention: No legality check to the input game_str in the latter two function (TODO maybe).\n")
  
  game_str, board_str = generateGame(random.randint(3, 4))
  
  print('You can try this:\n(or re-run this file to try another game that may have different size or/and difficulty)\n')
  printGame(game_str)

  input('\nPress \'enter\' or \'return\' to show the solution.')
 
  print('\nSolution:\n')
  
  printGame(board_str)
  
  print('\nThe above solution is obtained when generating the game.')
  print('The below solution is obtained via Backtracking Search.\n')
  
  printGame(convert2str(game_str, solveByBT(game_str)['solution']))
  
  print('\nGames generated here may have multiple solutions.\nHence, the above two solutions may be different.\n')
  
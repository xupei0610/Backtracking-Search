# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "15:37, Nov. 6th, 2015"
""" This is the library file of the part 2 that belong to the project of Comparison of Search Algorithms.
This file supplies a class PC() as the implement for modified AC3 who can work for path consistency as well.
PC() here is able to handle node, arc and path consistency."""


class PC():
  """The implement for AC3 + the support for path consistency."""
  def __init__(self):
    """ Initialize class variables for storing variables' names, domains, and unary and binary constraints."""
    # self.variables is a one-dimensional list to store variables' names.
    self.variables = []
    # self.var_domains is a dictionay to store variables' domains. It is formatted as {var_name:[value1, value2, ...], ...}.
    self.var_domains = {}
    # self.unary_cons is a dictionary to store the unary constraints. It is formatted as {var_name:[func1, func2,...], ...}. func is a function that could return true if a given value of the variable var_name is acceptable in respect to his unary constraint.
    self.unary_cons = {}
    # self.binary_cons is dictionary to store the binary constraints. It is formatted as {var_name1: [[var_name2, func1, non-inverse], [var_name3, func2, non-inverse]], ...}.
    self.binary_cons = {}
    # TODO in fact is doing.
    self.multinary_cons = {}
    
  def set_domain(self, var_name, domain):
    """Set the domain for the variable whose name is var_name.
    The input var_name is a string that represents the target variable's name.
    The input domain is a one-dimensional list that represents the domain of the variable whose name is var_name."""
    if var_name not in self.variables:
      self.variables.append(var_name)
    self.var_domains[var_name] = []
    for x in domain:
      if x not in self.var_domains[var_name]:
        self.var_domains[var_name].append(x)
    
  def unary_constraint(self, var_name, func):
    """Set a unary constraint for the variable whose name is var_name.
    The input var_name is a string that represents the target variable's name.
    The input func is function who will return true if a given value of the target variable satisfies the unary constraint for the target."""
    if var_name in self.unary_cons:
      self.unary_cons[var_name].append(func)
    else:
      self.unary_cons[var_name] = [func]
    
  def binary_constraint(self, target_var, related_var, func):
    """Set a binary constraint for the variable whose name is target_var and the variable whose name is related_var.
    The input target_var is a string that represents the target variable's name.
    The input related_var is a string that represents the related variable's name.
    The input func is function who will return true if a given value of the target variable satisfies the binary constraint with a given value of the related variable. Two constraints for target_var and related_var respectively will generated automatically each time this function is used.
    For example, when using PC.binary_constraint('V1', 'V2', lambda x,y: x>y), two constraints are defined.
    1. for V1, return True if V1>V2
    2. for V2, return True if V2>V1
    """
    if target_var in self.binary_cons:
      self.binary_cons[target_var].append([related_var, func, True])
    else:
      self.binary_cons[target_var] = [[related_var, func, True]]
    if related_var in self.binary_cons:
      self.binary_cons[related_var].append([target_var, func, False])
    else:
      self.binary_cons[related_var] = [[target_var, func, False]]
      
  def multinary_constraint(self, related_vars, func):
    """Set a multinary constraint for the variable whose name is target_var. This function also supports to binary constraint.
    The input argument related_vars is a list composed of related variables' names.
    The input argument func is a function who will return true if a given group of related_vars satisfies the constraint. The func has one input who is a dict in which the key name is same to the name of the variable the element represents.
    e.g. PC.multinary_constraint(['A1', 'A2'], lambda x: x['A1'] + x['A2'] == 1)"""
    related_vars = list(set(related_vars))
    for i in range(len(related_vars)):
      target_var = related_vars[i]
      other_vars = related_vars.copy()
      del other_vars[i]
      if target_var in self.multinary_cons:
        self.multinary_cons[target_var].append([other_vars, func])
      else:
        self.multinary_cons[target_var] = [[other_vars, func]]
      
  
  def node_consistency(self, var_name):
    """Revise the domain for the variable whose name is var_name according to its unary constraints.
    This function returns the number of values in the domain of the variable whose name is var_name, the values who are deleted for node consistency."""
    removed = 0
    if var_name in self.unary_cons:
      for func in self.unary_cons[var_name]:
        for i in range(len(self.var_domains[var_name])):
          if func(self.var_domains[var_name][i-removed]):
            continue
          else:
            del self.var_domains[var_name][i-removed]
            removed = removed + 1
    return removed

  def arc_reduce(self, var_name):
    """Revise the domain for the variable whose name is var_name according to its binary constraints.
    This function returns the number of values in the domain of the variable whose name is var_name, the values who are deleted for arc consistency."""
    if var_name not in self.binary_cons:
      return 0
    total_removed = 0
    for con in self.binary_cons[var_name]:
      var2 = con[0]
      func = con[1]
      removed = 0
      iter_range = range(len(self.var_domains[var_name]))
      for i in iter_range:
        revise = True
        x = self.var_domains[var_name][i-removed]
        for y in self.var_domains[var2]:
          if con[2] == True:
            res = func(x, y)
          else:
            res = func(y, x)
          if res:
            revise = False
            break
        if revise == True:
          del self.var_domains[var_name][i-removed]
          removed = removed + 1
      total_removed = total_removed + removed
    return total_removed

  
  def path_consistency(self, var_name):
    """Revise the domain for the variable whose name is var_name according to its multinary constraints.
    This function returns the number of values in the domain of the variable whose name is var_name, the values who are deleted for path consistency."""
    from functools import reduce 
    if var_name not in self.multinary_cons:
      return 0
    total_removed = 0
    for con in self.multinary_cons[var_name]:
      # Obtain all possible combination of other related variables' value as the second input argument
      values = [self.var_domains[v] for v in con[0]]
      if values == []:
        ys=[{}]
      else:
        total = reduce(lambda x, y: x*y, map(len, values))
        ys = []
        for i in range(total):
          s = total
          tmp = []
          for v in values:
            s = s / len(v)
            tmp.append(v[int(i/s) % len(v)])
          ys.append(dict(zip(con[0], tmp)))
      func = con[1]
      removed = 0
      iter_range = range(len(self.var_domains[var_name]))
      for i in iter_range:
        revise = True
        x = self.var_domains[var_name][i-removed]
        for y in ys:
          y[var_name] = x
          res = func(y)
          if res:
            revise = False
            break
        if revise == True:
          del self.var_domains[var_name][i-removed]
          removed = removed + 1
      total_removed = total_removed + removed
    return total_removed
    
  def do_PC(self):
    """The implement for this modified AC3. Return False if any variable's domain has no value left; True otherwise.
    Variables' names, domains and constraints should be defined firstly, before using this function."""

    remaining_val = {}
    for var in self.variables:
      # Remove repeated elements in a variable's domain
      remaining_val[var] = len(self.var_domains[var])

    # Maintain node consistency
    for var in self.variables:
      removed = self.node_consistency(var)
      remaining_val[var] = remaining_val[var]-removed
      if remaining_val[var] == 0:
        return False
    # Repeatedly call self.arc_reduce() until any variable's domain is empty (False will be returned) or all variables' domains cannot be revised by that function (True will be returned).
    flag = True
    while(flag):
      flag = False
      # Maintain arc consistency
      for var in self.variables:
        removed = self.arc_reduce(var) + self.path_consistency(var)
        if removed > 0:
          flag = True
        remaining_val[var] = remaining_val[var]-removed
        if remaining_val[var] == 0: # No possiblity to be smaller than 0, since no bug in the program. ^.^
          return False
    return True
    

if __name__ == "__main__":
  import time
  print(__file__)
  print('Author: %s'%__author__)
  print('Copyright: %s'%__copyright__)
  print('License: %s'%__license__)
  print('Version: %s'%__version__)
  print("This is the library file of the part 2 that belong to the project of Comparison of Search Algorithms.\nThis file supplies a class PC() as the implement for a modified AC3 who can work for path consistency as well.\nPC() here is able to handle node, arc and path consistency.")
  
  print('\n\nA simple unit test will run in 2 second.\n')
  
  time.sleep(2)
  
  # Test for assigning the domain for a variable
  pc = PC()
  pc.set_domain('V1', [1, 2, 3])
  assert pc.variables == ['V1']
  assert pc.var_domains == {'V1':[1, 2, 3]}
  pc.set_domain('V2', [2, 3, 4])
  assert 'V2' in pc.variables
  assert pc.var_domains['V2'] == [2, 3, 4]
  print('Pass the test for assigning the domain for a variable for the class PC().')
  
  # Test for setting unary constraints for a variable
  pc = PC()
  pc.set_domain('V1', [1, 2, 3])
  pc.unary_constraint('V1', lambda x: x >= 2)
  pc.unary_constraint('V1', lambda x: x < 3)
  pc.node_consistency('V1')
  assert pc.var_domains['V1'] == [2]
  print('Pass the test for setting unary constraints for a variable for the class PC().')
  
  # Test for setting a binary constraint for a variable
  pc = PC()
  pc.set_domain('V1', [1, 2, 3])
  pc.set_domain('V2', [2, 3, 4])
  # V1's value must be greater than V2's value
  pc.binary_constraint('V1', 'V2', lambda x,y: x>y)
  pc.arc_reduce('V1')
  assert pc.var_domains['V1'] == [3]
  # V2's binary constraint related to V1 should be generated automatically,
  pc.arc_reduce('V2')
  assert pc.var_domains['V2'] == [2]
  print('Pass the test for setting a binary constraint for a variable for the class PC().')
  
  # Test for setting two binary constraints for a variable
  pc = PC()
  pc.set_domain('V1', [1, 2, 3])
  pc.set_domain('V2', [2, 3, 4])
  pc.set_domain('V3', [1, 2, 3])
  pc.binary_constraint('V3', 'V2', lambda x,y: x>y)
  pc.binary_constraint('V3', 'V1', lambda x,y: x==y)
  pc.arc_reduce('V1')
  pc.arc_reduce('V2')
  pc.arc_reduce('V3')
  assert pc.var_domains['V1'] == [1, 2, 3]
  assert pc.var_domains['V2'] == [2]
  assert pc.var_domains['V3'] == [3]
  
  pc = PC()
  pc.set_domain('V1', [1, 2, 3])
  pc.set_domain('V2', [2, 3, 4])
  pc.set_domain('V3', [1, 2, 3])
  pc.binary_constraint('V3', 'V2', lambda x,y: x>y)
  pc.binary_constraint('V3', 'V1', lambda x,y: x==y)
  pc.arc_reduce('V3')
  pc.arc_reduce('V2')
  pc.arc_reduce('V1')
  assert pc.var_domains['V1'] == [3]
  assert pc.var_domains['V2'] == [2]
  assert pc.var_domains['V3'] == [3]
  
  print('Pass the test for setting two binary constraints for a variable for the class PC().')
  
  # The order of using PC.arc_reduce would result to different results, but the final and optimal results will be obtained through using PC.do_PC() although it reduces arc for the variable who is defined firstly
  pc = PC()
  pc.set_domain('V1', [1, 2, 3])
  pc.set_domain('V2', [2, 3, 4])
  pc.set_domain('V3', [1, 2, 3])
  pc.binary_constraint('V3', 'V2', lambda x,y: x>y)
  pc.binary_constraint('V3', 'V1', lambda x,y: x==y)
  res = pc.do_PC()
  assert pc.var_domains['V1'] == [3]
  assert pc.var_domains['V2'] == [2]
  assert pc.var_domains['V3'] == [3]
  assert res == True
  print('Pass the test for successfully implementing AC3 via the class PC(). (Any variable\'s domain cannot be reduced via AC3 supported by PC())')
  
  # False will be returned if any varialbe's domain has no element
  pc = PC()
  pc.set_domain('V1', [1, 2, 3])
  pc.set_domain('V2', [2, 3, 4])
  pc.set_domain('V3', [1, 2, 3])
  pc.binary_constraint('V3', 'V2', lambda x,y: x>y)
  pc.binary_constraint('V3', 'V1', lambda x,y: x==y)
  pc.unary_constraint('V1', lambda x: x != 3)
  res = pc.do_PC()
  assert res == False
  print('Pass the test for unsuccessfully implementing AC3 via the class PC(). (Any variable\'s domain has no element.)')
  
  # A test using KenKen example  
  pc = PC()
  for i in ['A', 'B', 'C']:
    for j in ['1', '2', '3']:
      pc.set_domain(i+j, [1, 2, 3])
  pc.binary_constraint('A1', 'A2', lambda x,y: x!=y)
  pc.binary_constraint('A1', 'A3', lambda x,y: x!=y)
  pc.binary_constraint('A2', 'A3', lambda x,y: x!=y)
  pc.binary_constraint('B1', 'B2', lambda x,y: x!=y)
  pc.binary_constraint('B1', 'B3', lambda x,y: x!=y)
  pc.binary_constraint('B2', 'B3', lambda x,y: x!=y)
  pc.binary_constraint('C1', 'C2', lambda x,y: x!=y)
  pc.binary_constraint('C1', 'C3', lambda x,y: x!=y)
  pc.binary_constraint('C2', 'C3', lambda x,y: x!=y)
  pc.binary_constraint('A1', 'B1', lambda x,y: x!=y)
  pc.binary_constraint('A1', 'C1', lambda x,y: x!=y)
  pc.binary_constraint('B1', 'C1', lambda x,y: x!=y)
  pc.binary_constraint('A2', 'B2', lambda x,y: x!=y)
  pc.binary_constraint('A2', 'C2', lambda x,y: x!=y)
  pc.binary_constraint('B2', 'C2', lambda x,y: x!=y)
  pc.binary_constraint('A3', 'B3', lambda x,y: x!=y)
  pc.binary_constraint('A3', 'C3', lambda x,y: x!=y)
  pc.binary_constraint('B3', 'C3', lambda x,y: x!=y)
  
  pc.unary_constraint('A3', lambda x: x==2)
  pc.binary_constraint('A1', 'A2', lambda x,y: abs(x-y) == 2)
  pc.binary_constraint('B1', 'C1', lambda x,y: x/y == 2 or y/x == 2)
  pc.binary_constraint('B2', 'B3', lambda x,y: x/y == 3 or y/x == 3)
  pc.binary_constraint('C2', 'C3', lambda x,y: abs(x-y) == 1)
  
  pc.do_PC()

  assert pc.var_domains['A1'] == [3]
  assert pc.var_domains['A2'] == [1]
  assert pc.var_domains['A3'] == [2]
  assert pc.var_domains['B1'] == [2]
  assert pc.var_domains['B2'] == [3]
  assert pc.var_domains['B3'] == [1]
  assert pc.var_domains['C1'] == [1]
  assert pc.var_domains['C2'] == [2]
  assert pc.var_domains['C3'] == [3]
  
  print('Pass the test for solving the example Kenken game via the class PC()')
  
  pc = PC()
  pc.set_domain('V1', [1, 5, 8])
  pc.set_domain('V2', [2, 6, 9])
  pc.set_domain('V3', [3, 7, 10])
  pc.set_domain('V4', [4, 9, 11])
  pc.multinary_constraint('V1', ['V2', 'V3', 'V4'], lambda x,y: x + y[0] + y[1] + y[2] == 10)
  pc.multinary_constraint('V2', ['V1', 'V3', 'V4'], lambda x,y: y[0] + x + y[1] + y[2] == 10)
  pc.multinary_constraint('V3', ['V1', 'V2', 'V4'], lambda x,y: y[0] + y[1] + x + y[2] == 10)
  pc.multinary_constraint('V4', ['V1', 'V2', 'V3'], lambda x,y: y[0] + y[1] + y[2] + x == 10)
  pc.do_PC()
  
  assert pc.var_domains['V1'] == [1]
  assert pc.var_domains['V2'] == [2]
  assert pc.var_domains['V3'] == [3]
  assert pc.var_domains['V4'] == [4]
  
  print('Pass the test for path consistency via the class PC().')
  
  print('\nCongratulations!!!\nAll tests have been passed.')


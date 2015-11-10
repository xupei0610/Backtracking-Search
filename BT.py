# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "20:50, Nov. 6th, 2015"
""" This is the library file of the part 2 that belong to the project of Comparison of Search Algorithms.
This file supplies a class BT() as the implement for backtracking search for CSP."""

import random, time
from PC import *

class BT():
  """ This is an implement for Backtracking Search."""
  
  def __init__(self):
    self.assignment = {}
    self._bt_variables = {}
    self._bt_unary_cons = []
    self._bt_binary_cons = []
    self._bt_multinary_cons = []
    self._bt_pc = PC()
    self._assign_var_times = 0
    #self._infer_times = 0 # This should be always equal to the above, so no meaning here.
    self._find_unassigned_var_times = 0
    self._start_time = 0
  
  def set_domain(self, var_name, domain):
    """ Set the domain for the variable whose name is var_name."""
    if ~isinstance(domain, list):
      domain = list(domain)
    self._bt_variables[var_name] = domain
  
  def set_unary_cons(self, var_name, func):
    """ Set a unary constraint for the variable whose name is var_name."""
    self._bt_unary_cons.append([var_name, func])

  def set_binary_cons(self, var_name1, var_name2, func):
    """ Set a binary constraint for the variable whose name is var_name1 and the variable whose name is var_name2. A pair of constraint will be generated every time the function is called."""
    self._bt_binary_cons.append([var_name1, var_name2, func])

  def set_multinary_cons(self, related_vars, func):
    """ Set a multinary constraint for the variables in the related_vars list. The function also supports to binary constraints.
    The input argument func is a function who will return true if a given group of related_vars satisfies the constraint. The func has one input who is a dict in which the key name is same to the name of the variable the element represents.
    e.g. BT.set_multinary_cons(['A1', 'A2'], lambda x: x['A1'] + x['A2'] == 1)"""
    self._bt_multinary_cons.append([related_vars, func])
    
  
  def _complete(self):
    """ Return True if all variables' domains only have 1 acceptable element."""
    for var in self.assignment:
      if isinstance(self.assignment[var], list):
        if len(self.assignment[var]) == 1:
          self._bt_pc.set_domain(var, self.assignment[var])
        else:
          return False
      else:
        self._bt_pc.set_domain(var, [self.assignment[var]])
    return self._bt_pc.do_PC()
  
  def complete(self):
    """This function can be rewrite according to situation for some hard situation where the correctness of solutions cannot be determined just via PC."""
    return self._complete()
    
  def _find_unassigned_variable(self, method):
    """ Return the name of an unassigned variable.
    The unassigned variable is selected via random if the input method == 'random' or MRV (+ degree heuristic if possible) if the input method == 'MRV'."""
    if method == 'random':
      unassigned = []
      for var in self.assignment:
        if isinstance(self.assignment[var], list):
          unassigned.append(var)
      if unassigned != []:
        return random.choice(unassigned)
      else:
        return None
      
    elif method == 'MRV':
      target = []
      for var in self.assignment:
        if isinstance(self.assignment[var], list):
          remaining_values = len(self.assignment[var])
          if 'minimum_remaining_values' not in locals() or remaining_values < minimum_remaining_values:
            minimum_remaining_values = remaining_values
            target = [var]
          elif 'minimum_remaining_values' in locals() and remaining_values == minimum_remaining_values:
            target.append(var)
      if target:
        return random.choice(target)
      else:
        return None
  
    elif method == 'DH':
      target = []
      for var in self.assignment:
        if isinstance(self.assignment[var], list):
          checked = []
          degree = 0
          if var in self._bt_pc.binary_cons:
            for con in self._bt_pc.binary_cons[var]:
              if con[0] not in checked and con[0] in self.assignment and isinstance(self.assignment[con[0]], list):
                degree = degree + 1
                checked.append(con[0])
          if var in self._bt_pc.multinary_cons:
            for con in self._bt_pc.multinary_cons[var]:
              for v in con[0]:
                if v not in checked and v in self.assignment and isinstance(self.assignment[v], list):
                  degree = degree + 1
                  checked.append(v)
          if 'max_degree' not in locals() or degree > max_degree:
            max_degree = degree
            target = [var]
          elif 'max_degree' in locals() and degree == max_degree:
            target.append(var)
      if target:
        return random.choice(target)
      else:
        return None

    elif method == 'MRV+DH':
      # Select via MRV firstly
      target = []
      for var in self.assignment:
        if isinstance(self.assignment[var], list):
          remaining_values = len(self.assignment[var])
          if 'minimum_remaining_values' not in locals() or remaining_values < minimum_remaining_values:
            minimum_remaining_values = remaining_values
            target = [var]
          elif 'minimum_remaining_values' in locals() and remaining_values == minimum_remaining_values:
            target.append(var)
      if len(target) == 1:
        return target[0]
      elif len(target) == 0:
        return None
      # Select via degree heuristic
      real_target = []
      for var in target:
        if isinstance(self.assignment[var], list):
          checked = []
          degree = 0
          if var in self._bt_pc.binary_cons:
            for con in self._bt_pc.binary_cons[var]:
              if con[0] not in checked and con[0] in self.assignment and isinstance(self.assignment[con[0]], list):
                degree = degree + 1
                checked.append(con[0])
          if var in self._bt_pc.multinary_cons:
            for con in self._bt_pc.multinary_cons[var]:
              for v in con[0]:
                if v not in checked and v in self.assignment and isinstance(self.assignment[v], list):
                  degree = degree + 1
                  checked.append(v)
            if 'max_degree' not in locals() or degree > max_degree:
              max_degree = degree
              real_target = [var]
            elif 'max_degree' in locals() and degree == max_degree:
              real_target.append(var)
      
      if real_target:
        return random.choice(real_target)
      else:
        return random.choice(target)
    else:
      return False

  def _inference(self, current_var, method):
    """ Return the result of inference via the given method.
    Any of the method 'FC' for forward checking and 'MAC' for maintaining arc consistency is supported."""
    if method == 'FC':
      result = {}
      for var in self.assignment:
        if isinstance(self.assignment[var], list):
          self._bt_pc.set_domain(var, self.assignment[var].copy())
        else:
          self._bt_pc.set_domain(var, [self.assignment[var]].copy())
      if current_var in self._bt_pc.unary_cons:
        for con in self._bt_pc.unary_cons[current_var]:
          if isinstance(self.assignment[current_var], list):
            self._bt_pc.node_consistency(current_var)
            result[current_var] = self._bt_pc.var_domains[current_var].copy()
            if len(result[con[0]]) == 0:
              return False
      if current_var in self._bt_pc.binary_cons:
        for con in self._bt_pc.binary_cons[current_var]:
          if isinstance(self.assignment[con[0]], list):
            self._bt_pc.arc_reduce(con[0])
            result[con[0]] = self._bt_pc.var_domains[con[0]].copy()
            if len(result[con[0]]) == 0:
              return False
      if current_var in self._bt_pc.multinary_cons:
        for con in self._bt_pc.multinary_cons[current_var]:
          for c in con[0]:
            if isinstance(self.assignment[c], list):
              self._bt_pc.path_consistency(c)
              if c in self._bt_pc.unary_cons:
                self._bt_pc.node_consistency(c)
              if c in self._bt_pc.binary_cons:
                self._bt_pc.arc_reduce(c)
              result[c] = self._bt_pc.var_domains[c].copy()
              if len(result[c]) == 0:
                return False
      return result

    elif method == 'MAC':
      result = {}
      for var in self.assignment:
        if isinstance(self.assignment[var], list):
          self._bt_pc.set_domain(var, self.assignment[var].copy())
        else:
          self._bt_pc.set_domain(var, [self.assignment[var]].copy())
      res = self._bt_pc.do_PC()  
      if res == False:
        return False
      for var in self._bt_pc.var_domains:
        if isinstance(self.assignment[var], list):
          result[var] = self._bt_pc.var_domains[var]
      return result

    else:
      return False
  
  def do_search(self, v_binding_method = 'MRV+DH', inference_method = 'MAC', preprocess_by_PC = True):
    """The implement for Backtracking search.
    Return a dict {'solution': solution, ...} where the solution is formatted as {var_name:[val1, val2,...], ...} and other information is just used to record the search's performance; or return false if no solution is found.
    The input variable v_binding_method is the way through which Backtracking Search decides which variable should be assigned next time. It may be any of 'random' or 'MRV'.
    The input variable inference_method is the way through which Backtracking Search establishes consistency after a value is assigned to a variable. It may be any of 'FC' or 'MAC'.
    The input variable preceded_by_PC decides if PC (AC3 + PATH CONSISTENCY) will be processed before backtracking search."""
    # Initialize statistical information
    self._assign_var_times = 0
    self._find_unassigned_var_times = 0
    self._start_time = time.time()
    
    # Put constraints into PC
    for c in self._bt_unary_cons:
      self._bt_pc.unary_constraint(c[0], c[1])
    for c in self._bt_binary_cons:
      self._bt_pc.binary_constraint(c[0], c[1], c[2])
    for c in self._bt_multinary_cons:
      self._bt_pc.multinary_constraint(c[0], c[1])
    
    # Preprocess by PC
    if preprocess_by_PC == True:
      for var in self._bt_variables:
        self._bt_pc.set_domain(var, self._bt_variables[var])
      if self._bt_pc.do_PC():
        self._bt_variables = self._bt_pc.var_domains.copy()
      else:
        return False
      
    # Initialize assignment list
    self.assignment = self._bt_variables.copy()
    
    # Begin Search
    return self._bt_search(v_binding_method, inference_method)

  def _bt_search(self, v_binding_method, inference_method):
    """ This is the real function for Backtracking Search"""

    if self.complete():
      for var in self.assignment:
        if isinstance(self.assignment[var], list):
          self.assignment[var] = self.assignment[var][0]
      return {'solution': self.assignment, 'assignVarTimes': self._assign_var_times, 'findUnassignedVarTimes': self._find_unassigned_var_times, 'runningTime': time.time() - self._start_time} #'InferTimes': self._infer_times, 

    var = self._find_unassigned_variable(v_binding_method)
    self._find_unassigned_var_times = self._find_unassigned_var_times + 1
    if var:    
      remaining_values = self.assignment[var].copy()
    else:
      return False

    for v in remaining_values:
      self._assign_var_times = self._assign_var_times + 1
      self.assignment[var] = v
      infer = self._inference(var, inference_method)
      # self._infer_times = self._infer_times + 1
      if infer != False:
        assignment_old = self.assignment.copy()
        self.assignment.update(infer)
        result = self._bt_search(v_binding_method, inference_method)
        if result != False:
          return result
        self.assignment = assignment_old.copy()
        self.assignment[var] = []
  
    return False

      
      
if __name__ == "__main__":
  print(__file__)
  print('Author: %s'%__author__)
  print('Copyright: %s'%__copyright__)
  print('License: %s'%__license__)
  print('Version: %s'%__version__)
  print("This is the library file of the part 2 that belong to the project of Comparison of Search Algorithms.\nThis file supplies a class BT() as the implement for backtracking search for CSP.")
          
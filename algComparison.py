# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "19:31, Nov. 8th, 2015"
""" This is the testing and main program for the Part 2 of the project of Comparison of Search Algorithms.
Futoshiki games are generated and solved via Backtracking Search for comparison of random vs MRV using MAC.
MathCross games are generated and solved via Backtracking Search for comparison of Forwarding-Checking vs MAC using MRV.
As the additional work, Sudoku games are generated and solved via Backtracking Search for comparing the difference in performance between doing preprocess via AC3 and not doing preprocess via AC3. Backtracking search using MRV and MAC is employed for this test case."""

import time, logging, sys, getopt, os
from threading import Thread

import Futoshiki, CrossMath, Sudoku

def main(argv):
  try:
    opts, args = getopt.getopt(argv[1:], 'hvt:c:s:af:o:', ['help', 'version', 'test=', 'cases=', 'size=', 'analyze', 'file=', 'timeout='])
  except getopt.GetoptError as err:
    print(str(err))
    usage()
    sys.exit(2)
  
  do_test = False
  do_analysis = False
  supported_events = 'FCS'
  sample_log = 'p2test.sample.log'
  
  default_events = 'FCS'
  default_cases = 30
  default_size = {'F':6, 'C':3, 'S':9}
  default_time_out = 120
  
  cases = 0
  size = []
  log_file = None
  time_out = 120

  for o, a in opts:
    if o in ('-h', '--help'):
      usage()
      sys.exit()
    elif o in ('-v', '--version'):
      version()
      sys.exit()
    elif o in ('-t', '--test'):
      do_test = True
      events = ''
      for i in str(a):
        if i in supported_events:
          events = events + i
    elif o in ('-c', '--cases'):
      cases = int(a)
    elif o in ('-s', '--size'):
      size = list(str(a).split(','))
    elif o in ('-a', '--analyze'):
      do_analysis = True
    elif o in ('-f', '--file'):
      log_file = a
    elif o in ('-o', '--timeout'):
      time_out = int(a)
  
  if do_test == True:
    if events == '':
      events = default_events
    if cases < 1:
      cases = default_cases
    if len(size) == len(events):
      size = [int(i) for i in size]
      for i in size:
        if isinstance(i, int) and i > 0:
          continue
        else:
          size = []
          break
    if size == []:
      for e in events:
        size.append(default_size[e])
    if 'S' in events and size[events.index('S')]**0.5 != int(size[events.index('S')]**0.5):
      size[events.index('S')] == default_size['S']
    if log_file == '':
      log_file = None
    if time_out < 1:
      time_out = default_time_out
    log_file = test(events = events, size = size, cases = cases, log_file = log_file, time_out = time_out)
  
  if do_analysis == True:
    if log_file == None:
      if do_test == True:
        sys.exit()
      else:
        log_file = sample_log
    analyze(log_file)
    sys.exit()
  
  if do_test == False and do_analysis == False:
    usage()
    sys.exit()
    
def usage():
  print(__file__ + ' - the testing program for the Part 2 of the project Comparison of Search Algorithms.')
  print('Author: %s'%__author__)
  print('Copyright: %s'%__copyright__)
  print('License: %s'%__license__)
  print('\nThis program will use Futoshiki puzzles to test Backtracking Search using MAC and random order or MRV, or use CrossMath puzzles to test Backtracking using MRV and MAC or Forward Checking. As additional work, Sudoku puzzles will be utilized for comparison the difference in performance when AC3 is employed before search or not.')
  print('During testing, a log file will be generated. Please give enough permissions to this file before doing testing.')
  print('The file sptest.sample.log attached with this file is a sample log generated during a test conducted on Nov.9th. It can be used to analyze, and demonstrate 3 basic conclusions we expect to reach via the test.')
  
  print('\n3 conclusions we expect to reach:')
  print("  1: For Futoshiki puzzles, MRV will lead to an increase in the performance of Backtracking Search compared to random order of binding variables.")
  print("  2: For CrossMath puzzles, MAC will lead to an increase in the performance of Backtracking Search compared to Forward Checking.")
  print("  3: For Sudoku puzzles, the preprocess employing AC3 will lead to an increase in the performance of Backtracking Search.") 
   
  print('\nMetrics:')
  print('  1. The amount of times a search algorithm assigns a value to any variable during solving a puzzle.')
  print('  2. The amount of times a search algorithm does inference.')
  print('  3. The amount of times a search algorithm finds an unassigned variable.')
  print('  4. The running time for solving a puzzle will be record and used for comparison of these algorithms\' overall time complexity.')

  print('\nUsage of this file:')
  print('  -h, --help: show this help information.\n')
  print('  -v, --version: show the current version of this file and the library files it uses.\n')
  print('  -t, --test: the type of experiment, a combination string of F, C and S. Default value is FCS. F for Futoshiki, C for CrossMath and S for sudoku.\n')
  print('  -c, --cases: the amount of testing cases for each puzzle. Default value is 30.\n')
  print('  -s, --size: the size of testing puzzles. It can be a combination of numbers split by \',\', the numbers which respectively represents the size for a puzzle in the assigned string to the input experiment. 3 for 3x3, 4 for 4x4 and the like. For Sudoku, it should be a square number (see the doc for Sudoku.py for details).\n Advised size is 6 for Futoshiki, 3 for CrossMath and 9 for Sudoku. This is also the default size if no argument for s is input.')
  print('  -a, --analyze: analyze the log file generated during testing. \n    e.g. \'' +__file__+ ' -e FCS -s 6,3,9 -a\' will do tests firstly and then analyze the testing results.\n    Or e.g.\'' +__file__+ ' -a -f p2test.sample.log\' will analyze the given log file to prove the conclusions we expect to reach in this test.\n    Or e.g.\'' +__file__+ ' -a\' will analyze the default log file to prove the conclusions we expect to reach in this test.\n ')
  print('  -f, --file: the log file used for analyze (Default value is sptest.sample.log.); or the file name used for the log file generated by the testing program.\n')
  print('  -o, --timeout: the maximum time permitted for an algorithm to solve a puzzle. Default value is 120, namely 2 mins.')
  print("")


def version():
  print('%s \tv%s \t%s' % (__file__, __version__, __date__))
  print('%s \t\tv%s \t%s' % (os.path.split(AC3.__file__)[1], AC3.__version__, AC3.__date__))
  print('%s \t\tv%s \t%s' % (os.path.split(BT.__file__)[1], BT.__version__, BT.__date__))
  print('%s \tv%s \t%s' % (os.path.split(Futoshiki.__file__)[1], Futoshiki.__version__, Futoshiki.__date__))
  print('%s \tv%s \t%s' % (os.path.split(CrossMath.__file__)[1], CrossMath.__version__, CrossMath.__date__))
  print('%s \tv%s \t%s' % (os.path.split(Sudoku.__file__)[1], Sudoku.__version__, Sudoku.__date__))


def test(events, size, cases, log_file, time_out):
  """ Doing test according to the given events, game size and amount of testing cases, and generate a log file named log_file.
  A algorithm will stop if it runs time out according to the input time_out.
  Return the name of the log file generated.
  Return None if test fails."""
  
  # Log File's name
  if log_file == None:
    log_file = 'p2test %s.log'%(time.strftime("%H.%M.%S %F", time.localtime()))
  else:
    log_file = str(log_file)

  if os.path.exists(log_file):
    print('A file whose name is the same to the log file prepared to generate has existed !!!')
    return None

  # List testing information
  test_events = {}
  for i in range(len(events)):
    if events[i] == 'F':
      test_events['Futoshiki'] = size[i]
    elif events[i] == 'C':
      test_events['CrossMath'] = size[i]
    elif events[i] == 'S':
      test_events['Sudoku'] = size[i]

  print('Preparing testing...')
  print('The event of testing cases: %s' % ', '.join(test_events))
  print('The game size of sliding puzzle: %s' % ', '.join([str(i) + 'x' + str(i) for i in size]))
  print('The amount of testing cases: %d' % cases)
  print('The log file will be generated: %s' % log_file)
  print('The maximum time permitted for an algorithm to solve a puzzle: %ds' % time_out)
  
  # Using logger to recod testing results
  logger = logging.getLogger('p2test')
  logger.setLevel(logging.DEBUG)
  wh = logging.FileHandler(log_file)
  wh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
  ch = logging.StreamHandler()
  ch.setFormatter(logging.Formatter('%(message)s'))
  logger.addHandler(wh)
  logger.addHandler(ch)

  # Decorator function used to generate logger and limit the solver's running time.
  total_run_time = [0]
  time_out_cases = [0]
  def testingDecorator(time_out, total_run_time, time_out_cases):
    def decorator(func):
      def nfunc(*args, **args2):
        class TimeOut(Thread):
          def __init__(self, _error = None):
            Thread.__init__(self)
            self._error = _error
          def run(self):
            try:
              self.result = func(*args, **args2)
            except Exception as e:
              self._error = e
          def stop(self):
            if self.is_alive():
              self.stopped = True
        th = TimeOut()
        th.setDaemon(True)
        th.start()
        th.join(time_out)
        if th.is_alive(): # timeout
          th.stop()
          result = {'solution': False, 'assignVarTimes': 0, 'findUnassignedVarTimes': 0, 'runningTime': time_out}
          time_out_cases[0] = time_out_cases[0] + 1
          run_time_out = True
        else:
          run_time_out = False
          result = th.result
        if th._error is None:
          total_run_time[0] = total_run_time[0] + result['runningTime']
          logger = logging.getLogger('p2test')
          logger.info('Puzzle: %s - VarBindMethod: %s - InferMethod: %s - PreprocessedViaPC: %d - AssignVarTimes: %d - findUnassignedVarTimes: %d - TimeTaken: %f - TimeOut - %d' % (current_puzzle, args[1], args[2], int(args[3]), result['assignVarTimes'], result['findUnassignedVarTimes'], result['runningTime'], int(run_time_out)))
          return result
        else:
          raise Exception(th._error)
      return nfunc
    return decorator

  if 'Futoshiki' in test_events:
    @testingDecorator(time_out, total_run_time, time_out_cases)
    def FutoshikiSearchTest(*args):
      return Futoshiki.solveByBT(*args)
  if 'CrossMath' in test_events:
    @testingDecorator(time_out, total_run_time, time_out_cases)
    def CrossMathSearchTest(*args):
      return CrossMath.solveByBT(*args)
  if 'Sudoku' in test_events:
    @testingDecorator(time_out, total_run_time, time_out_cases)
    def SudokuSearchTest(*args):
      return Sudoku.solveByBT(*args)
    
  # Begin Testing
  print("\nTest begins...")
  total_cases = 0
  total_tests = 0
  if 'Futoshiki' in test_events:
    # For Futoshiki, we compare random vs MRV vs DH vs MRV+DH and use MAC as the inference method and preprocess via AC3 and PC1
    current_puzzle = 'Futoshiki'
    for i in range(cases):
      # Sometimes, it may fail generating game due to too many recrusives.
      while(True):
        try:
          game_str = Futoshiki.generateGame(test_events['Futoshiki'])[0]
          break
        except Exception as err:
          continue

      logger.info('Test Case %d. Puzzle Type: %s. Size: %dx%d. Puzzle State: %s' % (i+1, current_puzzle, test_events[current_puzzle], test_events[current_puzzle], game_str))

      for bm in ['random', 'MRV', 'DH', 'MRV+DH']:
        FutoshikiSearchTest(game_str, bm, 'MAC', True)
        total_tests = total_tests + 1

      total_cases = total_cases + 1

  if 'CrossMath' in test_events:
    # For CrossMath, we compare MAC vs FC and use MRV + DegreeHeuristic as the order method and preprocess via AC3 and PC1
    current_puzzle = 'CrossMath'
    for i in range(cases):
      # Sometimes, it may fail generating game due to too many recrusives.
      while(True):
        try:
          game_str = CrossMath.generateGame(test_events['CrossMath'])[0]
          break
        except Exception as err:
          continue

      logger.info('Test Case %d. Puzzle Type: %s. Size: %dx%d. Puzzle State: %s' % (i+1, current_puzzle, test_events[current_puzzle], test_events[current_puzzle], game_str))

      for im in ['MAC', 'FC']:
        CrossMathSearchTest(game_str, 'MRV+DH', im, True)
        total_tests = total_tests + 1

      total_cases = total_cases + 1
      
  if 'Sudoku' in test_events:
    # For Sudoku, we compare the performance of backtracking serch preprossed via AC3 and PC1 to that not preprossed. MAC is used as the inference method and MRV + DegreeHeuristic is used as the variable binding method.
    current_puzzle = 'Sudoku'
    for i in range(cases):
      # Sometimes, it may fail generating game due to too many recrusives.
      while(True):
        try:
          game_str = Sudoku.generateGame(test_events['Sudoku'])[0]
          break
        except Exception as err:
          continue

      logger.info('Test Case %d. Puzzle Type: %s. Size: %dx%d. Puzzle State: %s' % (i+1, current_puzzle, test_events[current_puzzle], test_events[current_puzzle], game_str))

      for pre in [True, False]:
        SudokuSearchTest(game_str, 'MRV+DH', 'MAC', pre)
        total_tests = total_tests + 1

      total_cases = total_cases + 1

  # Test ends
  print("\n%d cases and %d tests have been processed.\n%d of them run time out.\nTotal Time Taken: %fs\nLogger File Generated: %s"%(total_cases, total_tests, time_out_cases[0], total_run_time[0], log_file))

def analyze(log_file):
  print("========================= Analysis =============================\n")
  print('The Function will be completed soon for writing the Part 2 daft.')

if __name__ == '__main__':
  main(sys.argv)

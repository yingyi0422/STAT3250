##
## File: week08.py (STAT 3250)
## Topic: Common errors discovered by the autograder
## 

## General suggestions for avoiding autograder problems
##
## 1. Restart the kernel (under "Consoles" menu) and then run
##    your code line by line to be sure that no coding errors
##    are present.
##
## 2. Never use q1, q2, ... (and similar) as variables!
##
## 3. Double check to be sure that the thing you are assigning to 
##    q1, q2, ... is what you want.
##
## 4. Be sure that the data type matches what is specified.  In the 
##    case where a value is called for -- for instance, a count or
##    a percentage -- be sure that only the value is being passed
##    to the autograder.  For instance, don't submit a Series with
##    the required value as the Series value, it will be marked
##    incorrect. (This is important for these kinds of problems
##    as they do not usually have visible tests of the data type.)
##
## 5. If the autograder says you have an error, then carefully
##    examining the error message -- it is usually helpful.  See
##    the examples below.

## Example 1: Incorrect location of an input file.

#################################################################
########################### THE ERROR  ##########################
#################################################################

Traceback (most recent call last):
  File "run_tests.py", line 39, in <module>
    from assignment06 import q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11
  File "/autograder/source/assignment06.py", line 33, in <module>
    loglines = open('desktop/timing_log.txt').read().splitlines()
FileNotFoundError: [Errno 2] No such file or directory: 'desktop/timing_log.txt'
Your assignment was not read in correctly, please fix the error and resubmit before the deadline.


## Example 2: An index value for a list is out of the list range.

#################################################################
########################### THE ERROR  ##########################
#################################################################

Traceback (most recent call last):
  File "run_tests.py", line 39, in <module>
    from assignment06 import q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11
  File "/autograder/source/assignment06.py", line 79, in <module>
    y = loglines[100000]
IndexError: list index out of range
Your assignment was not read in correctly, please fix the error and resubmit before the deadline.


## Example 3: A key error, which is similar to Example 2 but for 
##            a Series or DataFrame

#################################################################
########################### THE ERROR  ##########################
#################################################################

Traceback (most recent call last):
  File "/usr/local/lib/python3.8/dist-packages/pandas/core/indexes/range.py", line 351, in get_loc
    return self._range.index(new_key)
ValueError: -17 is not in range

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "run_tests.py", line 39, in <module>
    from assignment06 import q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11
  File "/autograder/source/assignment06.py", line 103, in <module>
    ser[-17]
  File "/usr/local/lib/python3.8/dist-packages/pandas/core/series.py", line 853, in __getitem__
    return self._get_value(key)
  File "/usr/local/lib/python3.8/dist-packages/pandas/core/series.py", line 961, in _get_value
    loc = self.index.get_loc(label)
  File "/usr/local/lib/python3.8/dist-packages/pandas/core/indexes/range.py", line 353, in get_loc
    raise KeyError(key) from err
KeyError: -17
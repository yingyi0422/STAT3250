##
## File: week03a.py (STAT 3250)
## Topic: Conditionals and Loops
##

####   Conditionals: Comparing values 
 
x = 4
y = 16

x == 8  # Test if x = 8
x < y   # Test if x < y
x**2 < y  # Test if x^2 < y
x**2 <= y  # Test if x^2 <= y
x != 5  # Test if x is not equal to 5

## We can also create compound conditionals using "and" & "or"

## "and" requires all statements to be True for the compound statement to 
## be True.  Otherwise the compound statement is False.

## Both are True so this compound statement is True
x**2 == y and y > 10 

## Note: "&" is not the same as "and".  In this context we will typically
## want to use "and".   
x < y and y == 7  # The second statement is False  

## "or" requires all statements to be False in order for the compound 
## statement to be False.  Otherwise the compound statement is True.

## The first is False but the second is True so this compound is True
x > y or y == 16  

## Both are False so this compound is False  
x > y or x == 10

## As above, use "or" not "|"


#### If/Else statements

## "if" statements execute code when a conditional statement is True
a = 8
b = 10
if a < b: # Code will be run since a < b
    print(a)      # Indent specifies scope of if
    print("Done")

## Nothing happens since b < a is False
if b < a:
    print("Nothing to see here")
    
## Compound statement is True, so code runs
if a**2 < b or b >= 10:
    print(b)
    
## We can add "else" to provide code to run if statement is False.
if a > b:  # Since a > b, statement is False so the "else" code runs.
    print(a)
    print("Done")
else:
    print(b)
    print("Really done!")
    
    
#### "For" loops -- an intro

primes = [2,3,5,7,11,13,17,19,23,29] # The first 10 primes

## Here is a for loop to print each element of "primes"
for i in range(10):   # range(n) gives 0, 1, 2, ..., n-1
    print(primes[i])  # Indentation indicates loop scope

## We also can loop directly across the list, without having
## to use an index to identify individual entries.
for p in primes:  # Initiates the loop; list needed
    print(p)      # Prints out each prime p
    
## The next code will print out the primes and their squares,
## and add up the prime values
s = 0  # This will hold the sum of the primes
for p in primes:
    print(p)     # The indented code is inside the loop
    print(p**2)
    s = s + p    # Adds the current prime value to the sum
print(s)    # Not in the loop; prints sum at the end

## We can populate a new list with the squares of primes.
primes2 = 10*[0] # Creates a list with 10 0's.
for i in range(10):            # Compute each square,
    primes2[i] = primes[i]**2  # put it in primes2
print(primes2)


#### if/else in for loops

## We can put if/else in for loops
primes = [2,3,5,7,11,13,17,19,23,29] # 10 primes
for p in primes:
    if p > 15:
        print(p)
    else:
        print("Too small to print")

## Here we count the number of primes with remainder 1 upon division 
## by 4, found using the % operator
ct = 0 # This will hold the count
for p in primes:
    if p % 4 == 1:  # Test if p/4 has remainder 1
        print(p)
        ct = ct + 1
print(ct)

## This combines the above to determine the number of entries in "primes" 
## that are greater than 15 or have remainder 1 upon division by 4.
ct = 0 # This will hold the count
for p in primes:
    if p % 4 == 1 or p > 15:  
        ct = ct + 1
    else:
        print(p)
print(ct)

#### while loops

## A "while" loop repeats until a condition is not met.  An example:
primes = [2,3,5,7,11,13,17,19,23,29] # 10 primes
i = 0  # initialize index
p = primes[0]
while p <= 15:  # Loop will run until ct > 5
   print("The current prime is %d" % primes[i])  # print count
   i += 1  # increment index
   p = primes[i]









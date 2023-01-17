##
## File: assignment03.py (STAT 3250)
## Topic: Assignment 3 
##

## Two *very* important rules that must be followed in order for your 
## assignment to be graded correctly:
##
## a) The file name must be exactly "assignment03.py" (without the quotes)
## b) The variable names followed by "= None" must not be changed and these 
##    names variable names should not be used anywhere else in your file.  Do   
##    not delete these variables, if you don't know how to find a value just  
##    leave it as is. (If a variable is missing the autograder will not grade  
##    any of your assignment.)

## Questions 1-7: For the questions in this part, use the following
##  lists as needed:
    
list01 = [5, -9, -1, 8, 0, -1, -2, -7, -11, 0, -1, 6, 7, -2, -1, -5]
list02 = [-2, -5, -2, 8, 7, -7, -11, 11, -1, 6, 6, -7, -9, 1, 5, -11]
list03 = [9, 0, -8, 3, 2, 7, 3, -4, 5, -9, -7, -3, -11, -6, -5, 1]
list04 = [-4, -6, 8, 8, -5, -5, -8, -3, -1, 7, 0, 2, -5, -2, 0, -5]
list05 = [-11, -3, 8, -9, 2, -8, -7, -12, 7, 3, 12, 0, 6, 4, -11, 6]
biglist = list01 + list02 + list03 + list04 + list05

##  Questions 1-7: Use loops to answer each of the following applied to  
##  the lists defined above.
 
## 1.  Add up the cubes of the entries of biglist.

import numpy as np # import numpy
s = 0 # set s = 0
for p in biglist: # form a loop
    s = s + (p**3)
    print(s)
    
q1 = s

## 2.  Create "newlist01", which has 16 entries, each the sum of the 
##      corresponding entry from list01 added to the corresponding entry
##      from list02.  That is,
##     
##         newlist01[i] = list01[i] + list02[i] 
##
##      for each 0 <= i <= 15.

newlist01 = 16*[0] # make a list
for i in range(16): # form a loop
    if 0 <= i <= 15:
        newlist01[i] = list01[i] + list02[i] # add up the same index
        
q2 = newlist01

## 3.  Determine the number of entries in biglist that are less than 3.

ct = 0 # create ct = 0
for h in biglist: # make a loop
    if h < 3:
        ct += 1
q3 = ct

## 4.  Create a new list called "newlist02" that contains the elements of
##      biglist that are less than -7, given in the same order as the
##      elements appear in biglist.

newlist02 = [] # create a list

for t in biglist: # make a loop
    if t < -7:
        newlist02.append(t)

q4 = newlist02

## 5.  Find the sum of the negative entries of biglist.

sum = 0
for n in biglist:
    if n < 0:
        sum += n
        
q5 = sum

## 6. Make a list of the first 12 positive entries of biglist, given in
##     the order that the values appear in biglist.

newlist03 = []
for m in biglist:
    if m > 0 and len(newlist03) < 12:
        newlist03.append(m)
q6 = newlist03

## 7. Identify all elements of biglist that have a smaller element that 
##     immediately preceeds it.  Make a list of these elements given in
##     the same order that the elements appear in biglist.

newlist04 = []
for b in range(len(biglist)):
    if biglist[b] > biglist[b-1]:
        newlist04.append(biglist[b])
q7 = newlist04

#### Questions 8-15

##  The questions in this section refer to the data in the file
##  'assignment03-data.csv'.  The data contains 711 records from an
##  employer, with 21 columns of data for each record.  (There
##  are a few missing values indicated by zeros where zeros 
##  are clearly not appropriate.)  The file 'README-03.pdf' has
##  a summary of the meanings for the variables.
##
##  All of these questions can be completed **without** loops.  You 
##  should try to do them this way, "code efficiency" will take 
##  this into account.


## 8.  Find the mean body mass index among all records.

import pandas as pd # import panda
df = pd.read_csv("assignment03-data.csv") # read file
q8 = np.mean(df)['Body mass index'] 


## 9.  Determine the number of records corresponding to
##      being absent on a Wednesday.

q9 = len(df.loc[df['Day of the week'] == 3])

## 10.  Find the number of unique employees IDs represented in 
##      this data.  

q10 = len(np.unique(df["ID"])) 

## 11.  Find the total transportation expense for the employee with
##      ID = 22.

q11 = np.sum(df.loc[df['ID'] == 22, 'Transportation expense'])


## 12.  Find the total number of hours absent for the records
##      for employee ID = 17.

q12 = np.sum(df.loc[df['ID'] == 17, 'Absenteeism time in hours'])

## 13.  Find the mean number of hours absent for the records where the
##      employee was absent due to diseases of the genitourinary system.

q13 = np.mean(df.loc[df['Reason for absence'] == 14, 'Absenteeism time in hours'])


## 14.  Find the median number of hours absent for the records of those who 
##     have no pets.

q14 = np.median(df.loc[df['Pet'] == 0, 'Absenteeism time in hours'])


## 15.  Among the records for absences that exceeded 6 hours, find the 
##      percentage that involved smokers.  (Be sure your answer is in
##      percentage and not proportion.)

sorteddf1 = df.loc[df['Absenteeism time in hours'] > 6]
q15 = np.sum(sorteddf1['Social smoker'] == 1) / len(sorteddf1) * 100


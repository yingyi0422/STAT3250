##
## File: assignment01.py (STAT 3250)
## Topic: Assignment 1 
##

## Two *very* important rules that must be followed in order for your assignment
## to be graded correctly:
##
## a) The file name must be exactly "assignment01.py" (without the quotes)
## b) The variable names followed by "= None" must not be changed and these 
##    variable names should not be used anywhere else in your file.  Do not  
##    delete these variables, if you don't know how to find a value just leave 
##    it with "= None". (If a variable is missing the autograder will not grade  
##    any of your assignment.)

####  For Questions 1-6 use the following lists as needed:
list01 = [2,5,4,9,10,-3,5,5,3,-8,0,2,3,8,5,2,-3,8,7]
list02 = [-7,-3,8,-5,-5,2,4,9,10,-7,9,10,2,13,-12,-4,1,3,5]
list03 = [2,-5,6,0,7,-2,-3,5,0,2,8,7,9,2,0,-2,5,5,6]
list04 = [3,5,-10,2,0,4,-5,-7,6,2,3,3,5,12,-5,-9,-7,4]
biglist = list01 + list02 + list03 + list04

## 1.  Find the product of the last five elements of list04.

q1 = list04[-1] * list04[-2] * list04[-3] * list04[-4] * list04[-5] #identify 
## each of the element and take their product

## 2.  Extract the sublist of list01 that goes from
##     the 4th to the 10th elements (inclusive).

q2 = list01[3:10] # identify the sublist of list01 that goes from
##     the 4th to the 10th elements

## 3.  Concatenate list01 and list04 (in that order), sort
##     the combined list, then extract the sublist that 
##     goes from the 6th to the 17th elements (inclusive).

Midlist = list01 + list04 # generate Midlist which combines list01 and list04
Midlist.sort() # sort the list
q3 = Midlist[5:17] # extract the sublist

## 4.  Generate "biglist", then extract the sublist of every 5th 
##     element starting with the 4th list element

q4 = biglist[3:75:5] # extract the sublist of every 5th 
##     element starting with the 4th list element

## 5.  Determine the number of times that 3 appears in biglist.

q5 = biglist.count(3) # count the number of times that 3 appears

## 6.  Determine the index for the first appearance of 12 in biglist.

q6 = biglist.index(12) # Determine the index for the first appearance of 12 
## in biglist.

####  Read in the file 'assignment01-data.csv' and use this data for 
####  Questions 7-8

## 7.  Determine the mean of the values in the 'Yards' column.

import pandas as pd # import pandas
df = pd.read_csv("assignment01-data.csv") # access the csv file
q7 = df['Yards'].mean() # find the mean of the yards

## 8.  Determine the median of the values in the 'YardLineFixed' column.

q8 = df['YardLineFixed'].median() # find the median of the column





  
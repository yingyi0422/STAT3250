##
## File: assignment13.py (STAT 3250)
## Topic: Assignment 13 
##

## Two *very* important rules that must be followed in order for your assignment
## to be graded correctly:
##
## a) The Python file name must be exactly "assignment13.py" (without the quotes)
## b) The variable names q1, q2, ... must not be changed.  These variable 
##    names should not be used anywhere else in your file.  Do not delete these
##    variables. If you don't know how to find a value for a variable, just  
##    leave the corresponding variable with "= None". (If any variable is     
##    missing the autograder will not grade your assignment.)

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the assignment13 data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  

##  Submission Instructions: Submit your code file in Gradescope under 
##  'Assignment 13'.  The autograder will evaluate your answers to
##  Questions 1-6.  

##  All questions on this assignment use the data 'assignment13-data.csv'.
##  This data set consists of 100,000 records from a larger data set of 
##  New York city parking violation citations.  There are 43 variables
##  (columns) in the data set.  You can see more information about the
##  data at
##
##  https://www.opendatanetwork.com/dataset/data.cityofnewyork.us/pvqr-7yc4
##
##  For this assignment, use the "pipe version" of code descibed in the
##  assignment demo file and video to the extent possible.  The coding method 
##  will be included in the Code Efficiency score.

import pandas as pd #Import package
df = pd.read_csv('assignment13-data.csv') #Read in file




## 1.  From the data frame, determine the number of records for which the 
##     Violation County code is BX.

q1 =(
     df
     .query(
         "`Violation County` == 'BX'") #subset to only BX county
     .shape[0] #number of rows
     )  # number of records with Violation County = BX


## 2.  From the data frame, determine the number of records for which the 
##     Issuing Agency code is P, the Vehicle Body Type is SUBN, and the
##     Vehicle Make is Ford.
q2=(
    df
    .query(
        "`Issuing Agency` == 'P'" #first condition
        "and `Vehicle Body Type` == 'SUBN'" #second condition
        "and `Vehicle Make` == 'FORD'") #subset thir condition
    .shape[0] #number of rows
    ) # number of records with conditions described above


## 3.  From the data frame, extract the records for which Plate Type is COM.
##     From among these, determine the number of each type of Vehicle Body
##     Type.  Submit a Series of the top 10 value counts (including ties), sorted
##     from most to least. (The index can be the Vehicle Body Type.)
q3=(
    df
    .query(
        "`Plate Type` == 'COM'") #subset to COM plate
    .filter(items=["Vehicle Body Type"]) #only keep body type column
    .value_counts() #count each value
    .nlargest(10,keep='all') #keep 10 largest
    ) # data frame of violation code counts, plate type = COM
## 4.  From the data frame, extract the records for which Plate Type is PAS,
##     the Registration State is NJ, and the Law Section is 408.
##     From among these, determine the number of each type of Violation County.
##     Submit a Series of the count values, sorted
##     from most to least.  (The index can be the violation county.)
q4=(
    df
    .query(
        "`Plate Type` == 'PAS'" #first condition
        "and `Registration State` == 'NJ'" #second condition
        "and `Law Section` == 408") #third condition
    .filter(items=['Violation County']) #keep only county column
    .value_counts() #count occurance of each value
    .sort_values(ascending=False) #sort
    )# data frame of violation county counts


## 5.  From the data frame, extract the records for which Feet From Curb is
##     greater than 0, and then determine the number of each Vehicle Body
##     Type. Submit a Series of the count values, sorted
##     from most to least, giving the top-10 (including ties).  (The index can be the vehicle  
##     body type.)
q5=(
    df
    .query(
        "`Feet From Curb` >0") #subset to from curb >0
    .filter(items=['Vehicle Body Type']) #keep only body type column
    .value_counts() #count occurance of each value
    .nlargest(10,keep='all') #keep 10 largest
    )# data frame of vehicle body type counts, feet from curb > 0



## 6.  From the data frame, extract the records for which Feet From Curb is
##     greater than 0, and then from among these determine the average number 
##     of feet from the curb for each Registration State. Submit a Series
##     of the top-10 mean values (including ties), sorted from largest to smallest.
##     (The index can be the Registration State.)
q6=(
    df
    .query(
        "`Feet From Curb` >0") #subset to feet from curb >0
    .filter(items=['Feet From Curb', 'Registration State']) #filter to only 2 columns
    .groupby("Registration State") #groupby state
    .agg(["mean"])# calculate mean 
    .squeeze() #convert to series
    .nlargest(10,keep='all') #keep 10 largest
    )# data frame of feet from curb averages






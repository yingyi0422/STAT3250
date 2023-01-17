##
## File: assignment07.py (STAT 3250)
## Topic: Assignment 7
##

##  Note: The description below takes the place of a README file for
##  this assignment.

##  The questions this assignment are based on "assignment07-data.txt".
##  The file "assignment07-data.txt" contains the set of all WeBWorK
##  log entries on April 1, 2011.  The entries are organized by
##  one log entry per line, with each line including the following:
##
##  --the date and time of the entry
##  --a number that is related to the user (but is not unique)
##  --something that appears to be the epoch time stamp
##  --a hyphen
##  --the "WeBWorK element" that was accessed
##  --the "runTime" required to process the problem
##
##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the assignment07-data.txt data that includes only a fraction of 
##  rthe ecords.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.
## 
##  Note: Most or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.


## Load pandas and read in the data set
import pandas as pd # load pandas as pd
import numpy as np # load numpy as np
loglines = open('assignment07-data.txt').read().splitlines()


## 1.  How many log entries were for requests for a PDF version of an
##     assignment?  Those are indicated by "hardcopy" appearing in the 
##     WeBWorK element.

temp = pd.Series(loglines).str.split(' ') #first split all the entries by space and name it temp
hardcopy = temp.str[8][temp.str[8].str.contains('hardcopy')] # get the 9th elements in the separated entries and find all that contain hardcopy
q1 =  len(hardcopy) # number of log entries requesting a PDF

## 2.  What percentage of log entries involved a Spring '12 section of MATH 1320?

spring12_1320 = temp.str[8][temp.str[8].str.contains('Spring12-MATH1320')] # get the elements in the separated entries and find all that contain spring12math1320
q2 = len(spring12_1320) / len(temp.str[8]) * 100 # percentage of log entries, Spring '12 MATH 1320

## 3. How many different classes use the system? Treat each different name 
##    as a different class, even if there is more than one section of a course.
##    (Any difference at all -- even just upper or lower case -- is a different
##    class.)  

temp1 = temp.str[8].str.split('/') # separate all the 9th entries by /
classes = temp1.str[2].dropna() # drop any NA inputs
classes = classes.str.replace(']','').str.replace(' ','') # remove all the ] and empty spaces
classes = classes[classes!=''] # remove all the empty entries
classdiff = np.unique(classes) # find different classes that are unique
q3 = len(classdiff)  # number of different classes using the system
                        

## 4.  Find the percentage of log entries that came from an initial
##     log in.  For those, the WeBWorK element has the form
##
##          [/webwork2/ClassName] or [/webwork2/ClassName/]
##
##     where "ClassName" is the name of a class.  (Anything in the 'ClassName'
##     position is a classname, regardless of what is says.) 

entries = pd.Series(loglines).str.split('[') #convet to series and then split all the elemets by [
entries1 = entries.str[2].str.split(']').str[0].str[:-1].str.split("/") # choose the third elements in the entries
#and split them by ], then choose all the elements except the last one and split them by /
q4 = len(entries1[entries1.str.len() == 3]) / len(temp) * 100  # percentage of log entries from initial log in
# if there are three elements then it is an initial login

## 5.  Determine the percentage of log entries for each section of MATH 1310
##     from Spring 2012, among the total number of log entries for MATH 1310,
##     Spring 2012.  Give the percentages as a Series with class name as
##     index and percentages as values, sorted by percentage largest to smallest.
##     (The class name should be of the form 'Spring12-MATH1310-InstructorName')

spring12_1310 = temp.str[8][temp.str[8].str.contains('Spring12-MATH1310')] # get all the entries that contain spring12-math1310
spring12_1310 = spring12_1310.str.split('/').str[2].str.replace(']','') # split the entries by / and take the 3rd element and remove ]
sections = spring12_1310.groupby(spring12_1310).count() # groupby the elements in spring12_1310
q5 = (sections / len(spring12_1310) * 100).sort_values(ascending = False) # Series of MATH 1310 sections and percentage within MATH 1310


## 6.  How many log entries were from instructors performing administrative
##     tasks?  Those are indicated by "instructor" alone in the 3rd position of
##     the WeBWorK element.  

instructors = temp.str[8][temp.str[8].str.contains('instructor')] #get all the entries that contain instructor
alone = instructors.str.split('/').str[3] #split the entries by / and pick the fourth element which is the instructor
q6 = len(alone[alone == 'instructor'])  # number of instructor administrative log entries


## 7.  Find the number of log entries for each hour of the day. Give the
##     counts for the top-5 (plus ties as usual) as a Series, with hour of day
##     as index and the count as values, sorted by count from largest to 
##     smallest.

hour = temp.str[3].str.split(':').str[0] #pick the fouth element then split by : and pick the first element which is hour
q7 = hour.value_counts().nlargest(5,keep='all')  # Series of entry count by hour, top 5


## 8.  Find the number of log entries for each minute of each hour of the day. 
##     Give the counts for the top-8 (plus ties as usual) as a Series, with 
##     hour:minute pairs as index and the count as values, sorted by count 
##     from largest to smallest.  (An example of a possible index entry
##     is 15:47)

minute = temp.str[3].str.split(':', expand = True).iloc[:,0:2] #get the minute element, which is to pick all the fouth element of all entries and split by :, then group two columns
minute.columns = ['hour','minute'] #name the two column that was grouped
q8 = minute.groupby(['hour','minute']).size().nlargest(8,keep='all')  # Series of counts by hour:minute, top-8 plus ties


## 9. Determine which 5 classes had the largest average "runTime".  Give a 
##    Series of the classes and their average runTime, with class as index
##    and average runTime as value, sorted by value from largest to smallest.

temp2 = pd.Series(loglines).str.split(' ',expand = True) # split all the loglines entries by empty space
temp3 = temp2[8].str.split('/',expand=True)  # then pick the 9th elements and split by /
temp4 = pd.DataFrame(temp3[2]) # convert the tgrid element in temp 3 into a dataframe
temp4['runTime'] = temp2[11].astype(float).dropna() # add a column runtime which is the the 12th element in temp2
temp4.columns = ('Course','runTime') #renames the columns
temp4 = temp4[temp4['Course'] != ']'] #remove any non-numerical values
temp4['Course'] = temp4['Course'].str.replace(']','') #remove any ]
q9 = temp4['runTime'].groupby(temp4['Course']).mean().sort_values(ascending = False).head(5) # Series of classes and average runTimes


## 10. Determine the percentage of log entries that were accessing a problem.  
##     For those, the WeBWorK element has the form
##
##           [/webwork2/ClassName/AssignmentName/Digit]
##     or
##           [/webwork2/ClassName/AssignmentName/Digit/]
##
##     where "ClassName" is the name of the class, "AssignmentName" the
##     name of the assignment, and "Digit" is a positive digit. (Any digit in
##     the 'Digit' position is considered a problem.)

data10 = temp1.str[4].dropna() # get the fifth entries of every entry in temp1, drop any NA value
data10 = data10[data10 != ']'] # remove any non-numerical values
q10 = len(data10) / len(temp)*100  # percentage of log entries accessing a problem
 

## 11. Find the top-10 (plus tied) WeBWorK problems that had the most log entries,
##     and the number of entries for each (plus ties as usual).  Sort the 
##     table from largest to smallest.
##     (Note: The same problem number from different assignments and/or
##     different classes represent different WeBWorK problems.) 
##     Give your answer as a Series with index entries of the form
##
##          ClassName/AssignmentName/Digit
##
##     and counts for values, sorted by counts from largest to smallest.

data11 = temp3.iloc[:,2:5].dropna() # choose the third to the sixth elements in temp3 and drop any NA Values
data11.columns = ('ClassName','AssignmentName','Digit') # names the columns as class assignement and digit
data11 = data11[data11['Digit']!=']'] # remove digits that are not ]
q11 = data11.groupby(['ClassName','AssignmentName','Digit']).size().nlargest(10,keep='all')  # Series of problems and counts



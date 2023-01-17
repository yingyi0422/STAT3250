##
## File: assignment06.py (STAT 3250)
## Topic: Assignment 6 
##

## Two *very* important rules that must be followed in order for your assignment
## to be graded correctly:
##
## a) The Python file name must be exactly "assignment06.py" (without the quotes)
## b) The variable names q1, q2, ... must not be changed.  These variable 
##    names should not be used anywhere else in your file.  Do not delete these
##    variables. If you don't know how to find a value for a variable, just  
##    leave the corresponding variable with "= None". (If any variable is     
##    missing the autograder will not grade your assignment.)

##  Submission Instructions: Submit your code file in Gradescope under 
##  'Assignment 6'.  The autograder will evaluate your answers to
##  Questions 1-11.  

##  All questions on this assignment use the data 'assignment06-data.csv'.
##  See README-06.txt for information about the data set.

##  Gradescope will run your code on a version of assignment06-data.csv
##  that has had about 40% of the records removed.  You will need to write
##  your code in such a way that your file will automatically produce the
##  correct answers on the new set of data.  

##  Notes: 
##    * When available, use the value of a dedicated variable instead of
##      the information given in the play Description.
##    * Plays with penalties have been removed from the data set, to improve
##      the clarity of some questions.


## 1.  Determine all teams that had at least 250 RUSH plays when the offense 
##     team. (This is for the entire season.)  Give your answer as a Series
##     with team identifier as index and the corresponding number of RUSH
##     plays as value, sorted from largest to smallest. 
##     Note: Use the 'PlayType' variable to determine which plays are RUSH.
import pandas as pd

df = pd.read_csv("assignment06-data.csv")

rush = df[df['PlayType']=='RUSH'] #get the playtype for rush

df1 = rush['PlayType'].groupby(rush['OffenseTeam']).count() #group the playtype by offense team

q1 = df1[df1>=250].sort_values(ascending=False) # Series of number of RUSH plays


## 2.  Determine the top-10 teams (including all teams tied for the 10th
##     position) in terms of the number of interceptions when the defensive 
##     team.  Give your answer as a Series with the team identifier
##     as index and the number of interceptions as value, sorted from most
##     to least.

interc = df[df['IsInterception']==1] #get the interception that are successful

df2 = interc['IsInterception'].groupby(interc['DefenseTeam']).count()
#group the interception by defenseteam and sort

q2 = df2.nlargest(10,keep='all') # Series of number of interceptions


## 3.  Determine the top-12 teams (including all teams tied for the 12th
##     position) in terms of the average number of SACKS per game while 
##     the defensive team.  Give your answer as a Series with the 
##     team identifier as index and the average number of SACKS as value,
##     sorted from most to least. (You may assume that each team plays in
##     16 games.)

sack = df['IsSack'].groupby([df['DefenseTeam'],df['GameId']]).sum() #group the sack by defenseteam and calculate the sum

sack = sack.groupby(level='DefenseTeam').mean() #group by Defenseteam and find the mean

q3 = sack.nlargest(12,keep='all')  # Series of average number of sacks


sacks = df['IsSack'].groupby([df['DefenseTeam'],df['GameId']]).sum() 
#group slack by defenseteam and find the sum
sacks = sacks.groupby(level='DefenseTeam').mean()
q3 = sacks.nlargest(12,keep='all')  # slice the topp 12



## 4.  Determine the top-8 teams (including all teams tied for the 8th
##     position) in terms of the highest average Yards gained per PASS 
##     play when the offensive team.  Give your answer as a Series with
##     the team identifier as index and the average number of Yards per 
##     PASS play as value, sorted from most to least.

p = df[df['PlayType']=='PASS'] #get the Pass play

yards = p['Yards'].groupby(p['OffenseTeam']).mean() #group the yard by offenseteam and calculate the mean

df4 = yards.sort_values(ascending=False) #sort in descending order

q4 = df4[0 : 8, ]  # Series of average number of yards per pass play


## 5.  Determine the teams for which the average yards ToGo on 2nd Down plays
##     when on defense is at least 8.0.  Give your answer as a Series with
##     the team identifier as index and the average yards per play as value,
##     sorted from most to least.

down = df[df['Down']==2] #get the second down plays

Togo = down['ToGo'].groupby(down['DefenseTeam']).mean() #group to go by defenseteam and calculate the mean

q5 = Togo[Togo>=8].sort_values(ascending=False)   #calculate values that are at least 8 and sort in descending order



## 6.  Determine the teams that have at least 20% of all PASS attempts
##     classified as DEEP (all types) in the 'PassType' variable.  Give your 
##     answer as a Series with team identifier as index and percentage as
##     value, sorted from most to least.


n1 = p['PassType'].groupby(p['OffenseTeam']).count()
# find all passes group by offense team

deep = p[p['PassType'].str.contains(pat='DEEP')]
# check if passtype contains deep

n2 = deep['PassType'].groupby(p['OffenseTeam']).count()
# find all appearances of DEEP and group by offense team

result = 100*n2/n1 # calculate the percentage

q6 = result[result>=20].sort_values(ascending=False) # Series of percentages




## 7.  Identify the Bottom-5 teams in terms of average Yards per RUSH when there 
##     is less than 5 minutes in the Quarter 4 as the team on offense.  (This  
##     is when the variable Minute is 4 or less.) Give your answer as a Series 
##     with team identifier as index and average yards per RUSH as value, 
##     sorted from smallest to largest.
##     Note: Use the 'PlayType' variable to determine which plays are RUSH.


rush2 = df[(df['PlayType']=='RUSH')&(df['Minute']<5)&(df['Quarter']==4)]
#get playtype for rush when there is less than 5 minute

df7 = rush2['Yards'].groupby(rush2['OffenseTeam']).mean().sort_values(ascending=True)
#group yards by offenseteam, calculate the mean, and sort in descending order

q7 = df7[0 : 5, ]  # Series of average yards


## 8.  Determine the percentage of pass attempts by SF quarterback Nate Mullens
##     that were incomplete.  (Player names are given in the 'Description'
##     variable.)

df8 = df[df['Description'].str.lower().str.contains('n.mullens')]
#get all the ones that include mullens

p8 = df8[df8['PlayType'] == 'PASS'] #get the pass playtype

q8 = 100*len(p8[p8['IsIncomplete']==1])/len(p8) # percentage of pass attempts that are incomplete  



## 9.  Determine the average length of successful field goal attempts by 
##     Baltimore kicker Justin Tucker. Use the information in the 
##     'Description' and 'PlayType' for this question.



JT = df[(df['Description'].str.lower().str.contains('9-j.tucker'))&(df['PlayType']=='FIELD GOAL')]
#find the ones contain tucker and field goal as playtype

good = JT[JT['Description'].str.contains('IS GOOD')]
#get the good attempts

q9 = good['YardLineFixed'].mean() + 18 #average length


## 10. For each team and each quarter, determine the total Yards (full season)
##     given up when the defensive team.  Use this data to determine, for each
##     quarter, which team gave up the most total Yards.  Give your answer
##     as a Series with team identifier as index and total yards as value,
##     sorted by quarter 1, 2, 3, 4, 5.


Yards10 = df['Yards'].groupby([df['DefenseTeam'],df['Quarter']]).sum()
#Get the yards, group by defenseteam and quarter, find the sum

df10 = Yards10.groupby('Quarter', group_keys=False).nlargest(1) 

q10 = df10.droplevel('DefenseTeam',axis=0) # Series of total yards 


## 11. For each team, determine which quarter yielded the greatest total
##     Yards when the offensive team.  Use this information to create a
##     Series of all teams for which the 2nd quarter yielded the most total
##     Yards, with team identifier as index and total yards as value, sorted
##     alphabetically by team identifier.


Yards11 = df['Yards'].groupby([df['OffenseTeam'],df['Quarter']]).sum() #get the yards, group by offenseteam and quarter

df11 = Yards11.groupby('OffenseTeam', group_keys=False).nlargest(1) 

q11 = df11.xs(2,level='Quarter') # Series of teams and 2nd quarter total yards




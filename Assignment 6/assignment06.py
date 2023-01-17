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

import pandas as pd #import pandas
df = pd.read_csv("assignment06-data.csv") #read the file

group1 = df.loc[df['PlayType'] == 'RUSH'] #slice rush
group1a = group1['PlayType'].groupby(group1['OffenseTeam']).count() #group playtype
#by offense team and count the number of entries
q1 = group1a[group1a >= 250].sort_values(ascending = False) # Series of number of RUSH plays

## 2.  Determine the top-10 teams (including all teams tied for the 10th
##     position) in terms of the number of interceptions when the defensive 
##     team.  Give your answer as a Series with the team identifier
##     as index and the number of interceptions as value, sorted from most
##     to least.

group2 = df.loc[df["IsInterception"] == 1] #slice entries that are intercepted
group2a = group2["IsInterception"].groupby(group2["DefenseTeam"]).count() #group isinterception by defense teams
q2 = group2a.nlargest(10, keep = "all") # Series of number of interceptions


## 3.  Determine the top-12 teams (including all teams tied for the 12th
##     position) in terms of the average number of SACKS per game while 
##     the defensive team.  Give your answer as a Series with the 
##     team identifier as index and the average number of SACKS as value,
##     sorted from most to least. (You may assume that each team plays in
##     16 games.)

group3 = df.loc[df["IsSack"] == 1] #slice to get the entries that have sacks
group3a = group3["IsSack"].groupby(group3["DefenseTeam"]).count() / 16
#group issack by the defense teams and get the average out of 16 games
q3 = group3a.nlargest(12, keep = "all") # Series of average number of sacks

## 4.  Determine the top-8 teams (including all teams tied for the 8th
##     position) in terms of the highest average Yards gained per PASS 
##     play when the offensive team.  Give your answer as a Series with
##     the team identifier as index and the average number of Yards per 
##     PASS play as value, sorted from most to least.

group4 = df.loc[df["IsPass"] == 1] #slice the entries with pass
group4a = group4["IsPass"].groupby(group4["OffenseTeam"]).count() #group Ispass by offense teams and count the number
group4b = group4["Yards"].groupby(group4["OffenseTeam"]).sum() #group yards by offenseteam and get the sum
q4 = (group4b / group4a).nlargest(8, keep = "all") # Series of average number of yards per pass play

## 5.  Determine the teams for which the average yards ToGo on 2nd Down plays
##     when on defense is at least 8.0.  Give your answer as a Series with
##     the team identifier as index and the average yards per play as value,
##     sorted from most to least.

group5 = df.loc[df["Down"] == 2] #slice out entries when down = 2
group5a = group5["ToGo"].groupby(group5["DefenseTeam"]).mean() #group togo by defense teams and find the mean
q5 = group5a.loc[group5a >= 8].sort_values(ascending = False) # Series of average yards

## 6.  Determine the teams that have at least 20% of all PASS attempts
##     classified as DEEP (all types) in the 'PassType' variable.  Give your 
##     answer as a Series with team identifier as index and percentage as
##     value, sorted from most to least.

group6 = group4["PassType"].groupby(group4["OffenseTeam"]).count() #group passtype by offense teams and count the number of passes
group6a = group4[group4['PassType'].str.contains('DEEP')] #figure out the pass types that contain "deep"
group6b = group6a['PassType'].groupby(group6a['OffenseTeam']).count() #group passtypes that contain deep by offense teams
percent = group6b / group6 * 100 # find the percentage of types that are deep among all teams
q6 = percent[percent >= 20].sort_values(ascending = False) # Series of percentages

## 7.  Identify the Bottom-5 teams in terms of average Yards per RUSH when there 
##     is less than 5 minutes in the Quarter 4 as the team on offense.  (This  
##     is when the variable Minute is 4 or less.) Give your answer as a Series 
##     with team identifier as index and average yards per RUSH as value, 
##     sorted from smallest to largest.
##     Note: Use the 'PlayType' variable to determine which plays are RUSH.

group7 = df[(df['PlayType'] == 'RUSH') & (df['Quarter'] == 4) & (df['Minute'] <=  4)] #slice entries that meet all three conditions
group7a = group7['Yards'].groupby(group7['OffenseTeam']).mean() #group yards by offense and take the average
q7 = group7a.sort_values(ascending = True)[0:5, ] # Series of average yards

## 8.  Determine the percentage of pass attempts by SF quarterback Nate Mullens
##     that were incomplete.  (Player names are given in the 'Description'
##     variable.)

group8 = df[df["PlayType"] == "PASS"] # slice the entries that have play type as pass
group8a = group8[group8['Description'].str.contains('N.MULLENS')] #find all entries that contain Nate Mullens
q8 = len(group8a[group8a['IsIncomplete'] == 1]) / len(group8a) * 100 # percentage of pass attempts that are incomplete  

## 9.  Determine the average length of successful field goal attempts by 
##     Baltimore kicker Justin Tucker. Use the information in the 
##     'Description' and 'PlayType' for this question.

group9 = df[df["PlayType"] == "FIELD GOAL"] #slice the entries that have play type as field goal
group9a = group9[group9['Description'].str.contains('J.TUCKER')] #find entries that contain justin tucker
group9b = group9a[group9a['Description'].str.contains('IS GOOD')] #find the successful attempts
group9c = group9b['Description'].str.split(' ', expand=True) #split description by space
yard_length = group9c[2] #find the yards mentioned in the description
q9 = yard_length.astype(int).mean()  # average kick length

## 10. For each team and each quarter, determine the total Yards (full season)
##     given up when the defensive team.  Use this data to determine, for each
##     quarter, which team gave up the most total Yards.  Give your answer
##     as a Series with team identifier as index and total yards as value,
##     sorted by quarter 1, 2, 3, 4, 5.

group10 = df['Yards'].groupby([df['DefenseTeam'],df['Quarter']]).sum() #group yards by defense teams and quarter and take the sum
group10a = group10.groupby('Quarter', group_keys=False).nlargest(1) #group quarter and find the greatest yards
q10 = pd.Series(data=group10a.values, index=list(zip(*group10a.index))[0]) # Series of total yards 

## 11. For each team, determine which quarter yielded the greatest total
##     Yards when the offensive team.  Use this information to create a
##     Series of all teams for which the 2nd quarter yielded the most total
##     Yards, with team identifier as index and total yards as value, sorted
##     alphabetically by team identifier.

group11 = df['Yards'].groupby([df['OffenseTeam'],df['Quarter']]).sum() #group yard by offense team and quarter
group11a = group11.groupby('OffenseTeam', group_keys=False).nlargest(1) #groupby offense team and find the greatest yards
q11 = group11a.xs(2, level='Quarter')  # Series of teams and 2nd quarter total yards





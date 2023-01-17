##
## File: assignment04.py (STAT 3250)
## Topic: Assignment 4 
##

## Two *very* important rules that must be followed in order for your assignment
## to be graded correctly:
##
## a) The Python file name must be exactly "assignment04.py" (without the quotes)
## b) The variable names q1, q2, ... must not be changed.  These variable 
##    names should not be used anywhere else in your file.  Do not delete these
##    variables. If you don't know how to find a value for a variable, just  
##    leave the corresponding variable with "= None". (If any variable is     
##    missing the autograder will not grade your assignment.)

##  Submission Instructions: Submit your code file in Gradescope under 
##  'Assignment 4 Code'.  The autograder will evaluate your answers to
##  Questions 1-8, but all code (including that for the graphs) must be
##  included.  

##  The graphs in Questions 9-13 should be submitted under "Assignment 4 Graphs".
##  Save each of your graphs as a separate PNG file, then submit each one
##  separately under the corresponding question.  (This will save you the
##  trouble of creating a PDF document of graphs and produces better results
##  in Gradescope.) 

##  All questions on this assignment use the data 'assignment04-data.csv'.
##  See README-04.txt for information about the data set.

## 1.  Determine the number of offensive plays in the data for SF in the
##     SF vs NYJ game.

import pandas as pd
import seaborn as sns
import numpy as np
df = pd.read_csv('assignment04-data.csv')

q1 = len(df.loc[df['OffenseTeam'] == 'SF']) # number of offensive plays


## 2.  Determine the number of plays (all games) for which the formation was
##     SHOTGUN.

q2 = len(df.loc[df['Formation'] == 'SHOTGUN'])  # number of plays


## 3. Determine the mean net yards gained on BUF offensive plays in the
##    BUF vs NYJ game.

q3 = np.mean(df.loc[df['OffenseTeam'] == 'BUF', 'Yards'])  # mean net yards


## 4.  Determine the mean number of yards to go for a first down on the
##     3rd down plays.

q4 = np.mean(df.loc[df['Down'] == 3, 'ToGo']) # mean net yards


## 5.  Determine the mean number of net yards gained by DEN on 1st down in 
##     the DEN vs NYJ game.

df_1 = df[df['OffenseTeam'] == 'DEN']
q5 = np.mean(df_1.loc[df_1['Down'] == 1, 'Yards']) # mean net yards


## 6.  Determine the mean net yards gained by BUF on plays of type RUSH.

df_2 = df[df['OffenseTeam'] == 'BUF']
q6 = np.mean(df_2.loc[df_2['PlayType'] == 'RUSH', 'Yards'])  # mean net yards


## 7.  Determine the total number of plays resulting in first downs by SF and  
##     IND in their games.
Teamlist = ['SF','IND']
q7 = len(df[df['OffenseTeam'].isin(Teamlist) & df['SeriesFirstDown'] == 1])# total number of plays


## 8.  Determine the mean net yards gained by IND on plays that had formation  
##     UNDER CENTER or NO HUDDLE SHOTGUN.

df_4 = df[(df['OffenseTeam']=='IND') & (df['Formation'].isin(['NO HUDDLE SHOTGUN','UNDER CENTER']))]
q8 = np.mean(df_4['Yards'])   # mean net yards


## 9.  For each team (BUF, DEN, IND, SF) determine the proportion of plays on
##     Down = 3 for which the ToGo value is less than the Yards value.  Give
##     the proportions as a list in the order of the teams shown.

df_5 = df[df['ToGo'] < df['Yards']]
Teamlist_1 = ['BUF', 'DEN', 'IND', 'SF']
list = []
for i in Teamlist_1:
    list.append(len(df_5[(df_5['Down'] == 3) & (df_5['OffenseTeam'] == i)]) / len((df[(df['Down']==3) & (df['OffenseTeam'] == i)])))
q9 = list  # list of proportions


#### Graphs

## 10.  Generate a scatterplot of the variables 'Yards' (on the x-axis) vs.
##     'ToGo' (on the y-axis) for the SF offensive plays in the SF vs NYJ
##     game.  Your graph should match that given in Graph 10.

df_6 = df[df['OffenseTeam'] == 'SF']
p1 = sns.relplot(data=df_6, 
                 x='Yards', 
                 y='ToGo')
p1.set(xlabel='Yards gained',
       ylabel='Yards to go',
       title='SF vs NYJ')

## 11.  Generate a histogram of the values of the variable 'Yards' that are
##      no greater than 20 for the DEN offensive plays in the DEN vs NYJ game.  
##      Your graph should match that given in Graph 11.

df_7 = df[(df['Yards'] <= 20) & (df['OffenseTeam'] == 'DEN')]
p2 = sns.displot(data = df_7, 
                 x='Yards', 
                 binwidth=3)
p2.set(xlabel='Yards gained (<=20)', 
       title='DEN vs NYJ',
       xticks=range(-3,22,3))


## 12.  Generate side-by-side boxplots, one for each offensive team, of the
##      values of 'Yards' for plays classified as 'PASS' under 'PlayType'.
##      Your graph should match that given in Graph 12.

df_8 = df[df['PlayType'] == 'PASS']
p3 = sns.boxplot(data=df_8, 
                 x='OffenseTeam',
                 y='Yards',
                 order=['BUF','DEN','IND','SF'])
p3.set(xlabel='Team on Offense',              
       ylabel='Yards',
       title='Distribution of yards gained by team')

## 13.  Generate a scatterplot of the variables 'Yards' (on the x-axis) vs.
##      'ToGo' (on the y-axis) from the offensive plays 'RUSH" (under 'PlayType') 
##      from the games involving SF and BUF.  Your graph should match that
##      given in Graph 13.

Teamlist_2 = ['SF','BUF']
df_9 = df[(df['PlayType']=='RUSH')&(df['OffenseTeam'].isin(Teamlist_2))]
p4 = sns.relplot(data=df_9, 
                 x='Yards', 
                 y='ToGo',
                 hue='OffenseTeam')
p4.set(xlabel='Yards gained',
       ylabel='Yards to go',
       title='Rushing Plays, BUF & SF')

## 14.  Generate side-by-side barplots, one for each team on offensive, that 
##      give the number of PASS and number of RUSH plays (both under 'PlayType').
##      (Each team will have two bars.)  Your graph should match that given in
##      Graph 14.

PlayType_list = ['PASS','RUSH']
df_10 = df[df['PlayType'].isin(PlayType_list)]
p5 = sns.countplot(data=df_10, 
                   x='OffenseTeam',
                   hue='PlayType',
                   order=['BUF','DEN','IND','SF'])   
p5.set(xlabel='Team on Offense',              
       ylabel='Number of plays',
       title='Play type by team')






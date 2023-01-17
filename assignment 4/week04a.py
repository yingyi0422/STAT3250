##
## File: week04a.py (STAT 3250)
## Topic: Subsetting and Graphs
##

import pandas as pd # load pandas
import seaborn as sns # load seaborn

# Read in data from the 2021 UVA baseball season
df = pd.read_csv('virginia21.csv')

# Below we have a number of sample graphs

## Example 1
##
## Make a scatterplot of hits (x-axis) vs runs (y-axis) for the games where
## there were at least 14 players used.

# Extract sub-dataframe of games where at least 14 players are used
df1 = df[df['PlayersUsed'] >= 14]

# Use the dataframe df1 along with previously-seen methods for plotting
p1 = sns.relplot(data=df1, x='Hits', y='Runs')
p1.set(xlabel='Hits',
      ylabel='Runs Scored',
      title='Hits vs Runs (14 or more players used)')


## Example 2
##
## Make a histogram of ERA values for games where UVA was the Visitor

# Extract sub-dataframe of games where UVA is the visiting team
df2 = df[df['Location'] == 'Visitor']

# Use the dataframe df2 along with previously-seen methods for plotting
p2 = sns.displot(data=df2, x='ERA', binwidth=2)
p2.set(xlabel='ERA (per game)', 
      title='UVA ERA per game (Visitor only)',
      xticks=range(0,15,2))


## Example 3
##
## Make side-by-side boxplots for ERA, divided between Visitor and Home.

# This time we are using the entire data set, so there is no need for a
# sub-dataframe before plotting.

# the x-variable sets the boxplot categories; otherwise the same as before
p3 = sns.boxplot(data=df, x='Location', y='ERA',
                order=['Home','Visitor'])    
p3.set(xlabel='Location (home or away',
       ylabel='ERA (per game)',           
       title='ERA per game (home or away)')


## Example 4
##
## Make a scatterplot of hits (x-axis) vs runs (y-axis) for the games where
## UVA was home, with the points color-coded by opponent.

# Start by extracting the Home games into a separate dataframe
df4 = df[df['Location']=='Home']

# The only new argument is 'hue' which color-codes on 'Opponent'
p4 = sns.relplot(data=df4, x='Hits', y='Runs', 
                hue='Opponent')
p4.set(xlabel='Hits',
       ylabel='Runs Scored',
       xticks=range(1,15),
       yticks=range(1,18),
       title='Hits vs Runs, UVA Home Games')


## Example 5
##
## Make a side-by-side barplot of runs scored for home vs visitor, for only
## the opponents Notre Dame, Pittsburgh, Miami, Georgia Tech, Clemson, and
## Florida State.

# Extract the games for the listed opponents.  The funcion 'isin' returns a
# T/F series that is used to extra the indicated games.
opponentlist = ['Notre Dame','Pittsburgh','Miami','Georgia Tech','Clemson','Florida St']
df5 = df[df['Opponent'].isin(opponentlist)]

# We use the barplot function as before, but this time besides specifying 
# home or visitor, we get bars by opponent within those groupings with 'hue'
p5 = sns.barplot(data=df5, x='Location', y='Runs',
                  hue='Opponent',
                  ci=None,
                  order=['Home','Visitor'])   
p5.set(xlabel='Game Location',              
      ylabel='Average Runs Scored',
      title='Runs Scored by Opponent (home vs visitor)')

# We can fix the gaps by reorganizing the dataframe to put the home and 
# visitor games together.  Below we extract the games we want as before
# and then use the 'sort_values' function to sort forst by Location and 
# then by Opponent.
df5 = df5 = df[df['Opponent'].isin(opponentlist)].sort_values(by=['Location','Opponent'])

# Now we plot just as above
p5 = sns.barplot(data=df5, x='Location', y='Runs',
                  hue='Opponent',
                  ci=None,
                  order=['Home','Visitor'])   
p5.set(xlabel='Game Location',              
      ylabel='Average Runs Scored',
      title='Runs Scored by Opponent (home vs visitor)')

# We'll discuss how to change the location of the legend in another file.








##
## File: assignment12.py (STAT 3250)
## Topic: Assignment 12
##

##  For this assignment we revisit past men's NCAA basketball tournaments 
##  (including the glorious 2019 edition) using data from the file 
##
##      'ncaa.csv':  NCAA Men's Tournament Scores, 1985-2019
##
##  The organization of the file is fairly clear.  Each record has information
##  about one game, including the year, the teams, the final score, and each 
##  team's tournament seed.  

##  Two important points:
##    1) Each team is assigned a "seed" at the start of the tournament.  The
##       teams thought to be better are assigned smaller number seeds.  (So 
##       the best teams are assigned 1 and the worst assigned 16.)  In this 
##       assignment a "lower seed" refers to a worse team and hence larger 
##       seed number, with the opposite meaning for "higher seed". 
##    2) All questions refer only to the data in this in 'ncaa.csv' so you
##       don't need to worry about tournaments prior to 1985.

##  The data set is from Data.World, with the addition of the 2019
##  tournament provided by your dedicated instructors. 

##  Note: Most of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  Note: The coding methods required for this abbreviated assignment have
##  been covered in previous assignments, so there are no 'demo' files
##  with this assignment.


## 1.  Find all schools that have won the championship. Report your results in
##     a Series that has the schools as index and number of championships for
##     values, sorted alphabetically by school.

import pandas as pd 
import numpy as np
df = pd.read_csv('ncaa.csv')

championship = df[df['Region Name'] == 'Championship'] # subset the championship games 
championship['who_won'] = championship.loc[championship['Score'] > championship['Score.1'],'Team']
# create a column storing the champion schools
# if score > score.1, then fill in Team
championship.loc[championship['who_won'].isna(),'who_won'] = championship['Team.1'] # the onces that don't get filled out, we fill those by Team.1 
group1 = championship['who_won'].groupby(championship['who_won']).count() # groupby that column and count each school's number of championships 
q1 = group1.sort_index()  # Series of champions and counts


## 2.  Determine all schools that have been in the tournament at least 25 times.
##     Report your results as a Series with schools as index and number of times
##     in the tournament as values, sorted alphabetically by school.

round1 = df[df['Round'] == 1] # include teams in round 1 as each tournmanet appear counts as 1 only
round1 = pd.Series(round1[['Team','Team.1']].to_numpy().flatten()) # first subset the data to include only team and team.1, then convert to numpy to use the flatten() function 
group2 = round1.groupby(round1).count() # groupby on school names and find count 
q2 = group2[group2 >= 25].sort_index()  # Series of schools and tournament appearance counts


## 3.  Find all years when the school that won the tournament was seeded 
##     3 or lower. (Remember that "lower" seed means a bigger number!) Give  
##     a DataFrame with years as index and corresponding school and seed
##     as columns (from left to right).  Sort by year from least to most recent.

seed3 = df[df['Region Name'] == 'Championship'] # include only championship games 
seed3['who_won'] = df.loc[df['Score'] > df['Score.1'],'Team'] # only adding another seed column recording the winning team
seed3['who_won_seed'] = df.loc[df['Score'] > df['Score.1'],'Seed'] # same as question 1
seed3.loc[seed3['who_won'].isna(),'who_won'] = seed3.loc[seed3['who_won'].isna(),'Team.1']
seed3.loc[seed3['who_won_seed'].isna(),'who_won_seed'] = seed3.loc[seed3['who_won_seed'].isna(),'Seed.1']
group3 = seed3[seed3['who_won_seed'] >= 3] # subset winning teams with a seed of >= 3
group3.index = group3['Year'] # set index to year 
q3 = group3[['who_won','who_won_seed']].sort_index()  # DataFrame of years, schools, seeds


## 4.  Determine the average tournament seed for each school.  Make a Series
##     of all schools that have an average seed of 5.0 or higher (that is,
##     the average seed number is <= 5.0).  The Series should have schools
##     as index and average seeds as values, sorted alphabetically by
##     school

seedmean = pd.DataFrame() # cerate a dataframe
seedmean['team'] = pd.Series(df[['Team','Team.1']].to_numpy().flatten()) # expand team, team1
seedmean['seed'] = pd.Series(df[['Seed','Seed.1']].to_numpy().flatten()) # expand seed, seed1
seedmean['year'] = df['Year'].repeat(2).reset_index(drop = True) # repeat year 2 times and expand 
seedmean = seedmean.drop_duplicates() # then get unique items since each team is assigned 1 seed only in each year;
group4 = seedmean['seed'].groupby(seedmean['team']).mean() # group by team and find mean seed number 
q4 = group4[group4 <= 5].sort_index()  # Series of schools and average seed


## 5.  For each tournament round, determine the percentage of wins by the
##     higher seeded team. (Ignore games of teams with the same seed.)
##     Give a Series with round number as index and percentage of wins
##     by higher seed as values sorted by round in order 1, 2, ..., 6. 
##     (Remember, a higher seed means a lower seed number.)

winperp = df[df['Seed'] != df['Seed.1']] # filter out games where seed = seed.1
winperp['condition'] = 0 # create a column of 0s storing our condition 
winperp.loc[(winperp['Seed'] < winperp['Seed.1']) & (winperp['Score'] > winperp['Score.1']),'condition'] = 1 # if seed < seed.1 and team wins, we set 'condition' to 1
winperp.loc[(winperp['Seed.1'] < winperp['Seed']) & (winperp['Score.1'] > winperp['Score']),'condition'] = 1 # if seed.1 < seed and team.1 wins, we set'condition' to 1 
group5a = winperp['condition'].groupby(winperp['Round']).count().sort_index() # group by overall count for each round 
group5b = winperp['condition'].groupby(winperp['Round']).sum().sort_index() # group by number of fulfilled conditions for each round 
q5 = group5b / group5a*100  # Series of round number and percentage higher seed wins


## 6.  For each seed 1, 2, 3, ..., 16, determine the average number of games
##     won per tournament by a team with that seed.  Give a Series with seed 
##     number as index and average number of wins as values, sorted by seed 
##     number 1, 2, 3, ..., 16. (Hint: There are 35 tournaments in the data set
##     and each tournamentstarts with 4 teams of each seed.  We are not 
##     including "play-in" games which are not part of the data set.)

avggame = df.copy()
avggame['seed_won'] = 0 # record winning team's seed number in each game 
avggame.loc[avggame['Score'] > avggame['Score.1'],'seed_won'] = avggame.loc[avggame['Score'] > avggame['Score.1'],'Seed']
avggame.loc[avggame['Score'] < avggame['Score.1'],'seed_won'] = avggame.loc[avggame['Score'] < avggame['Score.1'],'Seed.1']
group6 = avggame['seed_won'].groupby(avggame['seed_won']).count() # group by seed_won and find count 
q6 = group6.sort_index()/140  # Series of seed and average number of wins
# divide by 140 to find avg and sort by index (seed number)

## 7.  For each year's champion, determine their average margin of victory 
##     across all of their games in that year's tournament. Find the champions
##     that have an average margin of victory of at least 15. Give a DataFrame 
##     with year as index and champion and average margin of victory as columns
##     (from left to right), sorted by from highest to lowest average victory 
##     margin.

margin = df.copy()
margin['who_won'] = margin.loc[margin['Score'] > margin['Score.1'],'Team'] # record the winning team's names 
margin.loc[margin['who_won'].isna(),'who_won'] = margin['Team.1']

champions = margin[margin['Region Name'] == 'Championship'] # champions stores the championship games

champions_games = pd.DataFrame() # create an empty data frame champions_games
# for each row: if the team wins a game and it is in the list of champions and belongs to the year when it won championship, add the game
for index, row in margin.iterrows():
    if row['Team'] in list(champions['who_won']) and row['Score'] > row['Score.1']:
        if row['Year'] in list(champions.loc[champions['who_won'] == row['Team'], 'Year']):
            champions_games = champions_games.append(row)
    elif row['Team.1'] in list(champions['who_won']) and row['Score.1'] > row['Score']: # do the same steps for Team.1 
        if row['Year'] in list(champions.loc[champions['who_won'] == row['Team.1'], 'Year']):
            champions_games = champions_games.append(row)
        
champions_games['margin_of_victory'] = abs(champions_games['Score'] - champions_games['Score.1']) # then find margin of victory 

group7 = champions_games['margin_of_victory'].groupby([champions_games['Year'].astype(int),champions_games['who_won']]).mean() # then group margin of victory by year and team name and find avg 
group7 = group7[group7 >= 15].sort_values(ascending=False) # filter out teams with mov < 15 and sort by mov in descending order 
# reset index to have team name as a column
q7 = group7.reset_index()  # DataFrame of years, schools, average margin of victory
q7.index = q7['Year'] # set index to year 
q7 = q7.iloc[:,1:] # removes year column


## 8.  Determine the 2019 champion.  Use code to extract the correct school,
##     not your knowledge of college backetball history.

school = df[(df['Year'] == 2019) & (df['Region Name'] == 'Championship')] # filter the exact game 
if int(school['Score']) > int(school['Score.1']): # since we only have one row, if-else is enough to extract the team name 
    q8 = school['Team'].squeeze() # use .squeeze() to extract element from 1x1 dataframe 
else:
    q8 = school['Team1'].squeeze()  # 2019 champion!








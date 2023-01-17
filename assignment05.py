##
## File: assignment05.py (STAT 3250)
## Topic: Assignment 5
##

##  This assignment requires the data file 'assignment05-data.csv'.  This file
##  contains records of over 14000 tweets and associated information related
##  to a number of airlines.  You should be able to read this file in using
##  the usual pandas methods.

##  Gradescope will run your code on a version of assignment05-data.csv
##  that has had about 55% of the records removed.  You will need to write
##  your code in such a way that your file will automatically produce the
##  correct answers on the new set of data.  

## Two *very* important rules that must be followed in order for your assignment
## to be graded correctly:
##
## a) The Python file name must be exactly "assignment05.py" (without the quotes)
## b) The variable names q1, q2, ... must not be changed.  These variable 
##    names should not be used anywhere else in your file.  Do not delete these
##    variables. If you don't know how to find a value for a variable, just  
##    leave the corresponding variable with "= None". (If any variable is     
##    missing the autograder will not grade your assignment.)


## Questions 1-7: These questions should be done without the use of loops.

## 1.  Determine the number of tweets for each airline, indicated by the
##      name in the 'airline' column of the data set.  Give the airline 
##      name and corresponding number of tweets as a Series with airline
##      name as the index, sorted by tweet count from most to least.

import pandas as pd #import pandas
import numpy as np #import numpy
df = pd.read_csv('assignment05-data.csv') #import dataframe and name it df

group1 = df['airline'].groupby(df['airline']) #group the data in the column 
# "airline" based on the entries in column "airline"
count1 = group1.count().sort_values(ascending = False) # sorted by tweet from most to 
#least
q1 = count1  # Series of airlines and number of tweets

## 2.  For each airline's tweets, determine the percentage that are negative
##      based on the classification in 'airline_sentiment'.  Give the airline 
##      name and corresponding percentage as a Series with airline
##      name as the index, sorted by percentage from smallest to largest.

group2 = df[df['airline_sentiment'] == 'negative'] # to obtain tweets that are 
#negative
group2 = group2['airline_sentiment'].groupby(group2['airline']) #group the data
#in column airline_sentiment based on the name of the airlines
q2 = (group2.count() / count1 * 100).sort_values(ascending = False) # Series of airlines 
# and percentage of negative tweets

## 3.  Find all user names (in the 'name' column) with at least 12 tweets
##      along with the number of tweets for each.  Give the user names and
##      corresponding counts as a Series with user name as index, sorted
##      by count from largest to smallest

group3 = df['name'].groupby(df['name']) #group the data in column name based on
#name
count3 = group3.count()[group3.count() >= 12].sort_values(ascending = False) #sort the entries

q3 = count3  # Series of users with at least 12 tweets

## 4.  Determine the percentage of tweets from users who have 4 or more 
##      tweets in this data set. (Note that this is not the same as 
##      the percentage of users with 4 or more tweets.)

group4 = df['name'].groupby(df['name']) #group the data in column name based on
#name
q4 = group4.count()[group3.count()>=4].sum()/group4.count().sum() * 100 # Percentage of 
#tweets from users with 4 or more tweets                            

## 5.  Among the negative tweets, determine the four reasons are the most common.
##      Give the percentage among all negative tweets for each as a Series 
##      with reason as index, sorted by percentage from most to least

group5 = df[df['airline_sentiment'] == 'negative'] #to obtain tweets that are 
#negative
count5 = df['airline_sentiment'].count() #count all the reasons
count5a = group5['airline_sentiment'].groupby(group5['negativereason']).count() 
#count the negative tweets
q5 = (count5a / count5 * 100).sort_values(ascending = False).iloc[0:4] 
# Series of reasons and percentages

## 6.  How many tweets include a link to a web site? (Indicated by the 
##      presence of "http" anywhere in the tweet.)

q6 = np.sum(df['text'].str.contains('http')) # Number of tweets that include a link

## 7.  How many tweets include the word "gate" (upper or lower case,
##      not part of another word)?

tweet = (" " + df['text'].str.lower() + " ").str.replace(r'[^\w\s]+', ' ')
#change the tweets to lower case and then add space and remove weird marks
q7 = np.sum(tweet.str.contains(' gate '))   # Number of tweets that include 'gate'

## Questions 8-12: Some of these questions can be done without the use of 
##  loops, while others cannot.  It is preferable to minimize the use of
##  loops where possible, so grading will reflect this.
##
##  Some of these questions involve hashtags and @'s.  These are special 
##  Twitter objects subject to special rules.  For these problems we assume
##  that a "legal" hashtag:
##
##  (a) Starts with the "#" (pound) symbol, followed by letter and/or numbers 
##       until either a space or punctuation mark (other than "#") is encountered.
##   
##      Example: "#It'sTheBest" produces the hashtag "#It"
##
##  (b) The "#" symbol can be immediately preceded by punctuation, which is 
##       ignored. If "#" is immediately preceded by a letter or number then
##       it is not a hashtag.
##
##      Examples: "The,#dog,is brown"  produces the hashtag "#dog"
##                "The#dog,is brown" does not produce a hashtag
##                "#dog1,#dog2" produces hashtags "#dog1" and "#dog2"
##                "#dog1#dog2" produces the hashtag "#dog1#dog2"
##
##  (c) Hashtags do not care about case, so "#DOG" is the same as "#dog"
##       which is the same as "#Dog".
##
##  (d) The symbol "#" by itself is not a hashtag
##
##  The same rules apply to Twitter handles (user names) that begin with the
##   "@" symbol.         

##  8.  How many of the tweets have at least three Twitter handles?

tweet = (" " + df['text'].str.lower() + " ").str.replace(r'[^\w\s@]+', ' ')
##change the tweets to lower case and then add space and remove weird marks
df['count8'] = tweet.str.count(' @') - tweet.str.count(' @ ') 
#to add a new column and assign the value
q8 = len(df[df['count8']>=3]) # number of tweets with at least three Twitter handles

##  9. Suppose that a score of 4 is assigned to each positive tweet, 1 to
##      each neutral tweet, and -3 to each negative tweet.  Determine the
##      mean score for each airline and give the results as a Series with
##      airline name as the index, sorted by mean score from highest to lowest.

df['score'] = 1 #create an empty column
df.loc[df['airline_sentiment'] == 'positive','score'] = 4 #score of 4 assigned 
#to entries with positive tweet
df.loc[df['airline_sentiment'] == 'negative','score'] = -3 #score of -3 assigned
#to entries with negative tweet
q9 = df['score'].groupby(df['airline']).mean().sort_values(ascending = False) 
 # Series of airlines and mean scores 

## 10. What is the total number of hashtags in tweets associated with each
##      airline?  Give a Series with the airline name as index and the
##      corresponding totals for each, sorted from least to most.

tweet = (" " + df['text'].str.lower() + " ").str.replace(r'[^\w\s#]+', ' ') 
#change the tweets to lower case and then add space and remove weird marks
df['count_hashtag'] = tweet.str.count(' #') - tweet.str.count(' # ')
 #create a column hashtag and assign the value we get
q10 = df['count_hashtag'].groupby(df['airline']).sum().sort_values(ascending = True) 
# Series of airlines and hashtag counts

## 11. Among the tweets that "@" a user besides the indicated airline, 
##      find the percentage including an "@" directed at the other airlines 
##      in this file. (You can assume a tweet associated with an airline
##      has an "@" directed at that airline, so you need just check if 
##      there is also an "@" directed at one of the other airlines.)

tweet1 = (" " + df['text'].str.lower() + " ").str.replace(r'[^\w\s@]+', ' ') 
#change the tweets to lower case and then add space and remove weird marks
count_11 = np.sum((tweet1.str.count(' @') - tweet1.str.count(' @ ')) > 1)
count_airlines = pd.Series(['@united',
                            '@virginamerica',
                            '@jetblue',
                            '@southwestair',
                            '@usairways',
                            '@americanair']) # to obtain the list of airlines
n = np.zeros(len(df)) #create a 0 array
for c in count_airlines: #loop through each airline
    n = n + 1 * tweet1.str.contains(" " + c + " ")
q11 = (np.sum(n > 1) / count_11) * 100  # Percentage of tweets "@" another airline

## 12. Suppose the same user has two or more tweets in a row, based on how they 
##      appear in the file. For such tweet sequences, determine the percentage
##      for which the most recent tweet (which comes nearest the top of the
##      file) is a positive tweet.

count_total = 0 #create count_total
count_positive = 0 #create tweets that are in a row and are positive
multi_tweet = df[["name","airline_sentiment"]] #pick the two variables from the frame
for i in range(len(multi_tweet) - 1): #start the loop
    if i == 0 and df.loc[i,"name"] == df.loc[i+1, 'name']: #if the two name in a row are the same
        count_total += 1 #total count +1
        if df.loc[i,"airline_sentiment"] == 'positive': #if it is a positive tweet
            count_positive += 1 #positive count+1
            
    if i != 0 and df.loc[i,'name'] == df.loc[i+1,'name'] and df.loc[i,'name'] != df.loc[i-1, 'name']:
        count_total += 1 #after the 1st and the 2nd row, it goes into this loop
        if df.loc[i,"airline_sentiment"] == 'positive':
            count_positive += 1 #same as above
        
q12 = count_positive / count_total * 100  # Percentage of tweet sequences starting with positive tweet



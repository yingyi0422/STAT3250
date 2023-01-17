##
## File: assignment10.py (STAT 3250)
## Topic: Assignment 10 
##

##  For this assignment you will be working with Twitter data related to the
##  opening of final Game of Thrones season on April 14, 2019.  You will use 
##  a set of over 10,000 tweets for this purpose.  The data is in the file 
##  'assignment10-data.txt'.  

##  Note: On this assignment it is fine to use loops to extract information
##  from the tweets. Have fun.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the GoTtweets.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  

##  Note: See the file week010a.py for the code to read in the data.  That
##  will make the assignment much easier than trying to read the data in as
##  straight text.


## 1.  The tweets were downloaded in several groups at about the same time.
##     Are there any that appear in the file more than once?  Give a Series 
##     with the tweet ID for any repeated tweets as the index and the number 
##     of times each ID appears in the file as values.  Sort by the index from
##     smallest to largest.

import pandas as pd #import pandas
import numpy as np #import numpy
import json #import json

# Read in the tweets and append them to 'tweets'
tweets = []
with open('assignment10-data.txt') as f: # Open the file
    for line in f:
        tweets.append(json.loads(line)) # Add to 'tweets' after converting
# for each dict, find the value associated with key 'id_str', append all of them into a pd series
rep = pd.Series(tweet['id_str'] for tweet in tweets)
# group by 'id_str' and find count
group1 = rep.groupby(rep).count()
# include those with count > 1 and sort by 'id_str' in ascending order
q1 = group1[group1 > 1].sort_index() # Series of tweet IDs that appear > 1 time

## Note: For the remaining questions in this assignment, do not worry about 
##       any duplicate tweets.  Just answer the questions based on the 
##       existing data set.
    

## 2.  Determine the number of tweets that include 'Daenerys' (any combination
##     of upper and lower case; part of another word OK) in the text of the 
##     tweet.  Then do the same for 'Snow'.

# find all 'text'
text = pd.Series(tweet['text'] for tweet in tweets)
# turn them all into lower case and find if they contain the keyword
q2a = sum(text.str.lower().str.contains('daenerys'))  # number of tweets including 'daenerys'
q2b = sum(text.str.lower().str.contains('snow'))  # number of tweets including 'snow'

## 3.  Find the average number of hashtags included in the tweets. (You may get 
##     the wrong answer if you use the text of the tweets instead of the
##     hashtag lists, so use those.)

# find all hashtag lists, then find the length of list of hashtag in each tweet
average = pd.Series(len(tweet['entities']['hashtags']) for tweet in tweets)
q3 = np.mean(average)  # average number of hashtags per tweet
 
## 4.  Determine the number of tweets that have 0 hashtags, 1 hashtag, 2 hashtags,
##     and so on.  Give your answer as a Series with the number of hashtags
##     as index (sorted smallest to largest) and the corresponding number of
##     tweets as values. Include in your Series index only the number of   
##     hashtags that occur for at least one tweet, so for instance, if there
##     are no tweets with 12 hashtags then 12 should not appear as an index
##     entry. (Note: Also see warning in #3)

# find all hashtags per tweet like the last question
hashtag = pd.Series(len(tweet['entities']['hashtags']) for tweet in tweets)
# groupby the lengths of the hashtag lists, find count, and sort by index in ascending order 
q4 = hashtag.groupby(hashtag).count().sort_index()  # Series of number of hashtags and counts

## 5.  Determine the number of tweets that include the hashtag '#GoT', then
##     repeat for '#GameofThrones'.  (You may get the wrong answer if you
##     use the text of the tweets instead of the hashtag lists.)
##     Note: Hashtags are not case sensitive, so any of '#GOT', '#got', 'GOt' 
##     etc are all considered matches so should be counted.

hashtag1 = [tweet['entities']['hashtags'] for tweet in tweets]
# find all hashtags
got_list = pd.Series() # create two empty series
gameofthrones_list = pd.Series()
for i in hashtag1:
    got = 0 # first set the counters to be 0
    gameofthrones = 0
    for j in i: 
        if j['text'].lower() == 'got': # check if its lower-case equals to 'got' or 'gameofthrones' 
            got += 1 # plus one if yes
        if j['text'].lower() == 'gameofthrones':
            gameofthrones += 1 # do the same thing for gameofthrone
    got_list = got_list.append(pd.Series(got)) # add our counter to the empty series and restore the counter to 0
    gameofthrones_list = gameofthrones_list.append(pd.Series(gameofthrones))
    
q5a = sum(got_list > 0)  # number of tweets with '#GoT' hashtag and upper/lower variants               
q5b = sum(gameofthrones_list > 0)  # number of tweets with '#GameofThrones' hashtags and upper/lower variants             

## 6.  Some tweeters like to tweet a lot.  Find the screen name for all 
##     tweeters with at least 3 tweets in this data.  Give a Series with 
##     the screen name (in lower case) as index and the number of tweets as 
##     value, sorting by the index in alphabetical order.  

#find all screen names in lower case
screen = pd.Series(tweet['user']['screen_name'] for tweet in tweets).str.lower()
# group by screen names and find the count
group6 = screen.groupby(screen).count()
q6 = group6[group6 >= 3].sort_index() # Series of screen name and counts

## 7.  Among the screen names with 3 or more tweets, find the average
##     'followers_count' for each and then give a table with the screen  
##     and average number of followers.  (Note that the number of
##     followers might change from tweet to tweet.)  Give a Series with
##     screen name (in lower case) as index and the average number of followers  
##     as value, sorting by the index in alphabetical order.  

follower = pd.DataFrame() # create a data frame
# find all screen names in lower case
follower['screen_name'] = [tweet['user']['screen_name'].lower() for tweet in tweets]
# find follower counts
follower['followers'] = [tweet['user']['followers_count'] for tweet in tweets]
# groupby mean on followers
group7 = follower['followers'].groupby(follower['screen_name']).agg(['count', 'mean'])
q7 = group7.loc[group7['count'] >= 3, 'mean'].sort_index()  # Series of screen names and mean follower counts  
                                                                
## 8.  Determine the hashtags that appeared in at least 50 tweets.  Give
##     a Series with the hashtags (lower case) as index and the corresponding 
##     number of tweets as values, sorted alphabetically by hashtag.

# find all hashtags
hashtag2 = pd.Series(tweet['entities']['hashtags'] for tweet in tweets)
#create a series
group8 = pd.Series()

for hashtags in hashtag2:
    unique = [] # check if the lower-case version is in the unique[] we set up to avoid duplicates
    for hashtag in hashtags:
        if hashtag['text'].lower() not in unique:
            unique.append(hashtag['text'].lower())
            if hashtag['text'].lower() in group8.index: # check if the hashtag is an index in group8
                group8[hashtag['text'].lower()] += 1 # if yes, then plus one
            else: 
                group8[hashtag['text'].lower()] = 1 # if not, then remains 1
                
q8 = group8[group8 >= 50].sort_index()  # Series of hashtags and counts

##  9.  Some of the tweets include the location of the tweeter.  Give a Series
##      of the names of countries with at least three tweets, with country 
##      name as index and corresponding tweet count as values.  Sort the
##      Series alphabetically by country name.
##      Note: Treat different spellings as different countries, even if they
##      appear to be referring to the same country.

# find all the places and drop NA values
country = pd.Series(tweet['place'] for tweet in tweets).dropna()
# find all the countries 
country = pd.Series(tweet['country'] for tweet in country)
# group by countries and find the count
group9 = country.groupby(country).count()
q9 = group9[group9 >= 3].sort_index() # Series of countries with at least three tweets

## Questions 10-11: The remaining questions should be done using regular 
##                  expressions as described in the sample Python files.

## 10.  Determine the percentage of tweets (if any) with a sequence of 3 or more
##      consecutive digits.  (Nothing between the digits!)  For such tweets,
##      apply 'split()' to create a list of substrings.  Among all the 
##      substrings that have a sequence of at least three consecutive digits,
##      determine the percentage where the substring starts with a '@' at the 
##      beginning of the substring.

# find all tweets
alltext = pd.Series(tweet['text'] for tweet in tweets)
# find tweets that contains 3 or more consecutive digits
three_or_more = alltext[alltext.str.contains("[0-9]{3,}", regex=True)]
# put tweets that contains 3 or more consecutive digits into columns, whih is three_or_more2, then  convert into numpy. Then flatten and drop NA values
three_or_more2 = pd.Series(three_or_more.str.split(' ', expand=True).to_numpy().flatten()).dropna()
# get the substring that contains all substrings that have 3 or more consecutive digits 
substring_three = three_or_more2[three_or_more2.str.contains("[0-9]{3,}", regex=True)]
# get the substring that contains all substrings that have 3 or more consecutive digits and also start with '@'
substring_tag = substring_three[substring_three.str.contains("^@", regex=True)]

q10a = len(three_or_more)/len(alltext)*100 # percentage of tweets with three consecutive digits
q10b = len(substring_tag)/len(substring_three)*100  # percentage starting with @ among substrings with 3 consec digits

## 11.  Determine if there are any cases of a tweet with a 'hashtag' that is
##      actually not a hashtag because there is a character (letter or digit)
##      immediately before the "#".  An example would be 'nota#hashtag'.
##      Count the number of tweets with such an incorrect 'hashtag'.

# find all tweets again
alltext1 = pd.Series(tweet['text'] for tweet in tweets)
# find any cases of a tweet with a 'hashtag' that is actually not a hashtag because there is a character
hashtag_wrong = alltext1[alltext1.str.contains('[a-zA-Z0-9][#]', regex=True)]
q11 = len(hashtag_wrong)  # count of tweets with bad hashtag





##
## File: assignment09.py (STAT 3250)
## Topic: Assignment 9
##

##  This assignment requires data from three files: 
##
##      'assignment09-data1.txt':  A file of over 1,000,000 movie ratings
##      'assignment09-data2.txt':  A file of over 6000 reviewers who provided ratings
##      'assignment09-data3.txt':  A file of nearly 3900 movies
##
##  The file 'README-09.txt' has more information about these files.
##  You will need to consult the readme file to answer some of the questions.

##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the movies.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  


## It is recommended that you read in the data sets in the manner shown below.
ratingtext = open('assignment09-data1.txt', encoding='utf8').read().splitlines()
reviewertext = open('assignment09-data2.txt', encoding='utf8').read().splitlines()
movietext = open('assignment09-data3.txt', encoding='utf8').read().splitlines()
import pandas as pd #import pandas

## 1.  Based on the data in 'assignment09-data2.txt': Determine the percentage of all 
##     reviewers that are female.  Determine the percentage of all reviewers in
##     the 35-44 age group.  Among the 18-24 age group, find the percentage 
##     of reviewers that are male.

reviewers = pd.Series(reviewertext).str.split('::',expand=True) # first split the string list by :: and make it into a dataframe
reviewers.columns = ['Reviewer_ID','Gender','Age','Occupation','Zipcode','State'] # name the columns accordingly

Gender = reviewers['Gender'] # gender will then include all the genders in the gender column of the dataframe
q1a = len(Gender[Gender == 'F']) / len(Gender) * 100  # percentage of female reviewers

Age = reviewers['Age'] # Age will then include all the ages in the age column
q1b = len(Age[Age == '35']) / len(Age) * 100  # percentage age 35-44

Age18 = reviewers[reviewers['Age'] == '18'] # Age18 will then include all reviewers in the 18-24 age group
q1c = len(Age18[Age18['Gender'] == 'M']) / len(Age18) * 100  # percentage of males reviewers in 18-24 age group

## 2.  Give a year-by-year Series of counts for the number of ratings, with
##     the rating year as index and the counts as values, sorted by rating
##     year in ascending order.

ratings = pd.Series(ratingtext).str.split('::',expand=True) #like the last question, split by :: and make ratingtext into a dataframe
ratings.columns = ['Reviewer_ID','Movie_ID','Rating','Timestamp'] # rename the columns

ratings['Rating'] = ratings['Rating'].astype(int) #convert the ratings into integers
Year = pd.to_datetime(ratings['Timestamp'], unit='s').dt.year #convert timestamp to datetime and take out the year portion by using .dt.year
q2 = Year.groupby(Year).count().sort_index() # Series of rating counts by year rated

## 3.  Determine the average rating from female reviewers and the average  
##     rating from male reviewers.

avg_rating = pd.merge(ratings, reviewers, on = 'Reviewer_ID') # Merge ratings and reviewers dataframes by the Reviewer_ID column
q3a = avg_rating.loc[avg_rating['Gender'] == 'F','Rating'].mean() # average rating for female reviewers
q3b = avg_rating.loc[avg_rating['Gender'] == 'M','Rating'].mean() # average rating for male reviewers

## 4.  Determine the number of movies that received an average rating of 
##     less than 1.75.  (Movies and remakes should be considered as
##     different.)

movies = pd.Series(movietext).str.split('::',expand=True) # do the same thing for the movie stringlist, convert it into a dataframe and separate the columns by ::
movies.columns = ['Movie_ID','Title','Genre'] # name the columns

sum(movies['Movie_ID'].value_counts() > 1) # combines all movies IDs
rating1 = ratings['Rating'].groupby(ratings['Movie_ID']).mean() #group rating by movie ID
q4 = len(rating1[rating1 < 1.75])  # count of number with average rating less than 1.75

## 5.  Determine the number of movies listed in movies data for which there
##     is no rating in ratings data.  

# unique() gives us the number of movies rated
q5 = len(movies) - len(ratings['Movie_ID'].unique())  # number of movies that were not rated

## 6.  Among the ratings from male reviewers, determine the average  
##     rating for each occupation classification (including 'other or not 
##     specified'), and give the results in a Series sorted from highest to 
##     lowest average with the occupation title (not the code) as index.

rating_reviewer = pd.merge(ratings, reviewers, on = 'Reviewer_ID') #merge ratings and reviewers
rating_reviewer = rating_reviewer[rating_reviewer['Gender'] == 'M'] # sort out the reviewers that are male
male_reviewer = rating_reviewer['Rating'].groupby(rating_reviewer['Occupation'].astype(int)).mean().sort_index()
# group ratings of these male reviewers by occupation and find the mean
male_reviewer.index = ['other','academic/educator','artist','clerical/admin','college/grad student','customer service','doctor/health care',
                     'executive/managerial','farmer','homemaker','K-12 student','lawyer','programmer','retired','sales/marketing','scientist',
                     'self-employed','technician/engineer','tradesman/craftsman','unemployed','writer']
# manually duplicate the index
q6 = male_reviewer.sort_values(ascending = False) # Series of average ratings by occupation

## 7.  Determine the average rating for each genre, and give the results in
##     a Series with genre as index and average rating as values, sorted 
##     alphabetically by genre.

genres = movies['Genre'].str.split('|', expand = True) #split the genre by | and make it a list of genres
genres = pd.Series(genres.to_numpy().flatten()).dropna().unique() #merge into a single column of genres, drop NA values and find the unique values
movie_rating = pd.merge(ratings, movies, on = 'Movie_ID') #then merge ratings and movies
genre_rating = pd.Series() #creat an empty serie
# for each i in the loop, we take the mean of rating for each genre in the movie_rating list, and then append to the genre_rating list
for i in genres: 
    rating_genres = pd.Series(movie_rating.loc[movie_rating['Genre'].str.contains(i),'Rating'].mean(),index = [i])
    genre_rating = genre_rating.append(rating_genres)

q7 = genre_rating.sort_index()  # Series of average rating by genre   

## 8.  For the reviewer age category, assume that the reviewer has age at the 
##     midpoint of the given range.  (For instance '35-44' has age (35+44)/2 = 39.5)
##     For 'under 18' assume an age of 16, and for '56+' assume an age of 60.
##     For each possible rating (1-5) determine the average age of the reviewers
##     giving that rating.  Give your answer as a Series with rating as index
##     and average age as values, sorted by rating from 1 to 5.

reviewer_age = pd.merge(ratings, reviewers, on = 'Reviewer_ID') # first merge rating and reviewer on reviewer_id 
# Change the age groups to proper midpoint ages by adding the minimum and maximum, then divide by 2. No need to change 16 and 60
reviewer_age.loc[reviewer_age['Age']=='1','Age'] = 16
reviewer_age.loc[reviewer_age['Age']=='18','Age'] = (18+24)/2
reviewer_age.loc[reviewer_age['Age']=='25','Age'] = (25+34)/2
reviewer_age.loc[reviewer_age['Age']=='35','Age'] = (35+44)/2
reviewer_age.loc[reviewer_age['Age']=='45','Age'] = (45+49)/2
reviewer_age.loc[reviewer_age['Age']=='50','Age'] = (50+55)/2
reviewer_age.loc[reviewer_age['Age']=='56','Age'] = 60
# group age by rating then take the mean value, and sort from 1 to 5
q8 = reviewer_age['Age'].groupby(reviewer_age['Rating']).mean().sort_index()  # Series of average age by rating

## 9.  Find the top-5 "states" in terms of average rating.  Give as a Series
##     with the state as index and average rating as values, sorted from 
##     highest to lowest average rating. (Include any ties as usual)
##     Note: "states" includes US territories and military bases. See the 
##     readme.txt file for more information on what constitutes a "state"
##     for this assignment.

reviewer_rating = pd.merge(ratings, reviewers, on='Reviewer_ID') # again merge ratings and reviewers
reviewer_rating = reviewer_rating[reviewer_rating['State'] != 'Unknown'] #sort out rows with state not equivalent to "Unknown"
# group ratings by state, and take the five largest values
q9 = reviewer_rating['Rating'].groupby(reviewer_rating ['State']).mean().nlargest(5, keep='all')  # top-5 states by average rating


## 10. For each age group, determine the occupation that gave the lowest 
##     average rating.  Give a Series that includes the age group code and 
##     occupation title as a multiindex, and average rating as values.  Sort  
##     the Series by age group code from youngest to oldest. 
# create a dictionary storing occupation id and the job title
occupation_dict = {'0':'other','1':'academic/educator','2':'artist','3':'clerical/admin','4':'college/grad student',
                   '5':'customer service','6':'doctor/health care','7':'executive/managerial','8':'farmer','9':'homemaker',
                   '10':'K-12 student','11':'lawyer','12':'programmer','13':'retired','14':'sales/marketing','15':'scientist',
                   '16':'self-employed','17':'technician/engineer','18':'tradesman/craftsman','19':'unemployed','20':'writer'}

reviewer_rating1 = pd.merge(ratings, reviewers, on='Reviewer_ID') # merge rating and reviewer on reviewer_id 
reviewer_rating1 = reviewer_rating1.replace({'Occupation': occupation_dict}) # replace our reviewer_rating1's occupation column with .replace(), 
# occupation ids are matched with the dictionary's keys, and the values are replaced
# find avg ratings grouped by age and occupation 
avg_rating1 = reviewer_rating1['Rating'].groupby([reviewer_rating1['Age'].astype(int),reviewer_rating1['Occupation']]).mean() 
# then get the minimum avg ratings grouped by ages, and sort the age in ascending order
q10 = avg_rating1.groupby('Age', group_keys=False).nsmallest(1).sort_index(level=0)  # Series of average ratings by age code and occupation title





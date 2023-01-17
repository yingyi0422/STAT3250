##
## File: assignment08.py (STAT 3250)
## Topic: Assignment 8 
##

##  This assignment requires the data file 'assignment08-data.txt'.  This file
##  contains records for nearly 3900 movies, including a movie ID number, 
##  the title (with year of release, which is not part of the title), and a 
##  list of movie genre classifications (such as Romance, Comedy, etc).  Note
##  that a given movie can be classified into more than one genre -- for
##  instance Toy Story is classified as "Animation", "Children's", and 
##  "Comedy".

##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the movies.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  

import numpy as np # load numpy as np
import pandas as pd # load pandas as pd

# Read in the movie data as text; leave in encoding = 'utf8'
movielines = open('assignment08-data.txt', encoding = 'utf8').read().splitlines()
movies = pd.Series(movielines).str.split('::',expand = True) # split the list into a df with columns separated by ::
movies.columns = ['ID','Title','Genre'] #renames the columns as ID, Title, and Genre

## 1.  Determine the number of movies included in genre "Animation", the number
##     in genre "Horror", and the number in both "Comedy" and "Crime".
# q1a: sum the number of movies which their genre contain animation, case sentitive matching
# q1b: sum the number of movies which their genre contain horror, case sensitive matching
q1a = np.sum(movies['Genre'].str.contains('Animation',case = False))  # Genre includes Animation
q1b = np.sum(movies['Genre'].str.contains('Horror',case = False))  # Genre includes Horror
q1c = np.sum((movies['Genre'].str.contains('Comedy').astype(int) + movies['Genre'].str.contains('Crime').astype(int)) == 2) # Genre includes both Comedy and Crime
# q1c: sum the number of movies that contain comedy and crime

## 2.  Among the movies in the genre "Horror", what percentage have the word
##     "massacre" in the title?  What percentage have 'Texas'? (Upper or lower
##     cases are allowed here.) 

horror = movies.loc[movies['Genre'].str.contains('Horror',case = False)] #create a df horror which includes movies with the genre horror
q2a = sum(horror['Title'].str.contains('Massacre',case = False)) / len(horror) * 100  # percentage in Horro that includes 'massacre'
q2b = sum(horror['Title'].str.contains('Texas',case = False)) / len(horror) * 100  # percentage in Horro that includes 'texas'

## 3.  Among the movies with exactly one genre, determine the genres that
##     have at least 50 movies classified with that genre.  Give a Series 
##     with genre as index and counts as values, sorted largest to smallest 
##     by count.

onegenre = movies.loc[movies['Genre'].str.contains('|',regex = False) == False] #sort out all the movies with just one genre
moviegenre = onegenre['Genre'].groupby(onegenre['Genre']).count() #groupby movies by genre
q3 = moviegenre[moviegenre >= 50].sort_values(ascending = False) # Series of genres for at least 50 movies and counts

## 4.  Determine the number of movies that have 1 genre, the number that have
##     2 genres, the number that have 3 genres, and so on. Give your results
##     in a Series, with the number of genres as the index and the counts as
##     values, sorted by index entries from smallest to largest. 

genres = movies['Genre'].str.split('|',expand = True) #separate genres by |
genres = (genres.isna() == False).astype(int) #assign 0 to NA values, then assign 1 to each genre on the same axis
genres = genres.sum(axis = 1) #sum the number of genres in each row
q4 = genres.groupby(genres).count().sort_index()  # Series of number of genres and counts


## 5.  How many remakes are in the data? We say a movie is a remake if the 
##     title is exactly the same as the title of an older movie.  Note that
##     the movie release year (in parenthesis) is not part of the title.
##     For instance, if 'Hamlet' is in the data set 4 times then 3 of those 
##     should be counted as remakes.
##     (Note that a sequel is not the same as a remake -- "Jaws 2" is not a 
##     remake of "Jaws".)

titles = movies['Title'].str[:-6] #delete the last six spaces in the title, which is to delete the year part
alltitles = titles.groupby(titles).count() #group titles by titles
q5 = (alltitles[alltitles >= 2] - 1).sum() # number of remakes in data set
# the observations that repeat twice would be a remake, and we minus one to get the number of remakes, then sum all the remakes

## 6.  Determine for each genre the percentage of movies in the data set that
##     are classified as that genre.  Give a Series of all with 8% or more,
##     with genre as index and percentage as values, sorted from highest to 
##     lowest percentage. 

genres1 = movies['Genre'].str.split('|',expand=True) #separates the genres by |
genrecount = genres1.apply(pd.Series).stack().reset_index(drop = True) #convert to a series, then use the stack function to convert all the genres into one column
q6 = genrecount.value_counts() / len(movies) * 100  #get the percentage
q6 = q6[q6 >= 8].sort_values(ascending = False) # Series of genres and percentages


## 7.  It is thought that musicals have become less popular over time.  We 
##     judge that assertion here as follows: Compute the median release year 
##     for all movies that have genre "Musical", and then do the same for all
##     other movies.  

# musical: find all the observations with genre as musical, slice to get the release year
# then do the same for nonmusicals
musical = (movies.loc[movies['Genre'].str.contains('Musical',case = False),'Title'].str[-5:-1]).astype(int)
nonmusical = (movies.loc[movies['Genre'].str.contains('Musical',case = False) == False,'Title'].str[-5:-1]).astype(int)
q7a = np.median(musical)  # median release year for Musical
q7b = np.median(nonmusical) # median release year for non-Musical 

##  8. Determine how many movies came from each decade in the data set.
##     An example of a decade: The years 1980-1989, which we shall label as
##     1980.  (Use this convention for all decades in the data set.) 
##     Give your answer as a Series with decade as index and counts as values,
##     sorted by decade 2000, 1990, 1980, ....

decade = movies['Title'].str[-5:-1].astype(int) // 10*10 # // to get the whole number and times 10 to get what we want
q8 = decade.groupby(decade).count().sort_index(ascending = False)  # Series of decades and counts


##  9. For each decade in the data set, determine the percentage of titles
##     that have exactly one word.  (Note: "Jaws" is one word, "Jaws 2" is not)
##     Give your answer as a Series with decade as index and percentages as values,
##     sorted by decade 2000, 1990, 1980, ....
##     Note: There are some titles that include an alternate version, usually
##     a translation.  Treat this as part of the title for this question so
##     that (for example) "Anatomy (Anatomie)" has two words.

onetitle = movies.copy() # duplicate movies
onetitle['Decade'] = onetitle['Title'].str[-5:-1].astype(int) // 10*10 # create a decade column
word = onetitle[onetitle['Title'].str.count(' ') == 1] # sort out the movies with only one word
one_word = word['Decade'].groupby(word['Decade']).count().sort_index(ascending=False) # group decade by decades and count the sum of movies
q9 = (one_word / onetitle['Decade'].groupby(onetitle['Decade']).count().sort_index(ascending=False) * 100).fillna(0).sort_index(ascending = False) # Series of percentage 1-word titles by decade 


## 10. For each genre, determine the percentage of movies classified in
##     that genre also classified in at least one other genre.  Give your 
##     answer as a Series with genre as index and percentages as values, 
##     sorted largest to smallest percentage.

genres2 = movies['Genre'].str.split('|',expand=True) # separates the genres by |
genres2 = pd.Series(genres2.to_numpy().flatten()).dropna().unique() # Split genre into columns and flatten the genres to find unique genres across all columns
genres4 = pd.Series() #create an empty series
genres3 = pd.Series() #same as above
for i in genres2: 
    genres2a = pd.Series(len(movies[movies['Genre'].str.contains(i,case=False) & movies['Genre'].str.contains('|',regex=False)]),index=[i])
    genres2b = pd.Series(len(movies[movies['Genre'].str.contains(i,case=False)]),index=[i])
    #loop through each genre to see if the movies contain that genre and has other genres. Containing | shows that the genre is also classified in other genres --- group4
    genres4 = genres4.append(genres2a) #append genres 2a to genres4
    genres3 = genres3.append(genres2b) #same as above
q10 = (genres4 / genres3 * 100).sort_values(ascending = False) # Series of genres, percentages

   


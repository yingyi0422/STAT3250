##
## File: assignment11.py (STAT 3250)
## Topic: Assignment 11 
##

##  The file Stocks.zip is a zip file containing nearly 100 data sets of price 
##  records for various stocks.  A sample of the type of files contained
##  in Stocks.zip is AA.csv, which we have seen previously and is posted
##  in recent course materials. Each file includes daily data for a specific
##  stock, with stock ticker symbol given in the file name. Each line of
##  a file includes the following:
##
##   Date = date for recorded information
##   Open = opening stock price 
##   High = high stock price 
##   Low = low stock price 
##   Close = closing stock price 
##   Volume = number of shares traded
##   Adj Close = closing price adjusted for stock splits (ignored for this assignment)

##   The time interval covered varies from stock to stock. For many files
##   there are dates when the market was open but the data is not provided, so
##   those records are missing. Note that some dates are not present because the 
##   market is closed on weekends and holidays.  Those are not missing records.  

##  The Gradescope autograder will be evaluating your code on a subset 
##  of the set of files in the folder Stocks.  Your code needs to automatically 
##  handle all assignments to the variables q1, q2, ... to accommodate the 
##  reduced set, so do not copy/paste things from the console window, and
##  take care with hard-coding values. 

##  The autograder will contain a folder Stocks containing the stock data sets.
##  This folder will be in the working directory so your code should be written
##  assuming that is the case.  See the file week11a.py for specific code that 
##  can be used to read in files.

##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

import pandas as pd # load pandas
import numpy as np # load numpy
import glob # 'glob' searches for files
pd.set_option('display.max_columns', 10) # Display 10 columns in console


## 1.  Find the mean for the Open, High, Low, and Close entries for all 
##     records for all stocks.  Give your results as a Series with index
##     Open, High, Low, Close (in that order) and the corresponding means
##     as values.

stocks = glob.glob('Stocks/*.csv')
df = pd.DataFrame()  # empty dataframe
for file in stocks:
    newdf = pd.read_csv(file)  # read in the file
    index = [file[7:-4]] * len(newdf)
    newdf = newdf.set_index([index])
    df = pd.concat([df,newdf], sort = False)  # concatenate to existing dataframe
   
# apply mean function to each column
q1 = df.iloc[:,1:5].apply(np.mean)  # Series of means of Open, High, Low, and Close

## 2.  Find all stocks with an average Close price less than 30.  Give your
##     results as a Series with ticker symbol as index and average Close price. 
##     price as value.  Sort the Series from lowest to highest average Close
##     price.  (Note: 'MSFT' is the ticker symbol for Microsoft.  'MSFT.csv',
##     'Stocks/MSFT.csv' and 'MSFT ' are not ticker symbols.)

avg_close = df['Close'].groupby(df.index).mean() # group 'close' by index (ticker) and find mean 
q2 =  avg_close[avg_close < 30].sort_values()  # Series of stocks with average close less than 30

## 3.  Find the top-10 stocks in terms of the day-to-day volatility of the
##     price, which we define to be the mean of the daily differences 
##     High - Low for each stock. Give your results as a Series with the
##     ticker symbol as index and average day-to-day volatility as value. 
##     Sort the Series from highest to lowest average volatility.

volatilities = df['High'] - df['Low'] # compute diff between high and low by index
q3 = volatilities.groupby(volatilities.index).mean().nlargest(10)  # Series of top-10 mean volatility
# groupby index and find the mean, then take the largest 10

## 4.  Repeat the previous problem, this time using the relative volatility, 
##     which we define to be the mean of
## 
##                       (High - Low)/(0.5(Open + Close))
##
##     for each day. Provide your results as a Series with the same specifications
##     as in the previous problem.

volat2 = (df['High'] - df['Low']) / (0.5*(df['Open'] + df['Close'])) # use the above formula and repeat the steps
q4 = volat2.groupby(volat2.index).mean().nlargest(10)  # Series of top-10 mean relative volatility
# same as the previous question

## 5.  For each day the market was open in October 2008, find the average 
##     daily Open, High, Low, Close, and Volume for all stocks that have
##     records for October 2008.  (Note: The market is open on a given
##     date if there is a record for that date in any of the files.)
##     Give your results as a DataFrame with dates as index and columns of
##     means Open, High, Low, Close, Volume (in that order).  The dates should 
##     be sorted from oldest to most recent, with dates formatted (for example)
##     2008-10-01, the same form as in the files.   

avg_daily = df[df['Date'].str.contains('2008-10')].iloc[:,:-1] #find date with '2008-10' for october 2008
q5 = avg_daily.groupby(avg_daily['Date']).mean().sort_index()  # DataFrame of means for each open day of Oct '08.
# groupby date and find mean of all 5 columns, then sort by index in ascending order 

## 6. For 2011, find the date with the maximum average relative volatility 
##    for all stocks and the date with the minimum average relative 
##    volatility for all stocks. Give your results as a Series with 
##    the dates as index and corresponding average relative volatility
##    as values, with the maximum first and the minimum second.

max_volat = df[df['Date'].str.contains('2011-')] # find date with '2011-' which indicates records in 2011
max_volat['rel_vol'] = (max_volat['High'] - max_volat['Low'])/(0.5 * (max_volat['Open'] + max_volat['Close'])) # find the relative volatility 
mean_volat = max_volat['rel_vol'].groupby(max_volat['Date']).mean() # group the relative volatility by date and find mean 
q6 = mean_volat[mean_volat == max(mean_volat)] # Series of average relative volatilities
q6 = q6.append(mean_volat[mean_volat == min(mean_volat)])
# add both max and min of mean entries to q6

## 7. For 2010-2012, find the average relative volatility for all stocks on
##    Monday, Tuesday, ..., Friday.  Give your results as a Series with index
##    'Mon','Tue','Wed','Thu','Fri' (in that order) and corresponding
##    average relative volatility as values. 

year = df[pd.to_datetime(df['Date']).dt.year.isin([2010,2011,2012])] # take out year for slicing 
year['Weekday'] = pd.to_datetime(year['Date']).dt.day_name().str[0:3] # get weekday names and format them as mon tue etc, then add them into a new column
year['Custom_sort'] = pd.to_datetime(year['Date']).dt.weekday # custom_sort column enables us to sort weekday names properly 
year['rel_vol'] = (year['High'] - year['Low'])/(0.5 * (year['Open'] + year['Close'])) # same as the previous question
q7 = year['rel_vol'].groupby([year['Weekday'],year['Custom_sort']]).mean().sort_index(level = 1).droplevel(level = 1)  # Series of average relative volatility by day of week
# groupby relative volatility on weekday and custom_sort, find mean, then sort index, and drop level to only get weekday names as index

## 8.  For each month of 2009, determine which stock had the maximum average 
##     relative volatility. Give your results as a Series with MultiIndex
##     that includes the month (month number is fine) and corresponding stock 
##     ticker symbol (in that order), and the average relative volatility
##     as values.  Sort the Series by month number 1, 2, ..., 12.

temp8 = df[df['Date'].str.contains('2009-')] # find date with '2009-' which indicates observations in 2009
temp8['Month'] = pd.to_datetime(temp8['Date']).dt.month #extract month and store them into a new column
temp8['rel_vol'] = (temp8['High'] - temp8['Low'])/(0.5 * (temp8['Open'] + temp8['Close'])) # store relative volatility
group8 = temp8['rel_vol'].groupby([temp8['Month'],temp8.index]).mean().sort_index(level = 0) # groupby month and index and find mean relative volatility 
q8 = group8.groupby(group8.index.names[0], group_keys=False).nlargest(1).sort_index(level = 0)  # Series of maximum relative volatilities by month
# groupby by month and find maximum mean relative volatility, and sort by month

## 9.  The “Python Index” is designed to capture the collective movement of 
##     all of our stocks. For each date, this is defined as the average price 
##     for all stocks for which we have data on that day, weighted by the 
##     volume of shares traded for each stock.  That is, for stock values 
##     S_1, S_2, ... with corresponding volumes V_1, V_2, ..., the average
##     weighted volume is
##
##           (S_1*V_1 + S_2*V_2 + ...)/(V_1 + V_2 + ...)
##
##     Find the Open, High, Low, and Close for the Python Index for each date
##     the market was open in January 2013. 
##     Give your results as a DataFrame with dates as index and columns of
##     means Open, High, Low, Close (in that order).  The dates should 
##     be sorted from oldest to most recent, with dates formatted (for example)
##     2013-01-31, the same form as in the files.   

index = df[df['Date'].str.contains('2013-01')] # indentify 'date' with '2013-01' which indicates records in Jan 2013
group9 = pd.DataFrame()
# use lamda function, and repeat groupby for Open, High, Low, and Close, and add them as columns to our group9 variable 
for i in ['Open', 'High', 'Low', 'Close']:
    group9[i] = index.groupby(index['Date']).apply(lambda index,a,b: sum(index[a]*index[b]) / sum(index[a]),'Volume', i)
q9 = group9.sort_index()  # DataFrame of Python Index values for each open day of Jan 2013. 


## 10. For the years 2007-2012 determine the top-8 month-year pairs in terms 
##     of average relative volatility of the Python Index. Give your results
##     as a Series with MultiIndex that includes the month (month number is 
##     fine) and year (in that order), and the average relative volatility
##     as values.  Sort the Series by average relative volatility from
##     largest to smallest.

top8 = df[pd.to_datetime(df['Date']).dt.year.isin([2007,2008,2009,2010,2011,2012])] # take out year portion of 'date' to match our slicing
group10 = pd.DataFrame()
# find Python Index the same way as Q9, use the lambda function again
# set column 'date' as the index values for group by, group relative volatility by month and then year and find the average 
for i in ['Open', 'High', 'Low', 'Close']:
    group10[i] = top8.groupby(top8['Date']).apply(lambda top8,a,b: sum(top8[a]*top8[b])/sum(top8[a]),'Volume', i)

group10['rel_vol'] = (group10['High'] - group10['Low'])/(0.5*(group10['Open'] + group10['Close']))
group10['Date'] = group10.index # name the index
q10 = group10['rel_vol'].groupby([pd.to_datetime(group10['Date']).dt.month,pd.to_datetime(group10['Date']).dt.year]).mean().nlargest(8)  # Series of month-year pairs and average rel. volatilities


## 11. Each stock in the data set contains records starting at some date and 
##     ending at another date.  In between the start and end dates there may be 
##     dates when the market was open but there is no record -- these are the
##     missing records for the stock.  For each stock, determine the percentage
##     of records that are missing out of the total records that would be
##     present if no records were missing. Give a Series of those stocks
##     with less than 1.3% of records missing, with the stock ticker as index 
##     and the corresponding percentage as values, sorted from lowest to 
##     highest percentage.
##     Note: If a date appears in at least one file in the date set, then the
##     market is open that day.  If not then the market is closed that day.
##     Do not make any other assumptions about when the market is open or
##     closed, and do not use Python libraries (or other libraries) to try to
##     determine when the market was open.

dates = pd.Series(df['Date'].unique()) # store unique dates(potential missing records)
group11 = df['Date'].groupby(df.index).agg(['min', 'max', 'count']) # group df['date'] by index and find min, max, and total number of records 
group11['full'] = None # then create a 'full' column, which specifies how many total records are supposed to be present for each stock 
group11 = group11.reset_index() # reset index for a for loop in parsing rows
# for each row (stock), check total records that are supposed to be included
# find the percentage of missing records for each stock 
for i in range(len(group11)):
    group11.iloc[i,4] = sum(dates.between(group11.iloc[i,1], group11.iloc[i,2]))

percentage_miss = pd.Series((group11['full'] - group11['count']) / group11['full'] * 100)
percentage_miss.index = group11['index'] # rename the index
q11 = percentage_miss[percentage_miss < 1.3].sort_values() # Series of stocks and percent missing





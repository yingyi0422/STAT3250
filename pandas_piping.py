#!/usr/bin/env python
# coding: utf-8

# # Easy to read pandas: pandas piping (also known as method chaining)
# 
# ## R pipe
# 
# Tidyverse in R has the "pipe" operator %>% which is extremely useful in writing
# readable code.
# 
# Ex:
# 
# ``` R
# df >%>
#     do_first_thing %>%
#     do_second_thing %>%
#     final_thing
# ```
# 
# The alternative is usually nesting of functions.
# 
# Ex:
# 
# ``` R
# final_thing(
#     do_second_thing(
#         do_first_thing(df)
#     )
# )
# ```
# 
# Or saving each intermediate step as its own variable.
# 
# Ex:
# 
# ```R
# df1 = do_first_thing(df)
# df2 = do_second_thing(df1)
# df3 = do_final_thing(df2)
# ```
# 
# ## Python pipe?
# 
# Pandas does not really have something as smooth as tidyverse, unfortunately.
# 
# In pandas, there are 2 ways to pipe functions on DataFrames.
# 1. Method chaining (or dot chaining) (general python)
# 2. The pipe function (pandas specific)
# 
# We have been using 1 for some time now, but it a limited way.
# For example:
# 
# ``` python
# mean_runtime_per_class_section = /
#     runtimes.groupby(class_section).mean().sort_values(ascending=False)
# ```
# 
# This is an example of method chaining as we are using methods back to back.
# We can simply format it in a more readable way by wrapping the method chain 
# in parentheses and adding a new line where we want.
# 
# ``` python
# mean_runtime_per_class_section = (
#     runtimes
#     .groupby(class_section)
#     .mean()
#     .sort_values(ascending=False)
# )
# ```
# 
# If you find your method chain getting too long, consider breaking up into multiple lines as shown above.
# 
# Functionally, the results from using "piped" vs not "piped" code are exactly the same. 
# However, piping can sometimes make the code easier to read and understand.
# Writing code that is easy to understand is an important skill for anyone who shares code with other people.
# 
# Furthermore, method chaining is concept that is used across the Python ecosystem.
# 
# ## Data Science Salary Dataset
# 
# Take the following code as an example.
# We are exploring a data science salary dataset.



import numpy as np
import pandas as pd




ds_salaries = pd.read_csv("ds_salaries.csv", index_col=0)
ds_salaries.head()


# ## Question
# 
# Which U.S., full time, entry level role pays the most for fully remote jobs?



print(ds_salaries.experience_level.value_counts())
print(ds_salaries.remote_ratio.value_counts())
print(ds_salaries.employment_type.value_counts())


# ### Pipe version



entry_full_time_remote = (
    ds_salaries
    .query(                                        # filter on conditions
        "employment_type == 'FT'"
        "and experience_level == 'EN'"
        "and remote_ratio == 100"
        "and employee_residence == 'US'")
    .filter(items=["job_title", "salary_in_usd"])  # filter columns
    .groupby("job_title")                          # for each job_title
    .agg(["mean", "count"])                        # calculate mean and count
    .sort_values(("salary_in_usd", "mean"), ascending=False)
)


# ### Intermediate steps



s1 = ds_salaries[
    (ds_salaries.employment_type == "FT") 
    & (ds_salaries.experience_level =="EN")
    & (ds_salaries.remote_ratio == 100)
    & (ds_salaries.employee_residence == "US")
]
s2 = s1[["job_title", "salary_in_usd"]]
s3 = s2.groupby("job_title")
s4 = s3.agg(["mean", "count"])
s5 = s4.sort_values(("salary_in_usd", "mean"), ascending=False)


# ### Nested



pd.DataFrame.sort_values(
    pd.DataFrame.groupby(
        ds_salaries[
            (ds_salaries.employment_type == "FT") 
            & (ds_salaries.experience_level =="EN")
            & (ds_salaries.remote_ratio == 100)
            & (ds_salaries.employee_residence == "US")]
        [["job_title", "salary_in_usd"]],
        "job_title"
    ).agg(["mean", "count"]),
    by=("salary_in_usd", "mean"),
    ascending=False
)


# The first and second are more readable than the third.
# The difference between the first and second are smaller, but I think the first is slightly easier to read.
# Could be personal preference.

# ## Outline
# 
# The rest of the lecture is as follows:
# 1. Overview of methods vs functions
# 2. Method/dot chaining
# 3. Useful DataFrame/Series methods
# 4. Pandas pipe function
# 
# Before we dive specific examples of useful methods for chaining, let's first briefly talk about methods in general.
# 
# ## Methods vs Functions
# 
# Methods are just functions that are "attached" to a specific class.
# For example, the *numpy library* has the sum **function**:
# 
# ``` python
#     np.sum
# ```
# 
# which can be used on things like numpy arrays.



X = np.array([1, 2, 3, 4])
np.sum(X)


# But all *numpy arrays*, like **X** in the above cell, also have their own sum **method**.
# To use it you simply type ".sum()" at the end of a numpy array.
# This will call the "sum()" function specific to the array class.



print(X.sum())


# In the previous example, *np.sum* is a **function**, while the *.sum()* after
# a numpy array is a **method** that is "attached" to all numpy ndarrays
# (the numpy arrays we've been working with).
# Specifically, that ".sum()" method is attached to the array class like
# 
# ``` python
# np.ndarray.sum()
# ```
# 
# So anything that is a numpy array type will be able to use the ".sum()" method.
# 
# In the pandas library, we've frequently used the ".unique()" method of pandas Series.
# 
# ``` python
# user_names_series.unique()
# ```
# 
# Pandas Series and DataFrames have many useful methods that we've been using throughout the semester.
# 
# ### Dot Notation
# 
# All methods follow the same "dot notation" even for objects and classes that
# are not numpy arrays.
# For example, lists have an *append* **method** which adds a new value to the end of
# a list.
# Using it looks like:



xlist = [] # initialize and empty list
xlist.append(1) # append a 1 to the list
print(xlist)

xlist.append("asdfasdf")
print(xlist)


# ## Method Chaining
# 
# Now, a really cool thing happens when a method returns an object that is the
# same type or class as the original object.
# 
# It allows you to use the "dot notation" repeatedly and create a pipeline of sorts.
# This is super useful in pandas, because lots of DataFrame/Series methods return Series/DataFrame themselves.
# Because these methods return a Series/DataFrame you can immediately chain another Series/DataFrame method.
# This looks like
# 
# ``` python
#     df1.method1() -> returns a dataframe, say df2
#     df2.method2() -> returns a dataframe, say df3
#     df3.method3() -> etc
# ```
# 
# In code, it will look like this:
# 
# ``` python
#     df1.method1().method2().method3().etc
# ```
# 
# This is the core idea of "Method Chaining" (also called "dot chaining").
# But as the method chain gets longer, it become harder to read, so you can 
# organize them by wrapping them in parentheses.
# 
# ``` python
#     result = (
#         df
#         .method1()
#         .method2()
#         .method3()
#         .etc()
#     )
# ```
# 
# So, what methods are available for DataFrames?
# Here are some simple useful ones.
# 
# ### Some useful DataFrame methods
# 
# * query
# * filter
# * assign
# * rename
# * drop
# 
# but there are many more.
# Check out https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html for a
# more exhaustive list.
# Pandas series methods (including str methods) can also be found https://pandas.pydata.org/pandas-docs/stable/reference/series.html
# But we'll stick with these few for now.
# 
# #### [query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html#pandas.DataFrame.query)
# 
# Select rows of a DataFrame based on certain conditional statements. Using boolean masks or the *.loc* method can achieve similar results.
# 
# #### [filter](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.filter.html#pandas.DataFrame.filter)
# 
# Select certain columns of a DataFrame, or certain indices.
# 
# #### [assign](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.assign.html#pandas.DataFrame.assign)
# 
# Add a new column to a DataFrame, or replace an existing one.
# 
# #### [rename](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html#pandas.DataFrame.rename)
# 
# Rename columns of a DataFrame or indices.
# 
# #### [drop](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html#pandas.DataFrame.drop)
# 
# Drop certain columns of a DataFrame or indices.

# ### query



df = pd.read_csv("football.csv")


# Two ways to do the same thing.



df.query("Quarter == 5").head()
df[df["Quarter"] == 5].head()


# The two lines achieve the same thing, but one could argue that the first is more readable than the second.
# According to the docs, using query can be slower for small datasets but faster for large ones.
# This difference is probably negligible in most cases.
# 
# If a column name has a space, then wrap it in backticks.
# Strings in the query can use single or double quotes, just use the opposite of the one it is wrapped in.



df["Play Type"] = df["PlayType"] # add a new column with a space in the name
df.query("`Play Type` == 'KICK OFF'").head()


# The query method can also contain multiple conditional statements.
# The following two lines are equivalent.



df.query("IsPass == True and IsIncomplete == False and IsInterception == False").head()




df[
    (df.IsPass == True) &
    (df.IsIncomplete == False) &
    (df.IsInterception == False)
].head()


# Variables can be reference in the query string using @



kicks = ["FIELD GOAL", "PUNT", "EXTRA POINT", "KICK OFF"]
df.query("PlayType in @kicks").head()




df[df.PlayType.isin(kicks)].head()


# ## Example
# 
# Do some quarters have better passing than other quarters?



passes_per_quarter = (
    df[["IsPass", "Quarter"]]
    .query("IsPass == True")
    .groupby("Quarter")
    .count()
)
successful_passes_per_quarter = (
    df[["IsPass", "Quarter", "IsIncomplete", "IsInterception"]]
    .query("IsPass == True and IsIncomplete == False and IsInterception == False")
    .groupby("Quarter")
    [["IsPass"]]
    .count()
)
(
    (successful_passes_per_quarter / passes_per_quarter)
    .reset_index()
    .rename(columns={"IsPass": "SuccessfulPass"})
)


# ### filter
# 
# Select specific columns or labels.
# Similar to loc.



df.head()




df.filter(items=["OffenseTeam", "DefenseTeam", "YardLine", "PlayType"])




df.filter(like="Team")


# ### assign
# 
# Create new columns, overwrite existing ones.



ds_salaries.head()




(
    ds_salaries
    .assign(in_office_ratio = 100 - ds_salaries.remote_ratio)
    .filter(like="ratio") # select columns that contain 'ratio'
)


# ### rename
# 
# Renames columns or labels.
# 
# We can rename specific columns.



df.rename(columns={"OffenseTeam": "offense_team"})


# Rename all columns with a function.



df.rename(mapper=str.lower, axis=1)


# Rename all labels with a function.



df.rename(mapper=lambda x: x + 4) # default is axis=0, the index so we don't need to specify


# ### drop
# 
# Drop labels or columns



df.drop(columns=["GameId", "GameDate", "Quarter"])


# All the functions an be done in different ways, for example using loc or masks.
# 
# ## Pipe function
# 
# Piping is another way to chain operations on DataFrames.
# It's a little more clunky than dot chaining, but is more flexible since you could use arbitrary functions (that expect Series or DataFrames).
# 
# Again, you can do it all on one line, or wrap over multiple lines with parentheses.



(
    ds_salaries
    .pipe(pd.DataFrame.query, "experience_level == 'EN'")
    .pipe(pd.DataFrame.filter, like="sal")
)


# ## Conclusion
# 
# Method chaining is an easy way to make your code more readable.
# It may also help approaching the problem in a systematic linear way.
# However, it is not required and ultimately 'readability' up to each user.
# 
# One big downside of long method chains is that you are not able to easily debug intermediate steps partway through the chain.
# So if you do require testing/checking intermediate steps, consider breaking up the pipeline.
# 






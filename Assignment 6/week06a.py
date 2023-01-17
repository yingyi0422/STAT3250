##
## File: week06a.py (STAT 3250)
## Topic: The MultiIndex

import pandas as pd # load pandas as pd

#### Working with a MultiIndex

# Load the 'samplegrades.csv' data set
grades = pd.read_csv("samplegrades.csv")

# Group Final exam scores on both Sect and Prev
gr = grades['Final'].groupby([grades['Sect'],grades['Prev']])
gr

# Compute the mean for each group; result is a Series with a MultiIndex that
# has columns Sect and Prev
demo1 = group1.mean()
demo1

#### Extracting values
demo1.loc[('MW200','Y')]  # Mean for MWF200 section, Prev = Y (one value)

# Slices (subsets) using xs
demo1.xs("N", level='Prev')  # entries where 'Prev' column = 'N'
demo1.xs("TR1230", level='Sect')  # entries where 'Sect' column = 'TR1230'


#### Extracting index columns

# index of demo1
demo1
demo1.index  # index of demo 1

# 'zip' will reorganize them
list(zip(*demo1.index))
list(zip(*demo1.index))[1]
list(zip(*demo1.index))[0]

# We can create a new Series with just 'Sect' as the index
pd.Series(data=demo1.values, index=list(zip(*demo1.index))[0])

# The same with 'Prev' as index
pd.Series(data=demo1.values, index=list(zip(*demo1.index))[1])

# We can also move the index columns to the columns of a dataframe
# using 'reset_index'
df = pd.DataFrame(demo1).reset_index()
df

# We could use this dataframe to create the Series too
pd.Series(data=df['Final'].values, index=df['Prev'])


#### Finding maximum values

demo1

# The largest value for each 'Sect'
demo1.groupby('Sect', group_keys=False).nlargest(1)  # Note a Series with multiIndex

# Or 'max' works for this case too
demo1.groupby('Sect', group_keys=False).max()

# And for each 'Prev'
demo1.groupby('Prev', group_keys=False).nlargest(1)


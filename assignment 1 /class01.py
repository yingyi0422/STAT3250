#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:57:17 2022

@author: zach0422
"""

import pandas as pd # load pandas library as pd

df = pd.read_csv('virginia21.csv')

display(df)
runs = df['Runs']
runs
runs.mean()

df['Hits'].median()

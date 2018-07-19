#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 14:37:05 2017

@author: DaltonS1
"""

import pandas as pd
import csv
import os
import numpy

import lib.database.dbatools as db

# Reads CSV file to count number of lines including header line
def csv_row_count(file_name):
    with open(file_name, 'r') as f:
        reader = csv.reader(f, delimiter = ",")
        data = list(reader)
        row_count = len(data)
        return row_count

# Converts the most recent available CSV data to a DataFrame of up to size 'volume' by intervals of the requested frequency
def recent_interval_data(indicator, frequency, symbol, folder='CSV', volume=1440):
    # volume*frequency = number of lines needed from csv to cover volume request at specified frequency
    # overlap = is used to determine number of rows still needed to fulfill request
    overlap = volume*frequency

    row_offset = 1
    while (overlap > 0):
        # creates temporary DataFrame to append to return DataFrame df, skips repeat headers
        temp_df = db.Dbatools().findAllTickersByExchangeAndSymbol(1440, 'bitmex', symbol, indicator, 0)
        #pd.read_csv(path + '/' + csv_list[current_csv], header = 0, index_col = 'timestamp', usecols = ['timestamp', indicator], skiprows = range(1, row_count - overlap))

        overlap = overlap - len(temp_df) + row_offset

    return temp_df[frequency - 1::frequency]

  
# Simple moving average, takes a DataFrame and an integer 'span' that denotes the number
# of rows of the DataFrame that is used to calculate the new mean for those DataFrame rows
# returns a DataFrame with those new means
def simple_moving_average(df, span=1):
    z = df.rolling(window=span).mean()
    z.dropna(axis = 0, how = 'any')
    return z

# expomential moving average, takes a DataFrame and an integer 'window' that, like SMA,
# denotes the number of rows weighting the mean, returns a DataFrame with those new means
def exponential_moving_average(df, window=1):
    window = len(df)
    z = df.ewm(span=window).mean()
    z.dropna(axis = 0, how = 'any')
    return z

# mean, takes a DataFrame and returns the calculated mean of all elements of
# the DataFrame, returns the mean as a float
def mean_val(df):
    z = df.mean()
    return float(z)

# sqrt_mean, takes a DataFrame and square roots all the elements of the DataFrame
# then returns the mean of those values as a float
def sqrt_mean_val(df):
    z = df.apply(numpy.sqrt).mean()
    return float(z)

# std_dev, takes a DataFrame and returns the calculated standard deviation as a float
def std_dev_val(df):
    z = df.std()
    return float(z)

# percent_change, takes a DataFrame and returns a DataFrame containing the percent of change between each row
def percent_change(df):
    z = df.pct_change()
    return z

# rate_of_change, takes a DataFrame and returns a DataFrame containing the rate of change between each row
def rate_of_change(df):
    z = df*df.pct_change()
    return z

# acceleration, takes a DataFrame and returns a DataFrame containing the rate of change of the rate of change between rows
def acceleration(df):
    z = rate_of_change(df*df.pct_change())
    return z



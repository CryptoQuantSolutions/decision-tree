#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 13:07:51 2017

@author: alex_vo
"""

import logging

import lib.csv.csv_utils as csv_utils
import lib.database.dbatools as db
import lib.utils.analytic_utils as au

logger = logging.getLogger(__name__)

# ===========================================================================================
# Text Parser Object that takes in a txt file name from the current working directory
# Parses file into a dictionary with variable names as keys and entire exec string as values
# Everything before 'first space' is var name, everything after is exec string
# ===========================================================================================
class VariableMgr():
    def __init__(self):
        self.str_literal_vars = {}
        #self.__read_str_literals()
        
    # ====================================================================
    # Handles Variable-ExecString Parsing to be read into str_literal_vars
    # ====================================================================
    def __read_str_literals(self, txt_file):
        try:
            with open(txt_file, 'r') as file:
                txt_lines = file.read().splitlines()
                for line in txt_lines:
                    temp_list = line.split(' ', 1)

                    # 'Replace any 'var(ex_name)' to be the the corresponding ex_name's eval string
                    for key in self.str_literal_vars.keys():
                        temp_list[1] = temp_list[1].replace('var(' + str(key) + ')', self.str_literal_vars[key])

                    self.str_literal_vars[temp_list[0]] = temp_list[1]
        except FileNotFoundError as e:
            logger.error(e)

    # =====================================================================
    # Evaluate str_literal_vars dictionary and returns dictionary containing
    # evaluated values for each variable
    # =====================================================================
    def eval_str_literals(self):
        eval_dict = {}
        for key in self.str_literal_vars.keys():
            # Datafeed objects and Analytics objects both have a corresponding 'evaluate' method
            # normal eval is used if string is written not using any custom functions
            try:
                eval_dict[key] = eval(self.str_literal_vars[key]).evaluate()
            except:
                eval_dict[key] = eval(self.str_literal_vars[key])
            
        return eval_dict
            
            

# =========================================================================================
# Simplest Level of Data that all analytics are built on
# Fetches Data According to Specified Exchange, Indicator, Symbol
# =========================================================================================
class Datafeed():
    # exchange: BitMEX, GDAX, BitStamp, Bitfnex ...
    # indicator: index, mark, last
    # symbol: XBTUSD, XBTU17, XRPU17, ...
    # time offset is the number of minutes to start data frame back from current time
    # i.e. 0 = current time, 15 = 15 minutes ago
    def __init__(self, exchange, indicator, symbol, time_offset = 0):
        self.exchange = exchange
        
        if (indicator.lower() == 'index'):
            self.indicator = 'indicative_settle_price'
        elif (indicator.lower() == 'mark'): 
            self.indicator = 'marketprice'
        elif (indicator.lower() == 'last'): 
            self.indicator = 'lastprice'
        else:
            print("Please Specify a Valid Indicator")
            self.indicator = indicator
        
        self.symbol = symbol
        self.time_offset = time_offset
        
        #self.path = 'CSV/' + str(self.exchange) + '/' + str(self.symbol)
        self.supported_types = [EMA, SMA, Volatility, Acceleration, Datafeed]

        self.logger = logging.getLogger(__name__)

        
        
    # ============================================================
    # Overload Operators
    # Supports Arithmetic Operations between numbers and other Analytic/Datafeed Objects
    # ============================================================
    def __add__(self, value):
        if type(value) in self.supported_types:
            return self.evaluate() + value.evaluate()
        else:
            return self.evaluate() + value
        
    def __sub__(self, value):
        if type(value) in self.supported_types:
            return self.evaluate() - value.evaluate()
        else:
            return self.evaluate() - value
        
    def __mul__(self, value):
        if type(value) in self.supported_types:
            return self.evaluate() * value.evaluate()
        else:
            return self.evaluate() * value
        
    def __truediv__(self, value):
        if type(value) in self.supported_types:
            return self.evaluate() / value.evaluate()
        else:
            return self.evaluate() / value
        
    def __radd__(self, value):
        if type(value) in self.supported_types:
            return value.evaluate() + self.evaluate()
        else:
            return value + self.evaluate()
        
    def __rsub__(self, value):
        if type(value) in self.supported_types:
            return value.evaluate - self.evaluate()
        else:
            return value - self.evaluate()
        
    def __rmul__(self, value):
        if type(value) in self.supported_types:
            return value.evaluate() * self.evaluate()
        else:
            return value * self.evaluate()
        
    def __rtruediv__(self, value):
        if type(value) in self.supported_types:
            return  value.evaluate() / self.evaluate()
        else:
            return value / self.evaluate()
        
    # =================================================================
    # Returns Most Recent Data Point taking into account time_offset
    # Note: 'iloc[0][-1] is used to ensure 'left most' and 'most recent at bottom is used
    # evaluate is used if variable is only a Datafeed object
    # =================================================================
    def evaluate(self):
        #return csv_utils.recent_interval_data(self.path, 1, self.indicator, self.time_offset).iloc[-1][0]
        df = db.Dbatools().findAllTickersByExchangeAndSymbol(1, self.exchange, self.symbol, self.indicator, self.time_offset).iloc[-1][0]

        #self.logger.info('dataframe size: ' + df.size)

        return df
    
    # ==================================================================
    # Used when an analytical indicator is applied on top of a datafeed
    # This includes support for multiple indicators applied at a time
    # ==================================================================
    def create_dataframe(self, size):
        #recent_data = csv_utils.recent_interval_data(self.path, size, self.indicator, self.time_offset)
        # Rename_df_indices removes seconds and microseconds from timestamp indices

        recent_data = db.Dbatools().findAllTickersByExchangeAndSymbol(size, self.exchange, self.symbol, self.indicator, self.time_offset)

        #self.logger.info(recent_data.size)
        return csv_utils.rename_df_indices(recent_data)
        
    
# =======================================================================================
# Takes in a 'datafeed' which can be another Analytics object or DataFeed object
# ========================================================================================
class Analytics():
    def __init__(self, datafeed, window, interval):
        self.datafeed = datafeed
        self.window = window
        self.interval = interval
        self.supported_types = [EMA, SMA, Volatility, Acceleration, Datafeed]

        self.logger = logging.getLogger(__name__)

    # ============================================================
    # Overload Operators
    # Supports Arithmetic Operations between numbers and other Analytic/Datafeed Objects
    # ============================================================
    def __add__(self, value):
        if type(value) in self.supported_types:
            return self.evaluate() + value.evaluate()
        else:
            return self.evaluate() + value
        
    def __sub__(self, value):
        if type(value) in self.supported_types:
            return self.evaluate() - value.evaluate()
        else:
            return self.evaluate() - value
        
    def __mul__(self, value):
        if type(value) in self.supported_types:
            return self.evaluate() * value.evaluate()
        else:
            return self.evaluate() * value
        
    def __truediv__(self, value):
        if type(value) in self.supported_types:
            return self.evaluate() / value.evaluate()
        else:
            return self.evaluate() / value
        
    def __radd__(self, value):
        if type(value) in self.supported_types:
            return value.evaluate() + self.evaluate()
        else:
            return value + self.evaluate()
        
    def __rsub__(self, value):
        if type(value) in self.supported_types:
            return value.evaluate - self.evaluate()
        else:
            return value - self.evaluate()
        
    def __rmul__(self, value):
        if type(value) in self.supported_types:
            return value.evaluate() * self.evaluate()
        else:
            return value * self.evaluate()
        
    def __rtruediv__(self, value):
        if type(value) in self.supported_types:
            return  value.evaluate() / self.evaluate()
        else:
            return value / self.evaluate()

    # ================================================================================
    # Calculate Total Window Size for Analytics objects that will eventually allow its
    # dataframe to be collapsed to 1
    # General Recursive Formula: sum of window*intervals for each analytics
    # ================================================================================      
    def calculate_total_dataframe_size(self):
        datafeed = self
        
        total_df_size = 0
        while (type(datafeed) is not Datafeed):
            # =======================================================
            # Adjust window passed in according to type of operation
            # =======================================================
            if type(datafeed) is Acceleration:
                total_df_size += (datafeed.window + 2) * datafeed.interval
            elif type(datafeed) is Volatility:
                total_df_size += (datafeed.window +1) * datafeed.interval
            else:
                total_df_size += datafeed.window * datafeed.interval
            
            # Move Towards Inner analytic objects
            datafeed = datafeed.datafeed
            
        return total_df_size
        
    
    def evaluate(self):
        
        # =====================================================================
        # Create Multiple Lists of Indicators, Windows, and Intervals in order 
        # from outermost to innermost applied indicator
        # =====================================================================
        datafeed_cp = self

        indicator_list = [] #list of all indicator types in order from outermost to innnermost to be applied
        window_list = [] #list of all windows in order from most outermost to innermost
        interval_list = [] # list of all interval types in order from outermost to innermost to be applied
        while (type(datafeed_cp) != Datafeed):
            indicator_list.append(type(datafeed_cp))
            window_list.append(datafeed_cp.window)
            interval_list.append(datafeed_cp.interval)
            datafeed_cp = datafeed_cp.datafeed

        # ====================================================================
        # Create Dataframe with Correct Size 
        # ====================================================================
        df_size = self.calculate_total_dataframe_size() #total dataframe size required for when multiple operations are used
        self.logger.info('WINDOW SIZE:' + str(df_size))
        dataframe = datafeed_cp.create_dataframe(df_size)
        self.logger.info('SIZE:' + str(len(dataframe)))
        
        # ====================================================================
        # Apply Indicator Given Window and Interval
        # 'range' call re-orders list idx to 'innermost to outermost'
        # Index is called in reverse order
        # ====================================================================
        for idx in range(len(window_list) - 1, -1, -1):
            #dataframe = dataframe[::-interval_list[idx]][::-1]
            #print('SIZE:', len(dataframe), dataframe.head(), '\n')
            dataframe = self.apply_indic_df(dataframe, indicator_list[idx], window_list[idx], interval_list[idx])
            #print(dataframe)
            #print('SIZE:', len(dataframe), dataframe.head(), '\n')
       
        return dataframe.iloc[0][-1]
        

    def apply_indic_df(self, df, indicator_type, window, interval):
        if indicator_type is SMA:
            return au.simple_moving_average(df, window, interval)
        elif indicator_type is EMA:
            return au.exponential_moving_average(df, window, interval)
        elif indicator_type is Acceleration:
            return au.acceleration(df, window, interval)
        elif indicator_type is Volatility:
            return au.volatility(df, window)
        else:
            ValueError('Invalid Indicator Type Specified in apply_indic_df')    
        
        
        
# Analytic Subclasses that are initialized in text files
# Simply call their 'evaluate' method to eval the object
class EMA(Analytics):
    def __init__(self, datafeed, window, interval):
        Analytics.__init__(self, datafeed, window, interval)
        
class SMA(Analytics):
    def __init__(self, datafeed, window, interval):
        Analytics.__init__(self, datafeed, window, interval)
        
class Volatility(Analytics):
    def __init__(self, datafeed, window, interval):
        Analytics.__init__(self, datafeed, window, interval)
        
class Acceleration(Analytics):
    def __init__(self, datafeed, window, interval):
        Analytics.__init__(self, datafeed, window, interval)
 


# =====================================================================
# Debugging Code
# =====================================================================

test = VariableMgr() # Create Variable Manager Object
dt = test.eval_str_literals()       # Evaluated Values
raw_str = test.str_literal_vars     # Raw Eval String before it is "eval'd"

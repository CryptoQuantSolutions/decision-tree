#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 17:02:10 2017

@author: alex_vo
"""

import logging

#import lib.exchange.bitmex.bitmex as bitmex
from lib.utils.automation_equations import all_currency_y_search
import lib.utils.place_orders as po

from engine.arrays import Arrays
from engine.comparisons import Comparisons

logger = logging.getLogger(__name__)

# ================================================================
# Comparison Manager Must be Used Hand in Hand with VariableManger in variable_reader.py to Evaluate Comparisons for Variables.
# ComparisonMgr should never be used alone, only in a TradeEngine Object
# 'eval_comps' is to be called every 'x-number of seconds'
# Note: The 'adding' of LowComp objects to MasterComp objects is performed in trade_engine
# ================================================================
class ComparisonsMgr():
    def __init__(self, __exchange_mgr):
        self.symbol = 'XBTUSD'

        # Delta sum values
        self.sum_da = {'MasterComp':0,'LowerComp': 0}
        self.sum_db = {'MasterComp':0,'LowerComp': 0}
        self.sum_mca = {'MasterComp':0,'LowerComp': 0}
        self.sum_mcb = {'MasterComp':0,'LowerComp': 0}

        self.order_arrays = Arrays().arrays

        self.master_deltas = [0,0,0,0]
        self.recent_master_comp_idx = None
        self.recent_comp_idx = None
        self.__exchange_mgr = __exchange_mgr
        
        self.str_literal_vars = []
        self.comparisons_obj = Comparisons()

        self.__load_comparisons()

    def __repr__(self):
        return #'Recent Master:' + str(self.recent_master_comp_idx) + ' Recent Low:' + str(self.recent_comp_idx) + ' ' + str(self.master_deltas)
    
    def __load_comparisons(self):
        self.master_comps = self.comparisons_obj.comparison_list

    # Recursive decision tree search algorithm
    def find_leaf_node_comparison(self, comparison_obj=None):
        # Loop through all child comparisons
        for comparison in comparison_obj.child_comparisons:
            # Check to see if Parent comparison is True or False
            logger.info('Checking \'{0}\' comparison...'.format(comparison.id))

            # Check if comparison is a leaf node
            if len(comparison.child_comparisons) is not 0:
                if comparison.main_comparison:
                    logger.info('\'{0}\' comparison is True.'.format(comparison.id))
                    self.find_leaf_node_comparison(comparison)
                else:
                    logger.info('\'{0}\' comparison is False.'.format(comparison.id))
            else:
                # Leaf node
                logger.info('Leaf node found!')

                # Check to see if leaf node comparison is True
                if comparison.main_comparison:
                    # Do something
                    logger.info('\'{0}\' comparison(leaf node) is True.'.format(comparison.id))

                    comparison.set_symbol(self.symbol)

                    # Generate order arrays
                    comparison.generate_arrays(self.__exchange_mgr)

                    break

                else:
                    # if leaf node is False, adjust deltas (this may need to be changed)
                    logger.info('\'{0}\' comparison(leaf node) is False.'.format(comparison.id))
                    comparison.adjust_deltas()

                    logger.info('Adjusting deltas...')
                    for array in comparison.order_arrays:
                         array.adjust_deltas()





    # ============================================================================================
    # Modify Target Delta According to Above, Below, Max Change Above and Max Change Below, Deltas
    # ============================================================================================
    def find_comparison_delta_range(self, comparison):
        instant_delta = self.__exchange_mgr.instant_delta(self.symbol)
        delta_above_ = comparison.deltas[0]
        delta_below_ = comparison.deltas[1]
        max_change_above_ = comparison.deltas[2]
        max_change_below_ = comparison.deltas[3]
        midpoint_delta = round(((delta_above_ + delta_below_) / 2), 8)

        # Target buy and sell delta as determined by comparing instant delta to delta ranges
        # Returns None if doesn't apply
        buy_delta = None
        sell_delta = None

        logger.info("Instantaneous Delta: " + str(instant_delta))

        # ================================================================================
        # Set Target Delta to be Midpoint of Above/Below Delta if Greater than Delta Range
        # ================================================================================
        if instant_delta >= delta_below_:
            sell_delta = midpoint_delta
            logger.info('Instant Delta is greater than below delta')
            logger.info('Aiming for Sell Delta: ' + str(midpoint_delta))
            logger.info('Not Placing Any Buy Orders This Loop.')
        # ================================================================================
        # Modify Target Delta using User Specified Change Values
        # ================================================================================
        elif delta_below_ > instant_delta > delta_above_:

            # Check if Delta is Too Close to Below Side of Delta Range
            if abs(instant_delta - delta_below_) < abs(max_change_below_):
                buy_delta = delta_below_
                logger.info("Aiming for Buy Delta:" + str(delta_below_))
            else:
                buy_delta = instant_delta + max_change_below_
                logger.info("Aiming for Buy Delta:"+ str(instant_delta + max_change_below_))

            # Check if Delta is Too Close to Above Side of Delta Range
            if abs(instant_delta - delta_above_) < abs(max_change_above_):
                sell_delta = delta_above_
                logger.info("Aiming for Sell Delta:" + str(delta_above_))
            else:
                sell_delta = instant_delta + max_change_above_
                logger.info("Aiming for Sell Delta:" + str(instant_delta + max_change_above_))
        # ================================================================================
        # Set Target Delta to be Midpoint of Above/Below Delta if Less than Delta Range
        # ================================================================================
        elif instant_delta <= delta_above_:
            buy_delta = midpoint_delta
            logger.info('Instant Delta is less than above delta')
            logger.info('Aiming for Buy Delta: ' + str(midpoint_delta))
            logger.info('Not Placing Any Sell Orders This Loop.')

        else:
            raise Exception("Error: Unable to Compare Instant Delta to Above and Below Deltas")

        return buy_delta, sell_delta

    # ========================================================================
    # eval_comps is the function call run every iteration/x-number of seconds
    # It evaluates comparisons in the correct order (left to right) and handles 
    # the recent comparisons idx to determine how to modify/set new delta values
    # NOTE: This should never be called directly on a ComparisonsMgr object, 
    # only used as a helper in TradeEngine's 'run_trade_engine' method
    # ========================================================================q
    def eval_comps(self):
        self.__exchange_mgr.cancel_all_orders(self.symbol)

        for comparison in self.master_comps:
            if comparison.main_comparison is True:
                logger.info('\'{0}\' comparison is True.'.format(comparison.id))

                self.find_leaf_node_comparison(comparison)
            else:
                logger.info('\'{0}\' comparison is False.'.format(comparison.id))
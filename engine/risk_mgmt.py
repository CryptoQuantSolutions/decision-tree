import tkinter as tk
from datetime import datetime
from time import sleep
from re import sub


import logs as log
# from server import notifications as Twil, client_side_obj as cso
import first_test.bitmex
from first_test.automation_equations import all_currency_y_search
import first_test.place_orders as po

import threading
import csv_manager as cm
import data_analytics as da
import pygame.mixer as pgm

class RiskMgmt():
    def __init__(self):
        # Delta Values Constantly Modified
        self.__delta_above = 0
        self.__delta_below = 0
        self.__max_change_above = 0
        self.__max_change_below = 0

        # Delta sum values
        self.sum_da = 0
        self.sum_db = 0
        self.sum_mca = 0
        self.sum_mcb = 0

        # Initial delta values
        self.__initial_delta_above = 0
        self.__initial_delta_below = 0
        self.__initial_max_change_above = 0
        self.__initial_max_change_below = 0

    #=====================================================================================================
    # Modify class delta values based on comparisons created during compare_UI execution
    #=====================================================================================================
    def __update_deltas(self):
        self.sum_da = self.__initial_delta_above
        self.sum_db = self.__initial_delta_below
        self.sum_mca = self.__initial_max_change_above
        self.sum_mcb = self.__initial_max_change_below

        if not (self.sum_da == self.__initial_delta_above):
            self.__delta_above = self.sum_da
        if not (self.sum_db == self.__initial_delta_below):
            self.__delta_below = self.sum_db
        if not (self.sum_mca == self.__initial_max_change_above):
            self.__max_change_above = self.sum_mca
        if not (self.sum_mcb == self.__initial_max_change_below):
            self.__max_change_below = self.sum_mcb

        print("")
        print('current delta above: ', self.__delta_above)
        print('current delta below: ', self.__delta_below)
        print('current max above: ', self.__max_change_above)
        print('current max below: ', self.__max_change_below)

    # ============================================================================================
    # Modify Target Delta According to Above, Below, Max Change Above and Max Change Below, Deltas
    # ============================================================================================
    def __find_delta_range(self):
        instant_delta = self.__exchange_mgr.instant_delta(self.__symbol)
        delta_above_ = self.__delta_above
        delta_below_ = self.__delta_below
        max_change_above_ = self.__max_change_above
        max_change_below_ = self.__max_change_below
        midpoint_delta = round(((delta_above_ + delta_below_) / 2), 8)

        # Target buy and sell delta as determined by comparing instant delta to delta ranges
        # Returns None if doesn't apply
        buy_delta = None
        sell_delta = None

        print("Instantaneous Delta: " + str(instant_delta))

        # ================================================================================
        # Set Target Delta to be Midpoint of Above/Below Delta if Greater than Delta Range
        # ================================================================================
        if instant_delta >= delta_below_:
            sell_delta = midpoint_delta
            print('\nInstant Delta is greater than below delta')
            print('Aiming for Sell Delta: ', midpoint_delta)
            print('Not Placing Any Buy Orders This Loop.')
        # ================================================================================
        # Modify Target Delta using User Specified Change Values
        # ================================================================================
        elif delta_below_ > instant_delta > delta_above_:

            # Check if Delta is Too Close to Below Side of Delta Range
            if abs(instant_delta - delta_below_) < abs(max_change_below_):
                buy_delta = delta_below_
                print("Aiming for Buy Delta:", delta_below_)
            else:
                buy_delta = instant_delta + max_change_below_
                print("Aiming for Buy Delta:", instant_delta + max_change_below_)

            # Check if Delta is Too Close to Above Side of Delta Range
            if abs(instant_delta - delta_above_) < abs(max_change_above_):
                sell_delta = delta_above_
                print("Aiming for Sell Delta:", delta_above_)
            else:
                sell_delta = instant_delta + max_change_above_
                print("Aiming for Sell Delta:", instant_delta + max_change_above_)
        # ================================================================================
        # Set Target Delta to be Midpoint of Above/Below Delta if Less than Delta Range
        # ================================================================================
        elif instant_delta <= delta_above_:
            buy_delta = midpoint_delta
            print('\nInstant Delta is less than above delta')
            print('Aiming for Buy Delta: ', midpoint_delta)
            print('Not Placing Any Sell Orders This Loop.')

        else:
            raise Exception("Error: Unable to Compare Instant Delta to Above and Below Deltas")

        return buy_delta, sell_delta

    # =====================================================================================
    # Generate List of Bulk Orders From array_inputs List
    # ======================================================================================
    def __generate_arrays(self, buy_delta, sell_delta):
        order_list = []  # List of Order Dictionaries to be placed by BitMEX

        self.__b0 = self.__exchange_mgr.get_lastPrice(self.__symbol)  # Last Price

        w0 = self.__exchange_mgr.get_position_contractQty(self.__symbol) # Number of Contracts Held
        p0 = 100000000  # self.__exchange_mgr.get_margin_balance()/100000000 # Bitcoins Owned in Margin Balance
        b0 = self.__b0
        a0 = None
        if (self.__symbol == 'XBTUSD' or self.__symbol == 'XBTU17'):
            a0 = self.__exchange_mgr.get_indexPrice(self.__symbol)  # Index Price

        print("\nLast Price: " + str(b0))
        print("Margin Balance: " + str(p0))
        print("Contract Quantity: " + str(w0))

        # Loops through each set of inputs to generate separate arrays for each set
        for array_idx in range(len(self.__array_inputs)):

            # Set buy and sell deltas for individual arrays from find_delta_ranges()
            self.__array_inputs[array_idx]['buy_delta'] = buy_delta
            self.__array_inputs[array_idx]['sell_delta'] = sell_delta

            # Check whether skipping individual buy/sell arrays based on delta comparison
            if ((self.__array_inputs[array_idx]['buy_delta'] == None and self.__array_inputs[array_idx][
                'operation'] == 'buy') or
                    (self.__array_inputs[array_idx]['sell_delta'] == None and self.__array_inputs[array_idx][
                        'operation'] == 'sell')):
                continue

            # Generate Order_Qty for Every Array
            if self.__array_inputs[array_idx]['operation'] == 'sell':  # Delta Below
                try:
                    order_qty = all_currency_y_search(self.__array_inputs[array_idx]['operation'], self.__symbol,
                                                      self.__array_inputs[array_idx]['sell_delta'], w0, p0, b0,
                                                      self.__array_inputs[array_idx]['start_price_offset'],
                                                      self.__array_inputs[array_idx]['price_interval'],
                                                      self.__array_inputs[array_idx]['n_orders'], a0)
                except:
                    print('Invalid Order Quantity for Array: ' + str(self.__array_inputs[array_idx]))
                    print("Array will not be used due to exception being raised. Continuing loop.")
                    continue

            elif self.__array_inputs[array_idx]['operation'] == 'buy':
                try:
                    order_qty = all_currency_y_search(self.__array_inputs[array_idx]['operation'], self.__symbol,
                                                      self.__array_inputs[array_idx]['buy_delta'], w0, p0, b0,
                                                      self.__array_inputs[array_idx]['start_price_offset'],
                                                      self.__array_inputs[array_idx]['price_interval'],
                                                      self.__array_inputs[array_idx]['n_orders'], a0)
                except:
                    print('Invalid Order Quantity for Array: ' + str(self.__array_inputs[array_idx]))
                    print("Array will not be used due to exception being raised. Continuing loop.")
                    continue
            # ========================================================================================
            # Modify Order Qty to be Integer, Check if Above Minimum Order Qty
            # ========================================================================================
            print("Calculated contract quantity: " + str(order_qty))
            if (-self.__min_order_qty < round(order_qty) < self.__min_order_qty):
                print('Array', array_idx + 1, 'unused: calculated contract qty is below minimum:', self.__min_order_qty)
                continue  # not sure reason for symbol???? MICHELLE???
            # ===========================================================================================
            # Generate BitMEX dictionaries to be Placed as Bulk Orders
            # ===========================================================================================
            if self.__array_inputs[array_idx]['order_type'] == 'Limit':
                order_list.append(po.generate_limit_orders(self.__array_inputs[array_idx]['n_orders'],
                                                           b0 + self.__array_inputs[array_idx]['start_price_offset'],
                                                           self.__array_inputs[array_idx]['price_interval'],
                                                           self.__symbol,
                                                           round(order_qty),
                                                           abs(round(order_qty)),
                                                           self.__array_inputs[array_idx]['price_type']))

            elif self.__array_inputs[array_idx]['order_type'] == 'StopLimit':
                order_list.append(po.generate_stop_limit_orders(self.__array_inputs[array_idx]['n_orders'],
                                                                b0 + self.__array_inputs[array_idx][
                                                                    'start_price_offset'],
                                                                self.__array_inputs[array_idx]['price_interval'],
                                                                self.__symbol,
                                                                round(order_qty),
                                                                abs(round(order_qty)),
                                                                b0 + self.__array_inputs[array_idx]['trigger_offset'],
                                                                self.__array_inputs[array_idx]['trigger_interval'],
                                                                self.__array_inputs[array_idx]['price_type']))
        for array in order_list:
            print('\n', array)
            self.__exchange_mgr.create_bulk_orders(array)

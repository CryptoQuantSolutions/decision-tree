#from lib.exchange.bitmex.bitmex import BitMEX

import logging
from lib.utils.automation_equations import all_currency_y_search
import lib.utils.place_orders as po

from engine.arrays import Arrays

logger = logging.getLogger(__name__)

# ====================================================
# High Level "Master Set' Comparison Object
# Contains an Append Method to Add  'LowComp' objects
# =====================================================
class Comparison():
    def __init__(self, id, main_comparison):
        self.id = id
        self.main_comparison = main_comparison
        #self.deltas = [delta_above, max_change_above]
        self.symbol = ''
        self.child_comparisons = []
        self.order_arrays = []

        self.__min_order_qty = 20

        #self.__exchange_mgr = BitMEX()

        for array in Arrays().arrays:
            if array.id is self.id:
                self.add_order_array(array)

    def add_comparison(self, comp):
        self.child_comparisons.append(comp)

    def add_order_array(self, array):
        self.order_arrays.append(array)


    def set_symbol(self, symbol):
        self.symbol = symbol

    def cancel_orders(self):
        self.__exchange_mgr.cancel_all_orders(self.symbol)

    def find_delta(self, array, __exchange_mgr):
        instant_delta = __exchange_mgr.instant_delta(self.symbol)
        delta_above = array.deltas[0]
        delta_below = array.deltas[1]
        max_change_above = array.deltas[2]
        max_change_below = array.deltas[3]

        # This may be wrong
        midpoint_delta = round(((delta_above + delta_below) / 2), 8)

        # Target buy and sell delta as determined by comparing instant delta to delta ranges
        # Returns None if doesn't apply
        buy_delta = None
        sell_delta = None

        logger.info("Instantaneous Delta: " + str(instant_delta))

        # ================================================================================
        # Set Target Delta to be Midpoint of Above/Below Delta if Greater than Delta Range
        # ================================================================================
        if instant_delta >= delta_below:
            sell_delta = midpoint_delta     # If we take this out, what goes here?
            logger.info('Instant Delta is greater than below delta')
            logger.info('Aiming for Sell Delta: ' + str(midpoint_delta))
            logger.info('Not Placing Any Buy Orders This Loop.')
        # ================================================================================
        # Modify Target Delta using User Specified Change Values
        # ================================================================================
        elif delta_below > instant_delta > delta_above:

            # Check if Delta is Too Close to Below Side of Delta Range
            if abs(instant_delta - delta_below) < abs(max_change_below):
                buy_delta = delta_below
                logger.info("Aiming for Buy Delta:" + str(delta_below))
            else:
                buy_delta = instant_delta + max_change_below
                logger.info("Aiming for Buy Delta:" + str(instant_delta + max_change_below))

            # Check if Delta is Too Close to Above Side of Delta Range
            if abs(instant_delta - delta_above) < abs(max_change_above):
                sell_delta = delta_above
                logger.info("Aiming for Sell Delta:" + str(delta_above))
            else:
                sell_delta = instant_delta + max_change_above
                logger.info("Aiming for Sell Delta:" + str(instant_delta + max_change_above))
        # ================================================================================
        # Set Target Delta to be Midpoint of Above/Below Delta if Less than Delta Range
        # ================================================================================
        elif instant_delta <= delta_above:
            buy_delta = midpoint_delta
            logger.info('Instant Delta is less than above delta')
            logger.info('Aiming for Buy Delta: ' + str(midpoint_delta))
            logger.info('Not Placing Any Sell Orders This Loop.')

        return buy_delta, sell_delta


    def sum_last_price(self, price_list):
        sum = 0
        for price in price_list:
            sum += price

        return sum

    def interval_price_list(self, start_price, interval, n_orders):
        price_list = []
        current_price = start_price

        for interval_price in range(n_orders):
            price_list.append(current_price)
            current_price += interval_price

        return price_list

    def generate_arrays_price_list(self,  interval, n_orders, start_price=self.last_price):
        price_list = self.interval_price_list(start_price, interval, n_orders)

        return price_list

    def generate_arrays(self, __exchange_mgr):
        # Quick arrays hack
        #with open('arrays.txt', 'r') as file:
            #raw_data = eval(file.read())

        #self.order_arrays = raw_data[self.id]

        # order_arrays = Arrays()
        # 
        # for array in order_arrays.arrays:
        #     if array.id is self.id:
        #         self.order_arrays.append(array.generate_array())
        # order_arrays = []
        #
        # for array in self.order_arrays:
        #     order_arrays.append(array.generate_array())

        order_list = []  # List of Order Dictionaries to be placed by BitMEX

        self.__b0 = __exchange_mgr.get_lastPrice(self.symbol)  # Last Price

        w0 = __exchange_mgr.get_position_contractQty(self.symbol)  # Number of Contracts Held
        p0 = __exchange_mgr.get_margin_balance() / 100000000  # Bitcoins Owned in Margin Balance
        b0 = self.__b0
        a0 = None
        if (self.symbol == 'XBTUSD' or self.symbol == 'XBTU17'):
            a0 = __exchange_mgr.get_indexPrice(self.symbol)  # Index Price

        logger.info("Last Price: " + str(b0))
        logger.info("Margin Balance: " + str(p0))
        logger.info("Contract Quantity: " + str(w0))

        # Loops through each set of inputs to generate separate arrays for each set
        for array_index, array in enumerate(self.order_arrays):
            # Find deltas
            buy_delta, sell_delta = self.find_delta(array, __exchange_mgr)

            # Convert array object to dictionary
            array = array.generate_array()

            # Set buy and sell deltas for individual arrays from find_delta_ranges()
            array['buy_delta'] = buy_delta
            array['sell_delta'] = sell_delta

            # Check whether skipping individual buy/sell arrays based on delta comparison
            if ((array['buy_delta'] == None and array[
                'operation'] == 'buy') or
                    (array['sell_delta'] == None and array[
                        'operation'] == 'sell')):
                continue

            # Generate Order_Qty for Every Array
            if array['operation'] == 'sell':  # Delta Below
                price_list = self.generate_arrays_price_list(start_price, interval, n_orders)

                try:
                    order_qty = all_currency_y_search(array['operation'], self.symbol,
                                                      array['sell_delta'], w0, p0, b0,
                                                      array['start_price_offset'],
                                                      array['price_interval'],
                                                      array['n_orders'], a0, price_list)
                except:
                    logger.info('Invalid Order Quantity for Array: ' + str(array))
                    logger.info("Array will not be used due to exception being raised. Continuing loop.")
                    continue

            elif array['operation'] == 'buy':
                price_list = self.generate_arrays_price_list(start_price, interval, n_orders)

                try:
                    order_qty = all_currency_y_search(array['operation'], self.symbol,
                                                      array['buy_delta'], w0, p0, b0,
                                                      array['start_price_offset'],
                                                      array['price_interval'],
                                                      array['n_orders'], a0, price_list)
                except:
                    logger.info('Invalid Order Quantity for Array: ' + str(array))
                    logger.info("Array will not be used due to exception being raised. Continuing loop.")
                    continue
            # ========================================================================================
            # Modify Order Qty to be Integer, Check if Above Minimum Order Qty
            # ========================================================================================
            logger.info("Calculated contract quantity: " + str(order_qty))
            if (-self.__min_order_qty < round(order_qty) < self.__min_order_qty):
                logger.info('Array ' + str(array_index + 1) + ' unused: calculated contract qty is below minimum:' + str(self.__min_order_qty))
                continue  # not sure reason for symbol???? MICHELLE???
            # ===========================================================================================
            # Generate BitMEX dictionaries to be Placed as Bulk Orders
            # ===========================================================================================
            if order_qty > 0:
                if array['order_type'] == 'Limit':
                    order_list.append(po.generate_limit_orders(array['n_orders'],
                                                               b0 + array['start_price_offset'],
                                                               array['price_interval'],
                                                               self.symbol,
                                                               round(order_qty),
                                                               abs(round(order_qty)),
                                                               array['price_type']))

                elif array['order_type'] == 'StopLimit':
                    order_list.append(po.generate_stop_limit_orders(array['n_orders'],
                                                                    b0 + array[
                                                                        'start_price_offset'],
                                                                    array['price_interval'],
                                                                    self.symbol,
                                                                    round(order_qty),
                                                                    abs(round(order_qty)),
                                                                    b0 + array['trigger_offset'],
                                                                    array['trigger_interval'],
                                                                    array['price_type']))
            for array in order_list:
                logger.info(array)
                __exchange_mgr.create_bulk_orders(array)


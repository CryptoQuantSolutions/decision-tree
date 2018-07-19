from engine.orders import OrderArray

class Arrays():
    def __init__(self):
        # -- Place order arrays below
        # first = OrderArray(id, operation, price_type, order_type, max_above_delta, max_below_delta, max_change_sell, max_change_buying,
        #        start_price_offset, price_interval, n_orders, trigger_offset, trigger_interval)

        # Arrays for the 'fifth'
        first = OrderArray('fifth', 'buy', 'LastPrice', 'Limit', -200, 2.0, 0, 0.7, -17, -12, 17)
        second = OrderArray('fifth', 'buy', 'LastPrice', 'Limit', -200, 1.0, 0, 0.3, -5, -5, 17)

        # Arrays for the 'six'
        third = OrderArray('six', 'buy', 'LastPrice', 'Limit', -200, 1.0, 0, 0.7, -17, -12, 17)
        fourth = OrderArray('six', 'buy', 'LastPrice', 'Limit', -200, 0, 0, 0.3, -5, -5, 17)
        fifth = OrderArray('six', 'sell', 'LastPrice', 'Limit', -1, 200, -0.3, 0, 10, 7, 12)

        # Arrays for the 'seven'
        six = OrderArray('seven', 'buy', 'LastPrice', 'Limit', -200, 1.0, 0, 0.2, -17, -12, 7)
        seven = OrderArray('seven', 'sell', 'LastPrice', 'Limit', 0, 200, -0.3, 0, 10, 7, 6)

        # Arrays for the 'eighth'
        eight = OrderArray('eighth', 'buy', 'LastPrice', 'Limit', -200, 2.5, 0, 0.2, -17, -12, 7)
        nine = OrderArray('eighth', 'sell', 'LastPrice', 'Limit', 1.5, 200, -0.3, 0, 10, 7, 6)

        # Arrays for the 'nineth'
        ten = OrderArray('nineth', 'buy', 'LastPrice', 'Limit', -200, 0, 0, 0.2, -17, -12, 17)
        eleven = OrderArray('nineth', 'sell', 'LastPrice', 'Limit', -1, 200, -0.3, 0, 10, 7, 16)

        # Arrays for the 'tenth'
        twelve = OrderArray('tenth', 'buy', 'LastPrice', 'Limit', -200, 3.0, 0, 0.7, -17, -12, 17)
        thirteen = OrderArray('tenth', 'buy', 'LastPrice', 'Limit', -200, 2.0, 0, 0.3, -5, -5, 17)

        # Arrays for the 'eleventh'
        fourteen = OrderArray('eleventh', 'buy', 'LastPrice', 'Limit', -200, 2.0, 0, 0.7, -17, -12, 17)
        fifteen = OrderArray('eleventh', 'buy', 'LastPrice', 'Limit', -200, 1, 0, 0.3, -5, -5, 17)
        off = OrderArray('eleventh', 'sell', 'LastPrice', 'Limit', 0, 200, -0.3, 0, 10, 7, 12)

        # Arrays for the 'twelve'
        sixteen = OrderArray('twelve', 'buy', 'LastPrice', 'Limit', -200, 2.0, 0, 0.4, -17, -12, 17)
        seventeen = OrderArray('twelve', 'sell', 'LastPrice', 'Limit', 0.5, 200, -0.2, 0, 10, 7, 16)

        # Arrays for the 'thirteen'
        eighteen = OrderArray('thirteen', 'buy', 'LastPrice', 'Limit', -200, 5, 0, 0.5, -17, -12, 17)
        nineteen = OrderArray('thirteen', 'sell', 'LastPrice', 'Limit', 2.0, 200, -0.3, 0, 38, 7, 24)

        # Arrays for the 'fourteen'
        twenty = OrderArray('fourteen', 'buy', 'LastPrice', 'Limit', -200, 6, 0, 0.2, -17, -12, 17)
        twenty_one = OrderArray('fourteen', 'sell', 'LastPrice', 'Limit', 4, 200, -0.3, 0, 10, 7, 16)

        # Arrays for the 'fifteen'
        twenty_two = OrderArray('fifteen', 'buy', 'LastPrice', 'Limit', -200, 2.0, 0, 0.7, -17, -12, 17)
        twenty_three = OrderArray('fifteen', 'buy', 'LastPrice', 'Limit', -200, 1.0, 0, 0.3, -5, -5, 17)

        # Arrays for the 'sixteen'
        twenty_four = OrderArray('sixteen', 'buy', 'LastPrice', 'Limit', -200, 0.7, 0, 0.3, -17, -12, 17)
        twenty_five = OrderArray('sixteen', 'buy', 'LastPrice', 'Limit', -200, 0.7, 0, 0.2, -5, -5, 17)
        twenty_six = OrderArray('sixteen', 'sell', 'LastPrice', 'Limit', -0.3, 200, -0.2, 0, 10, 7, 12)

        # Arrays for the 'seventeen'
        twenty_seven = OrderArray('seventeen', 'buy', 'LastPrice', 'Limit', -200, 2.5, 0, 0.4, -17, -12, 17)
        twenty_eight = OrderArray('seventeen', 'sell', 'LastPrice', 'Limit', 0.75, 200, -0.2, 0, 10, 7, 16) # offset, interval, orders

        # Arrays for the 'eighteen'
        twenty_nine = OrderArray('eighteen', 'buy', 'LastPrice', 'Limit', -200, 8, 0, 0.8, -17, -12, 17)
        thirty = OrderArray('eighteen', 'sell', 'LastPrice', 'Limit', 5.5, 200, -0.4, 0, 18, 7, 24)

        # Arrays for the 'nineteen'
        thirty_one = OrderArray('nineteen', 'buy', 'LastPrice', 'Limit', -200, 3.5, 0, 0.3, -37, -12, 17)
        thirty_two = OrderArray('nineteen', 'sell', 'LastPrice', 'Limit', 2, 200, -0.3, 0, 2, 7, 16)

        self.arrays = []

        self.arrays.append(first)
        self.arrays.append(second)
        self.arrays.append(third)
        self.arrays.append(fourth)
        self.arrays.append(fifth)
        self.arrays.append(six)
        self.arrays.append(seven)
        self.arrays.append(eight)
        self.arrays.append(nine)
        self.arrays.append(ten)
        self.arrays.append(eleven)
        self.arrays.append(twelve)
        self.arrays.append(thirteen)
        self.arrays.append(fourteen)
        self.arrays.append(fifteen)
        self.arrays.append(off)
        self.arrays.append(sixteen)
        self.arrays.append(seventeen)
        self.arrays.append(eighteen)
        self.arrays.append(nineteen)
        self.arrays.append(twenty)
        self.arrays.append(twenty_one)
        self.arrays.append(twenty_two)
        self.arrays.append(twenty_three)
        self.arrays.append(twenty_four)
        self.arrays.append(twenty_five)
        self.arrays.append(twenty_six)
        self.arrays.append(twenty_seven)
        self.arrays.append(twenty_eight)
        self.arrays.append(twenty_nine)
        self.arrays.append(thirty)
        self.arrays.append(thirty_one)
        self.arrays.append(thirty_two)


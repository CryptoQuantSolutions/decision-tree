from engine.variable_reader import Datafeed, EMA, SMA, Acceleration
from lib.exchange.bitmex.bitmex import BitMEX
import datetime

class Variables():
    def __init__(self):
        ## -- Place Variables below
        self.last = Datafeed('bitmex', 'last', 'btc-usd')
        self.a = Datafeed('bitmex', 'last', 'btc-usd').evaluate()
        self.b = Datafeed('bitmex', 'index', 'btc-usd').evaluate()
        self.c = Datafeed('bitmex', 'mark', 'btc-usd').evaluate()
        self.d = float(10800)   # Min
        self.e = float(11800)   # Max
        self.f = SMA(self.last, 30, 15).evaluate()
        self.f1 = self.f + 165
        self.f2 = self.f + 67
        self.f3 = self.f + -67
        self.f4 = self.f + -165
        self.g = EMA(self.last, 25, 15).evaluate()
        self.bitmex_balance = BitMEX().get_margin_balance()/100000000
        #self.bitmex_indexprice_vol = Volatility(self.bitmex_indexprice, 1440, 1)
        #self.bitmex_lastprice_accel = Acceleration(self.bitmex_indexprice, 3, 1)




import unittest
from engine.variable_reader import EMA, SMA, Datafeed
from engine.trade_engine import TradeEngine

class TradeEngineTest(unittest.TestCase):
    def setUp(self):
        # Set the feed to test on
        #self.index_feed = Datafeed('bitmex', 'index', 'btc-usd')
        self.test_engine = TradeEngine()

    def test_get_account_balance(self):
        balance = self.test_engine.get_account_balance()/100000000

        if balance is not None:
            print("Current balance: " + str(balance))
        else:
            print("Error: problem retrieving balance.")


    # # Test prints out dataframe of EMA evaluated price points
    # def test_ema(self):
    #     ema = EMA(self.index_feed, 25, 30)
    #
    #     print('\n\n-- EMA Test Results --\n\n')
    #     print(ema.evaluate())
    #
    # # Test prints out dataframe of SMA evaluated price points
    # def test_sma(self):
    #     sma = SMA(self.index_feed, 30, 30)
    #
    #     print('\n\n-- SMA Test Results --\n\n')
    #     print(sma.evaluate())

if __name__ == "__main__":
    unittest.main()
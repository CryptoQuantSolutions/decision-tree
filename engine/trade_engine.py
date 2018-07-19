#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 20:27:06 2017

@author: alex_vo
"""

def display_ascii_logo():
    # Load ascii art
    with open(r'E:\programs\crypto\BitMexBot_new\BitMexBot_New\logo_ascii.txt') as file:
        content = file.readlines()

    # Strip '\n' (newline) characters
    content = [line.replace('\n', '') for line in content]

    # Display ascii art logo
    for line in content:
        print(line)

    print()

import logging
from config.settings import settings

logger = None

display_ascii_logo()
#setup_root_logger()

import logging

import engine.variable_reader as variable_reader
import engine.comparison_reader as comparison_reader
import lib.exchange.bitmex.bitmex as bitmex
import lib.database.tabledef as db

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from lib.log.log import setup_custom_logger

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from time import sleep
import datetime

from lib.error.ServerMoveFiles import *

#logger = setup_custom_logger('root')

engine = create_engine("postgresql+psycopg2://postgres:haze9856@192.168.1.146:5432/crypto_test_too", echo=False)

class TradeEngine():
    def __init__(self):
        # Name of account
        self.account_name = 'lovemyself'

        # Exchnage
        self.__exchange_mgr = bitmex.BitMEX()

        self.DBSession = sessionmaker(bind=engine)
        self.session = self.DBSession()

        #self.var_mgr = variable_reader.VariableMgr()
        self.comp_mgr = comparison_reader.ComparisonsMgr(self.__exchange_mgr)

        #self.logger = setup_custom_logger('root')
        self.logger = self.setup_root_logger()

    def setup_root_logger(self):
        formatter = logging.Formatter(fmt='%(asctime)s: %(levelname)s: %(module)s: %(message)s')

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger = logging.getLogger(__name__)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        return logger

    def get_account_balance(self):
        try:
            return self.__exchange_mgr.get_margin_balance()/100000000 #['account']
        except:
            return None

    # Main point of execution
    def run_trade_engine(self):
        try:
            self.logger.info('Running trade engine')

            # Keep track of balance
            current_balance = self.get_account_balance() #self.__exchange_mgr.get_current_balance()['account']
            self.logger.info('Current Balance: ' + str(current_balance))
            account = db.Account(datetime.datetime.now(), self.account_name, current_balance)

            # Save to database
            self.session.add(account)

            # Commit save
            self.session.commit()

            # Reset values
            self.comp_mgr.comparisons_obj.get_new_values()

            return self.comp_mgr.eval_comps()

        except Exception as e:
            ssh = SSHConnection()
            ssh.put()
            ssh.close()


##
## Temporary point of Execution
##
if __name__ == '__main__':
    # ======================================================
    # Sample Run through
    # You might run trade engine every 'x-seconds' so call 'run_trade_engine' every x-seconds
    # ======================================================
    trade_engine = TradeEngine()
    is_first = True

    for iter in range(36):
        result = trade_engine.run_trade_engine()

        if result is not None:
            for item in result:
                print('buy delta: ' + str(item['buy']))
                print('sell delta: ' + str(item['sell']))

        if is_first is not True:
            sleep(900)

        is_first = False
        # trade_engine.mytest_ema()
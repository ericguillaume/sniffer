# python3 main_bot.py | tee -a XXX
# import time
# import json
# import random
# import threading
# from urllib.request import urlopen


# from config import SYMBOLS
# from utils import is_symbol_in_usdt, convert_symbol_into_usdt, log



# class Symbol:
#
#   def __init__(self, name):
#     self.name = name
#     self.is_symbol_usdt = is_symbol_in_usdt(name)
#     self.usdt_name = convert_symbol_into_usdt(name)















# test current symbol price getter
# prices_manager = AllSymbolPricesManager()
# symbol = "BTCUSDT"
# seconds_between_queries = 0.1
# t = ThreadUpdatePricesBinance(prices_manager, symbol, seconds_between_queries)
# t.start()
# time.sleep(5)
#
# timestamp = time.time()
#
# container = prices_manager.get_container(symbol)
# print(container.array_timestamp_price)
# print("timestamp = {}".format(timestamp))
# print(container.get_price(timestamp)) # pk un calllll ici ???
# print(container.get_price(timestamp - 1000)) # pk si ici 10 il faut un cal
















# test price container
# random.seed(8)
#
# symbol = "BTCUSDT"
# s = SymbolPricesContainer(symbol)
# for i in range(20):
#   s.add_price(time.time() + random.randint(1, 40), 1)
#   s.add_price(random.randint(1, 10000), 1)
#   time.sleep(0.1)
#
# print(s.array_timestamp_price)
#
# last_t = -1000000
# for t, price in s.array_timestamp_price:
#   print(t)
#   if t < last_t:
#     print("error t: {} < last_t : {}".format(t, last_t))
#   last_t = t
# print("all good")




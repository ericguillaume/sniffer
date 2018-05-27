import time
import json
import threading
from urllib.request import urlopen

from utils import log
from bot.time_manager.time_manager import TimeManager



class UpdatePrices():
  def __init__(self, selected_symbols, price_manager, seconds_between_queries):
    self.price_manager = price_manager
    self.threads = [ThreadUpdateSymbolPrices(symbol, price_manager, seconds_between_queries) for symbol in selected_symbols]

  def start(self):
    for thread in self.threads:
      thread.start()


class ThreadUpdateSymbolPrices(threading.Thread):
  def __init__(self, symbol, price_manager, seconds_between_queries):
    threading.Thread.__init__(self)
    self.symbol = symbol
    self.seconds_between_queries = seconds_between_queries
    self.price_manager = price_manager
    if TimeManager.is_live():
      self.price_manager.get_current_symbol_price(self.symbol) # add a first price so that the price_manager is not empty

  def run(self):
    if TimeManager.is_debug():
      return True

    if TimeManager.is_offline():
      last_timestamp_queried = TimeManager.time() - 3600
      while TimeManager.time_changed_event.wait():
        if not TimeManager.should_continue():
          break
          
        new_timestamp_to_query = TimeManager.time() - 3600
        if new_timestamp_to_query >= last_timestamp_queried + 500 * 60:
          log("going to call get_kline_hour_symbol_price")
          self.price_manager.get_kline_hour_symbol_price(self.symbol, new_timestamp_to_query)
          last_timestamp_queried = new_timestamp_to_query


    if TimeManager.is_live():
      while True:
        self.price_manager.get_current_symbol_price(self.symbol)
        time.sleep(self.seconds_between_queries)




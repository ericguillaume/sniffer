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
    if TimeManager.is_offline():
      timestamp_to_query = TimeManager.time() - 3600

  def run(self):
    if TimeManager.is_debug():
      return True

    thread_just_started = True
    last_timestamp_queried = 0
    if TimeManager.is_offline():
      while thread_just_started or TimeManager.time_changed_event.wait():
        if not TimeManager.should_continue():
          break
          
        new_timestamp_to_query = TimeManager.time() - 3600
        if thread_just_started or new_timestamp_to_query >= last_timestamp_queried + 100 * 60:
          log("going to call get_kline_hour_symbol_price")
          self.price_manager.get_kline_hour_symbol_price(self.symbol, new_timestamp_to_query)
          last_timestamp_queried = new_timestamp_to_query

        thread_just_started = False


    if TimeManager.is_live():
      while True:
        self.price_manager.get_current_symbol_price(self.symbol)
        log("going to sleep {} s".format(self.seconds_between_queries))
        time.sleep(self.seconds_between_queries)




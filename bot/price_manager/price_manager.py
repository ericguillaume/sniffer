import time
import json
import threading
from urllib.request import urlopen

from utils import log, is_symbol_in_usdt, unstring_float
from bot.time_manager.time_manager import TimeManager



class PriceManager:
  def __init__(self, selected_symbols, qlm, debug_delay):
    self.qlm = qlm
    self.d_symbol_prices_mgr = {}
    for symbol in selected_symbols:
       self.d_symbol_prices_mgr[symbol] = SymbolPriceManager(symbol, qlm, debug_delay)

  def get_last_usdt_prices(self, symbols): # on taffe avec les symbols initiaux, osef des usdt, il sont geres ici ...
    last_btc_price = self.get_last_btc_price()

    d_symbol_last_price = {} ## todo paralleliser si ca prend du temps de faire ces demandes !!!!!!!!!!!!!
    for symbol in symbols:
      coeff = 1.0 if is_symbol_in_usdt(symbol) else last_btc_price
      symbol_last_price = self.d_symbol_prices_mgr[symbol].get_last_price()
      d_symbol_last_price[symbol] = coeff * symbol_last_price
    return d_symbol_last_price

  def get_one_hour_ago_usdt_prices(self, symbols):
    old_timestamp = TimeManager.time() - 3600
    old_btc_price = self.get_btc_price(old_timestamp)

    d_symbol_old_price = {} ## todo paralleliser si ca prend du temps de faire ces demandes !!!!!!!!!!!!!, chronometrerrrrr
    for symbol in symbols:
      coeff = 1.0 if is_symbol_in_usdt(symbol) else old_btc_price
      d_symbol_old_price[symbol] = coeff * self.d_symbol_prices_mgr[symbol].get_price(old_timestamp)
    return d_symbol_old_price

  def get_current_symbol_price(self, symbol):
    if TimeManager.is_live():
      success, price, timestamp = self.d_symbol_prices_mgr[symbol].do_get_current_price()
      return success, price, timestamp
    else:
      return True, self.d_symbol_prices_mgr[symbol].get_price(TimeManager.time()), TimeManager.time() # dernier truc est pas vraiment le timestamp du price !!!!!

  def get_kline_hour_symbol_price(self, symbol, timestamp):
    self.d_symbol_prices_mgr[symbol].get_kline_hour_symbol_price(timestamp)

  # private methods

  def get_last_btc_price(self): # renommer get current price si c'est le prix recent qu on veut ????
    return self.d_symbol_prices_mgr["BTCUSDT"].get_last_price() # mettre un cache ici, ptet trop d appel sinon ??

  def get_btc_price(self, timestamp):
    return self.d_symbol_prices_mgr["BTCUSDT"].get_price(timestamp)






class SymbolPriceManager:
  max_time_to_cache_prices = 20 * 3600
  max_added_prices_before_cleaning = 100
  max_time_price_can_be_late = 45

  # verifier
  def __init__(self, symbol, qlm, debug_delay):
    self.qlm = qlm
    self.debug_delay = debug_delay
    self.symbol = symbol
    self.array_timestamp_price = []
    self.added_prices_since_last_cache_clean = 0
    self.lock = threading.Lock()

  # not thread safe
  def get_first_older_element_index(self, timestamp):
    for idx, t_and_price in enumerate(self.array_timestamp_price): # peut on mettre du t, price ici  (sans enumerate marchait ??)
      t = t_and_price[0]
      if t > timestamp:
        return idx
    return len(self.array_timestamp_price)

  def add_price(self, timestamp, price):
    self.lock.acquire()
    index_to_insert = self.get_first_older_element_index(timestamp)
    self.array_timestamp_price.insert(index_to_insert, (timestamp, price))
    self.lock.release()

    self.clean_old_positions_if_need_be()

  # not thread safe 
  def do_add_price(self, timestamp, price):
    index_to_insert = self.get_first_older_element_index(timestamp)
    self.array_timestamp_price.insert(index_to_insert, (timestamp, price))

  def add_many_prices(self, array_timestamps_prices):
    self.lock.acquire()
    for timestamp_price in array_timestamps_prices:
      timestamp = timestamp_price[0]
      price = timestamp_price[1]
      self.do_add_price(timestamp, price)
    self.lock.release()

    for _ in range(len(array_timestamps_prices)):
      self.clean_old_positions_if_need_be()

  def clean_old_positions_if_need_be(self):
    self.added_prices_since_last_cache_clean += 1
    if self.added_prices_since_last_cache_clean >= SymbolPriceManager.max_added_prices_before_cleaning:
      self.clean_old_positions()

  def clean_old_positions(self):
    timestamp = TimeManager.time()
    self.lock.acquire()
    self.array_timestamp_price = [x for x in self.array_timestamp_price if
                                  x[0] >= timestamp - SymbolPriceManager.max_time_to_cache_prices and
                                  x[0] <= timestamp + SymbolPriceManager.max_time_to_cache_prices]  # does it keep order
    self.lock.release()
    self.added_prices_since_last_cache_clean = 0

  # attention price can be very very far :/    FETCH IT IF NEED BE
  def get_price(self, timestamp): # tester temps, si marche pas passer en dichotomie
    self.lock.acquire()

    has_searched = True
    if len(self.array_timestamp_price) == 0:
      has_searched = False

    is_smallest_distance_defined = False
    smallest_distance = 0.0
    smallest_distance_price = 0.0
    smallest_distance_timestamp = 0.0
    for t, price in self.array_timestamp_price:
      distance = abs(timestamp - t)
      if not is_smallest_distance_defined:
        smallest_distance = distance
        smallest_distance_price = price
        smallest_distance_timestamp = t
        is_smallest_distance_defined = True
      else:
        if distance <= smallest_distance:
          smallest_distance = distance
          smallest_distance_price = price
          smallest_distance_timestamp = t
    self.lock.release()

    #log("smallest_distance = {}".format(smallest_distance))
    if has_searched and smallest_distance <= SymbolPriceManager.max_time_price_can_be_late:
      if self.debug_delay:
        log("DEBUG get_price: FOUND {} late by {} s".format(self.symbol, timestamp - smallest_distance_timestamp))
      return smallest_distance_price
    else:
      ticker_timpestamp, price = self.query_and_add_price(timestamp)
      if self.debug_delay:
        log("DEBUG get_price: QUERIED {} late by {} s".format(self.symbol, timestamp - ticker_timpestamp))
      return price

  def get_last_price(self): # attention peut fail, prix peut etre plus vieux d une minute... si cest btc ou eth on veut casser l algo et pas le faire .!!
    if TimeManager.is_live():
      self.lock.acquire()
      if self.debug_delay:
        log("DEBUG get_last_price late by {} s".format(TimeManager.time() - self.array_timestamp_price[-1][0]))
      timpestamp_price = self.array_timestamp_price[-1][1] #### si vide demander le prix !!
      self.lock.release()
      return timpestamp_price
    else:
      return self.get_price(TimeManager.time())


  # those methods do external calls
  def query_and_add_price(self, timestamp): # try twice catch error    # devrait pas etre la et enlever les import de urllopen, json
    if TimeManager.is_offline():
      self.do_get_kline_hour_symbol_price(timestamp)

    self.qlm.queried()

    one_minute_in_ms = 60000
    timestamp_in_ms = int(timestamp * 1000)
    limit = 500

    url_to_call = "https://api.binance.com/api/v1/klines?symbol={}&interval=1m&limit={}&startTime={}&endTime={}" \
      .format(self.symbol, limit, timestamp_in_ms - one_minute_in_ms, timestamp_in_ms + one_minute_in_ms)
    html = urlopen(url_to_call)

    result_code = html.getcode()
    if result_code == 200:
      data = html.read().decode("utf-8")
      data = json.loads(data)
      array_t_prices = [[float(x[0]) / 1000.0, float(x[1])] for x in data] # assert les types plus haut !!!!!!!!!!!!!!!!!!!!!!!!

      for timestamp, price in array_t_prices:
        self.add_price(timestamp, price) # dichotomie permet de se contenter de faire ca !!!  GERER CAS D ERREUR ICI   THROW ERROR SI RIEN.   # shouldnot add price here maybe ??
      if abs(array_t_prices[0][0] - timestamp) < abs(array_t_prices[1][0] - timestamp):
        return array_t_prices[0]
      else:
        return array_t_prices[1]
    else:
      raise Exception("ERROR query_and_add_price didnt return anything for symbol: {} and timestamp: {}".format(self.symbol, timestamp))

  # works only with btc prices not usdt
  def do_get_current_price(self):
    if not TimeManager.is_live():
      raise Exception("ERROR do_get_current_price called in not livez mode")

    try:
      self.qlm.queried()

      url_to_call = "https://api.binance.com/api/v3/ticker/price?symbol={}".format(self.symbol)
      html = urlopen(url_to_call)
      result_code = html.getcode()
      if result_code == 200:
        timestamp = time.time()  # LATER: peut etre verifier que ca ait pas mis plus que x seconds a arriver !! logger ca et visualiser les logs
        data = html.read().decode("utf-8")
        data = json.loads(data)
        price = float(data["price"])
        self.add_price(timestamp, price)
        return True, price, timestamp
      else:
        log("error result_code = {}".format(result_code))
        return False, 0.0, 0.0
    except Exception as e:
      log(e)
      return False, 0.0, 0.0

  # for offline thread only
  def do_get_kline_hour_symbol_price(self, timestamp):
    if not TimeManager.is_offline():
      raise Exception("ERROR do_get_kline_hour_symbol_price called not in offline mode")

    limit = 500

    try:
      self.qlm.queried()

      timestamp_in_ms = int(timestamp * 1000)
      url_to_call = "https://api.binance.com/api/v1/klines?symbol={}&interval=1m&limit={}&startTime={}" \
        .format(self.symbol, limit, timestamp_in_ms)
      html = urlopen(url_to_call)
      result_code = html.getcode()
      if result_code == 200:
        data = html.read().decode("utf-8")
        data = json.loads(data)
        
        array_timestamps_prices = [[unstring_float(row[0]) / 1000, float(row[1])] for row in data if len(row) == 12]
        self.add_many_prices(array_timestamps_prices)

      else:
        print("error result_code = {}".format(result_code))
    except Exception as e:
      print(e)
      pass



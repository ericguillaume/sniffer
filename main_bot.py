import time
import json
import random
import threading
from urllib.request import urlopen


from config import SYMBOLS
from utils import is_symbol_in_usdt, convert_symbol_into_usdt



# class Symbol:
#
#   def __init__(self, name):
#     self.name = name
#     self.is_symbol_usdt = is_symbol_in_usdt(name)
#     self.usdt_name = convert_symbol_into_usdt(name)


class AllSymbolPricesManager:
  def __init__(self):
    self.d_symbol_container = {}

  def add_symbol(self, symbol, seconds_between_queries):
    self.d_symbol_container[symbol] = SymbolPricesContainer(symbol, seconds_between_queries)
    return self.d_symbol_container[symbol]

  def get_container(self, symbol):
    return self.d_symbol_container[symbol]

  def get_last_usdt_prices(self, symbols): # on taffe avec les symbols initiaux, osef des usdt, il sont geres ici ...
    last_btc_price = self.get_last_btc_price()

    d_symbol_last_price = {} ## todo paralleliser si ca prend du temps de faire ces demandes !!!!!!!!!!!!!
    for symbol in symbols:
      coeff = 1.0 if is_symbol_in_usdt(symbol) else last_btc_price
      symbol_last_price = self.d_symbol_container[symbol].get_last_price()
      d_symbol_last_price[symbol] = coeff * symbol_last_price
    return d_symbol_last_price

  def get_one_hour_ago_usdt_prices(self, symbols):
    old_timestamp = time.time() - 3600
    old_btc_price = self.get_btc_price(old_timestamp)

    d_symbol_old_price = {} ## todo paralleliser si ca prend du temps de faire ces demandes !!!!!!!!!!!!!, chronometrerrrrr
    for symbol in symbols:
      coeff = 1.0 if is_symbol_in_usdt(symbol) else old_btc_price
      d_symbol_old_price[symbol] = coeff * self.d_symbol_container[symbol].get_price(old_timestamp)
    return d_symbol_old_price

  def get_last_btc_price(self): # renommer get current price si c'est le prix recent qu on veut ????
    return self.d_symbol_container["BTCUSDT"].get_last_price() # mettre un cache ici, ptet trop d appel sinon ??

  def get_btc_price(self, timestamp):
    return self.d_symbol_container["BTCUSDT"].get_price(timestamp)




class SymbolPricesContainer:
  max_time_to_cache_prices = 2 * 3600
  max_added_prices_before_cleaning = 100

  # verifier
  def __init__(self, symbol, seconds_between_queries):
    self.symbol = symbol
    self.seconds_between_queries = seconds_between_queries
    self.array_timestamp_price = []
    self.added_prices_since_last_cache_clean = 0

  def get_first_older_element_index(self, timestamp): # add lock
    for idx, t_and_price in enumerate(self.array_timestamp_price): # peut on mettre du t, price ici  (sans enumerate marchait ??)
      t = t_and_price[0]
      if t > timestamp:
        return idx
    return len(self.array_timestamp_price)

  def add_price(self, timestamp, price):
    index_to_insert = self.get_first_older_element_index(timestamp)
    self.array_timestamp_price.insert(index_to_insert, (timestamp, price))

    self.clean_old_positions_if_need_be()

  def clean_old_positions_if_need_be(self):
    self.added_prices_since_last_cache_clean += 1
    if self.added_prices_since_last_cache_clean >= SymbolPricesContainer.max_added_prices_before_cleaning:
      self.clean_old_positions()

  def clean_old_positions(self):
    timestamp = time.time()
    self.array_timestamp_price = [x for x in self.array_timestamp_price if
                                  x[0] >= timestamp - SymbolPricesContainer.max_time_to_cache_prices]  # does it keep order
    self.added_prices_since_last_cache_clean = 0

  def query_and_add_price(self, timestamp): # try twice catch error
    one_minute_in_ms = 60000
    timestamp_in_ms = int(timestamp * 1000)
    limit = 500

    url_to_call = "https://api.binance.com/api/v1/klines?symbol={}&interval=1m&limit={}&startTime={}&endTime={}" \
      .format(self.symbol, limit, timestamp_in_ms - one_minute_in_ms, timestamp_in_ms + one_minute_in_ms)
    #print("query_and_add_price going to call {}".format(url_to_call))
    html = urlopen(url_to_call)

    result_code = html.getcode()
    if result_code == 200:
      data = html.read().decode("utf-8")
      data = json.loads(data)
      array_t_prices = [[float(x[0]) / 1000.0, float(x[1])] for x in data] # assert les types plus haut !!!!!!!!!!!!!!!!!!!!!!!!

      for timestamp, price in array_t_prices:
        self.add_price(timestamp, price) # dichotomie permet de se contenter de faire ca !!!  GERER CAS D ERREUR ICI   THROW ERROR SI RIEN
      return array_t_prices[-1][1]
    else:
      raise Exception("ERROR query_and_add_price didnt return anything for symbol: {} and timestamp: {}".format(symbol, timestamp))


  # attention price can be very very far :/    FETCH IT IF NEED BE
  def get_price(self, timestamp): # tester temps, si marche pas passer en dichotomie
    if len(self.array_timestamp_price) == 0:
      raise Exception("ERROR price asked while there was none for symbol = {}".format(symbol))

    is_smallest_distance_defined = False
    smallest_distance = 0.0
    smallest_distance_price = 0.0
    for t, price in self.array_timestamp_price:
      distance = abs(timestamp - t)
      if not is_smallest_distance_defined:
        smallest_distance = distance
        smallest_distance_price = price
        is_smallest_distance_defined = True
      else:
        if distance <= smallest_distance:
          smallest_distance = distance
          smallest_distance_price = price

    #print("smallest_distance = {}".format(smallest_distance))
    if smallest_distance <= self.seconds_between_queries:
      return smallest_distance_price
    else:
      return self.query_and_add_price(timestamp)

  def get_last_price(self): # attention peut fail, prix peut etre plus vieux d une minute... si cest btc ou eth on veut casser l algo et pas le faire .!!
    return self.array_timestamp_price[-1][1] #### si vide demander le prix !!







class ThreadUpdatePricesBinance(threading.Thread):
  def __init__(self, prices_manager, symbol, seconds_between_queries):
    threading.Thread.__init__(self)
    self.symbol = symbol
    self.prices_manager = prices_manager
    self.symbol_prices_container = prices_manager.add_symbol(symbol, seconds_between_queries)
    self.seconds_between_queries = seconds_between_queries

  def run(self):
    #while True: debug todo
    i = 0
    while i <= 5: # debug
      i += 1
      self.get_current_symbol_price()
      time.sleep(self.seconds_between_queries)

  def get_current_symbol_price(self):
    success, price, timestamp = do_get_current_price(self.symbol)
    if success:
      self.symbol_prices_container.add_price(timestamp, price)


def do_get_current_price(symbol): # on manipule des USDT OU DES BTC ICI ???
  try:
    url_to_call = "https://api.binance.com/api/v3/ticker/price?symbol={}".format(symbol)
    # print("get_current_symbol_price: going to call {}".format(url_to_call))
    html = urlopen(url_to_call)
    result_code = html.getcode()
    if result_code == 200:
      timestamp = time.time()  # peut etre verifier que ca ait pas mis plus que x seconds a arriver !! logger ca et visualiser les logs
      data = html.read().decode("utf-8")
      data = json.loads(data)
      price = float(data["price"])
      return True, price, timestamp
    else:
      print("error result_code = {}".format(result_code))
      return False, 0.0, 0.0
  except Exception as e:
    print(e)
    return False, 0.0, 0.0


bucket_middle = 0.003 # sure ou 0.004 ???      0 ???
def get_bucket(value):
  if value <= -bucket_middle:
    return -1
  elif value >= -bucket_middle and value <= bucket_middle:
    return 0
  elif value >= bucket_middle:
    return 1




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






class BuyManager(threading.Thread):
  def __init__(self, symbol, keep_for_k_minutes, buy_price):
    threading.Thread.__init__(self)
    self.symbol = symbol
    self.keep_for_k_minutes = keep_for_k_minutes
    self.buy_price = buy_price

  def run(self):
    print("we are going to buy {}".format(symbol))
    buy_time = time.time()

    ## buy here

    time.sleep(self.keep_for_k_minutes * 60)
    sell_time = time.time()
    success, sell_price, _ = do_get_current_price(self.symbol)  # try twice
    if not success:
      print("couldn't sell {} bought at time {} price {}, sell at time :{}"\
            .format(self.symbol, buy_time, self.buy_price, sell_time))
      return True

    # sell

    print("sell_price = {}".format(sell_price))
    profit = sell_price - self.buy_price
    relative_profit = profit / self.buy_price
    print("SOLD {}: relative_profit = {}  ---  bought at time {} price {}, sell at time: {}, price: {}"\
            .format(self.symbol, relative_profit, buy_time, self.buy_price, sell_time, sell_price))
    return True






selected_symbols = SYMBOLS[:30] # limiter later
prices_manager = AllSymbolPricesManager()

seconds_between_queries = 0.1
threads = [ThreadUpdatePricesBinance(prices_manager, symbol, seconds_between_queries) for symbol in selected_symbols]
for thread in threads:
  thread.start()
time.sleep(3)





keep_for_k_minutes = 10

d_symbol_diff = {} # its the usdt diff
d_symbol_relative_diff = {} # its the usdt diff
d_symbol_bucket = {} # its the usdt bucket
d_symbol_t_before_retrying = {}
dont_touch_same_currency_for_n_minutes = 50 # todo at start how can it be ????? evaluate !!!!!!!!!!!!!!

timestamp = time.time()
for symbol in selected_symbols:
  d_symbol_t_before_retrying[symbol] = 0 # timestamp + (60 * 1) # timestamp + dont_touch_same_currency_for_n_minutes ??????   attention secondes minutes

while True:
  print("entering big loop to check for BUYING, t: {}".format(int(time.time())))
  # compute diffs, buckets etc..
  d_symbol_last_price = prices_manager.get_last_usdt_prices(selected_symbols)
  d_symbol_old_price = prices_manager.get_one_hour_ago_usdt_prices(selected_symbols)
  domain_diffs = 0.0
  for symbol in selected_symbols:
    cur_price = d_symbol_last_price[symbol]
    old_price = d_symbol_old_price[symbol]
    diff = (cur_price - old_price)
    d_symbol_diff[symbol] = diff
    relative_diff = diff / old_price
    d_symbol_relative_diff[symbol] = relative_diff
    bucket = get_bucket(relative_diff)
    d_symbol_bucket[symbol] = bucket
    #print("{} - cur_price: {}, old_price: {}, diff / old_price: {},bucket : {} ".format(symbol, cur_price, old_price, (diff / old_price), bucket))
    domain_diffs += bucket
  domain_diffs /= len(selected_symbols)
  print("domain_diffs: {}".format(domain_diffs))

  # decision or not to buy
  # todo minutes_before_retrying

  min_diff_domains_to_buy_or_sell = 0.90 # 0.8 ????
  for symbol in selected_symbols:

    #diff = d_symbol_diff[symbol]   pas ca ?????
    if not (domain_diffs >= min_diff_domains_to_buy_or_sell):
      continue

    if not time.time() >= d_symbol_t_before_retrying[symbol]: # mettre un lock la dessus aussi ou pas ???
      #print("timestamps is too young")
      continue

    bucket = d_symbol_bucket[symbol]
    diff = d_symbol_diff[symbol]
    diff = d_symbol_diff[symbol]
    relative_diff = d_symbol_relative_diff[symbol]
    condition_to_buy = (bucket == 1 and diff <= 0.005) # relative_diff # RD pk c est statique ca ??? et pas dynamique ??      WARNING:::: diff / price[0] EST CE BIEN COMME CA LAUTRE le jupyter
    if not condition_to_buy:
      #print("no condition to buy: bucket={}, relative_diff={}".format(bucket, relative_diff))
      continue

    # buying
    success, buy_price, _ = do_get_current_price(symbol) # try twice
    if not success:
      continue

    d_symbol_t_before_retrying[symbol] = time.time() + (dont_touch_same_currency_for_n_minutes * 60)
    buy = BuyManager(symbol, keep_for_k_minutes, buy_price)
    buy.start()
  time.sleep(30)







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




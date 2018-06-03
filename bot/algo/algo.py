# python3 -m bot.algo.algo | tee -a XXX
import time

from config import SYMBOLS
from utils import log
from bot.time_manager.time_manager import TimeManager
from bot.price_cache.redis_cache import RedisCache
from bot.price_manager.query_limit_manager import QueryLimitManager
from bot.price_manager.price_manager import PriceManager
from bot.update_prices.update_prices import UpdatePrices
from bot.buy_manager.buy_manager import BuyManager



class Algo():

  def __init__(self):
      pass

  def start(self):
    # algo params
    number_currencies_kept = 30 # limiter LATER
    bucket_middle = 0.003 # sure ou 0.004 ???      0 ???
    keep_for_k_minutes = 10
    dont_touch_same_currency_for_n_minutes = 50 # todo at start how can it be ????? evaluate !!!!!!!!!!!!!!
    diff_domain_buy_trigger = 0.6
    diff_upper_buy_condition = 0.005


    # platform params
    debug_delay = False


    start_timestamp = 1524861267
    end_timestamp = 1526810400 
    TimeManager.set_offline(start_timestamp, end_timestamp)
    #TimeManager.set_live()

    selected_symbols = SYMBOLS[:number_currencies_kept] 

    cache = RedisCache()

    qlm = QueryLimitManager()
    price_manager = PriceManager(selected_symbols, qlm, cache, debug_delay)

    seconds_between_queries = 15
    update_price = UpdatePrices(selected_symbols, price_manager, seconds_between_queries)
    update_price.start()

    buy_manager = BuyManager(price_manager, keep_for_k_minutes)



    d_symbol_diff = {} # its the usdt diff
    d_symbol_relative_diff = {} # its the usdt relative diff
    d_symbol_bucket = {} # its the usdt bucket
    domain_diffs = 0.0

    d_symbol_t_before_retrying = {}

    timestamp = TimeManager.time()
    for symbol in selected_symbols:
      d_symbol_t_before_retrying[symbol] = 0 # timestamp + (60 * 1) # timestamp + dont_touch_same_currency_for_n_minutes ??????   attention secondes minutes

    should_continue = True
    while should_continue:
      loop_message = "entering big loop to check for BUYING, t: {}".format(int(TimeManager.time()))

      # compute diffs, buckets etc..
      d_symbol_last_price = price_manager.get_last_usdt_prices(selected_symbols)
      d_symbol_old_price = price_manager.get_one_hour_ago_usdt_prices(selected_symbols)
      
      d_symbol_diff, d_symbol_relative_diff, d_symbol_bucket, domain_diffs = \
        self.compute_features(selected_symbols, bucket_middle, d_symbol_last_price, d_symbol_old_price)

      log(loop_message + " and domain_diffs: {}".format(domain_diffs))

      for symbol in selected_symbols:
        if not (domain_diffs >= diff_domain_buy_trigger):
          continue

        if not TimeManager.time() >= d_symbol_t_before_retrying[symbol]: # mettre un lock la dessus aussi ou pas ???
          #log("timestamps is too young")
          continue

        bucket = d_symbol_bucket[symbol]
        diff = d_symbol_diff[symbol]
        relative_diff = d_symbol_relative_diff[symbol]
        condition_to_buy = (bucket == 1 and diff <= diff_upper_buy_condition) # LATER relative_diff # RD pk c est statique ca ??? et pas dynamique ??      WARNING:::: diff / price[0] EST CE BIEN COMME CA LAUTRE le jupyter
        if not condition_to_buy:
          #log("no condition to buy: bucket={}, relative_diff={}".format(bucket, relative_diff))
          continue

        d_symbol_t_before_retrying[symbol] = TimeManager.time() + (dont_touch_same_currency_for_n_minutes * 60)
        buy_manager.buy(symbol)

      qlm.sleep_to_limit_query_rate()
      should_continue = TimeManager.add_seconds(31) # 30 would make us have a regular modulo toward the minute
      buy_manager.time_was_updated()


  def compute_features(self, selected_symbols, bucket_middle, d_symbol_last_price, d_symbol_old_price):
    d_symbol_diff = {} # its the usdt diff
    d_symbol_relative_diff = {} # its the usdt relative diff
    d_symbol_bucket = {} # its the usdt bucket
    domain_diffs = 0.0

    for symbol in selected_symbols:
        cur_price = d_symbol_last_price[symbol]
        old_price = d_symbol_old_price[symbol]
        diff = (cur_price - old_price)
        d_symbol_diff[symbol] = diff
        relative_diff = diff / old_price
        d_symbol_relative_diff[symbol] = relative_diff
        bucket = Algo.get_bucket(bucket_middle, relative_diff)
        d_symbol_bucket[symbol] = bucket
        #log("{} - cur_price: {}, old_price: {}, diff / old_price: {},bucket : {} ".format(symbol, cur_price, old_price, (diff / old_price), bucket))
        domain_diffs += bucket
    domain_diffs /= len(selected_symbols)

    return d_symbol_diff, d_symbol_relative_diff, d_symbol_bucket, domain_diffs


  @classmethod
  def get_bucket(cls, bucket_middle, value):
    if value <= -bucket_middle:
      return -1
    elif value >= -bucket_middle and value <= bucket_middle:
      return 0
    elif value >= bucket_middle:
      return 1



if __name__ == "__main__":
  algo = Algo()
  algo.start()





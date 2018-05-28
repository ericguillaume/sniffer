import time
import threading

from utils import log
from bot.time_manager.time_manager import TimeManager


class BuyManager():

  def __init__(self, price_manager, keep_for_k_minutes):
    self.price_manager = price_manager
    self.keep_for_k_minutes = keep_for_k_minutes
    self.buys = set()

  def buy(self, symbol):
    sbm = SymbolBuyManager(self.price_manager, symbol, self.keep_for_k_minutes)
    sbm.buy()

    if TimeManager.is_live():
      return

    self.buys.add(sbm)

  def time_was_updated(self):
    if TimeManager.is_live():
      return

    buys_to_remove = []
    for buy in self.buys:
      should_keep = buy.time_was_updated()
      if not should_keep:
        buys_to_remove.append(buy)

    for buy in buys_to_remove:
      self.buys.remove(buy)



class SymbolBuyManager(threading.Thread):
  def __init__(self, price_manager, symbol, keep_for_k_minutes):
    threading.Thread.__init__(self)
    self.price_manager = price_manager
    self.symbol = symbol
    self.keep_for_k_minutes = keep_for_k_minutes

  def buy(self):
    # buying
    success, buy_price, _ = self.price_manager.get_current_symbol_price(self.symbol) # try twice
    if not success:
      return

    self.buy_price = buy_price
    log("we are going to buy {} at price = {}".format(self.symbol, buy_price))

    if TimeManager.is_live():
      self.start()
    else:
      self.buy_offline_timestamp = TimeManager.time()

  def run(self):
    if not TimeManager.is_live():
      return True

    log("we are going to buy {}".format(self.symbol))
    buy_time = TimeManager.time()

    ## buy here

    time.sleep(self.keep_for_k_minutes * 60)

    ## sell here

    sell_time = time.time()
    success, sell_price, _ = self.price_manager.get_current_symbol_price(self.symbol)  # try twice
    if not success:
      log("couldn't sell {} bought at time {} price {}, sell at time :{}"\
            .format(self.symbol, buy_time, self.buy_price, sell_time))
      return True
    log("sell_price = {}".format(sell_price))

    profit = sell_price - self.buy_price
    relative_profit = profit / self.buy_price
    time_currency_kept = sell_time - buy_time
    log("{} # shortcut_relative_profit".format(relative_profit))
    log("DEBUG time_currency_kept: {}, diff with expected = {}" \
      .format(time_currency_kept, abs(time_currency_kept - self.keep_for_k_minutes * 60)))
    log("SOLD {}: relative_profit = {}  ---  bought at time {} price {}, sell at time: {}, price: {}"\
            .format(self.symbol, relative_profit, buy_time, self.buy_price, sell_time, sell_price))
    return True


  def time_was_updated(self):
    if TimeManager.is_live():
      should_keep = False
      return should_keep

    if (TimeManager.time() < self.buy_offline_timestamp + (self.keep_for_k_minutes * 60)):
      should_keep = True
      return should_keep

    success, sell_price, sell_time = self.price_manager.get_current_symbol_price(self.symbol)
    if not success:
      log("couldn't sell {} bought at time {} price {}, sell at time :{}"\
            .format(self.symbol, self.buy_offline_timestamp, self.buy_price, sell_time))
      return True
    log("sell_price = {}".format(sell_price))

    profit = sell_price - self.buy_price
    relative_profit = profit / self.buy_price
    log("{}, # shortcut_relative_profit".format(relative_profit))
    log("SOLD {}: relative_profit = {}  ---  bought at time {} price {}, sell at time: {}, price: {}"\
            .format(self.symbol, relative_profit, self.buy_offline_timestamp, self.buy_price, sell_time, sell_price))

    should_keep = False
    return should_keep





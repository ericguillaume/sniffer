import time
import threading

from utils import log
from bot.time_manager.time_manager import TimeManager



# thread safe
class QueryLimitManager():

  def __init__(self):
    self.lock = threading.Lock()
    self.queries_since_last_periods = 0

  def queried(self):
    self.lock.acquire()
    self.queries_since_last_periods += 1
    log("queried = {}".format(self.queries_since_last_periods))
    self.lock.release()

  def sleep_to_limit_query_rate(self):
    if TimeManager.is_live():
      time.sleep(30)
    else:
      self.lock.acquire()
      query_nb = self.queries_since_last_periods
      self.queries_since_last_periods = 0
      self.lock.release()

      time_to_sleep = float(query_nb) / 1200.0 * 10
      #log("Going to sleep for {} s".format(time_to_sleep))
      time.sleep(time_to_sleep)
      
      



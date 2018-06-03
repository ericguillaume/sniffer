import unittest
from unittest.mock import MagicMock, patch

from bot.price_cache.redis_cache import RedisCache



class MockedRedis():

  def __init__(self):
    self.d = {}
    self.nb_calls_to_set = 0

  def get(self, key):
    if key in self.d:
      return self.d[key]
    return None

  def set(self, key, value):
    #print("___ set")
    self.nb_calls_to_set += 1
    self.d[key] = value

  def get_nb_calls_to_set(self):
    return self.nb_calls_to_set

  def get_d(self):
    return self.d


    

class TestRedisCache(unittest.TestCase):

  def setUp(self):
    use_redis = True
    mock_redis = True
    self.redis_cache = RedisCache(use_redis, mock_redis)
    self.mocked_redis = MockedRedis()
    self.redis_cache.set_redis(self.mocked_redis)
    self.symbol = "USD"
    self.default_timestamp = -1
    self.timestamp = self.default_timestamp

  def reinitialise_timestamp(self):
    self.timestamp = self.default_timestamp

  def one_minute_passed(self):
    self.timestamp += 60 * 40


  def test_mock_mode(self):
    for i in range(2):
      print("_______________________________________________________________")
      self.reinitialise_timestamp()
      for i in range(25):
        self.one_minute_passed()
        result = self.redis_cache.get(self.symbol, self.timestamp)
        if result == None:
          self.redis_cache.set(self.symbol, self.timestamp, [[self.timestamp + (i * 60), 0] for i in range(500)])
        else:
          result_timestamps = [row[0] for row in result]
          assert(self.timestamp >= result_timestamps[0])
          assert(self.timestamp <= result_timestamps[-1])
      nb_calls = self.mocked_redis.get_nb_calls_to_set()
      if i == 1:
        assert(nb_calls == 0)







if __name__ == '__main__':
  unittest.main()
  print(__name__)



import json
import redis



class RedisCache:

  timestamp_cache_period = 100 * 60
  binance_query_data_duration_in_s = 500 * 60

  def __init__(self, use_redis_cache, mock_redis):
    self.use_redis_cache = use_redis_cache
    self.mock_redis = mock_redis
    self.number_set_since_last_save = 0
    if self.use_redis_cache and not mock_redis:
      self.r = redis.StrictRedis(host='localhost', port=6379, db=0) # gerer toutes lse erreurs si el redis est pas connecte !!!

  # returns None if nothing is found
  def get(self, symbol, timestamp):
    if not self.use_redis_cache:
      return None

    first_modulo_timestamp = self.get_bigger_modulo_timestamp(timestamp - RedisCache.binance_query_data_duration_in_s + RedisCache.timestamp_cache_period)

    result = None
    modulo_timestamp = first_modulo_timestamp
    while modulo_timestamp < timestamp + RedisCache.timestamp_cache_period:
      value = self.r.get(self.get_redis_key(symbol, modulo_timestamp))
      if not value == None:
        result = json.loads(value)
      modulo_timestamp += RedisCache.timestamp_cache_period
    return result

  def set_if_not_already_in(self, symbol, timestamp, array_timestamp_price):
    cached_value = self.get(symbol, timestamp) 
    if cached_value == None:
      self.set(symbol, timestamp, array_timestamp_price)  
      print("Added to Redis")
    else:
      print("Already in redis")

  def set(self, symbol, timestamp, array_timestamp_price):
    if not self.use_redis_cache:
      return

    modulo_timestamp = self.get_bigger_modulo_timestamp(timestamp)
    key = self.get_redis_key(symbol, modulo_timestamp)
    self.r.set(key, json.dumps(array_timestamp_price)) ##### VERIFIER LES TYPES ICI ET EN ENTREE

    self.number_set_since_last_save += 1
    self.save_to_disk_if_need_be()



  # private functions

  def set_redis(self, r):
    self.r = r

  def get_redis(self):
    return self.r

  def get_redis_key(self, symbol, modulo_timestamp): # mettre exception la cle est bien modulo !!!!!
    return "{}_{}".format(symbol, int(modulo_timestamp))

  def get_bigger_modulo_timestamp(self, timestamp):
    if timestamp % RedisCache.timestamp_cache_period == 0:
      return timestamp
    missing_value_to_reach_period = RedisCache.timestamp_cache_period - (timestamp % RedisCache.timestamp_cache_period)
    return timestamp + missing_value_to_reach_period

  def save_to_disk_if_need_be(self):
    if self.number_set_since_last_save >= 50:
      self.r.bgsave() # save() exists too
      self.number_set_since_last_save = 0




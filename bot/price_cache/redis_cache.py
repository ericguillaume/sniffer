import json
import redis



class RedisCache:

  timestamp_cache_period = 100

  def __init__(self):
    self.r = redis.StrictRedis(host='localhost', port=6379, db=0) # gerer toutes lse erreurs si el redis est pas connecte !!!

  # returns None if nothing is found
  def get(self, symbol, timestamp):
    first_modulo_timestamp = self.get_bigger_modulo_timestamp(timestamp - 500)

    modulo_timestamp = first_modulo_timestamp
    while modulo_timestamp < timestamp:
      value = self.r.get(self.get_redis_key(symbol, modulo_timestamp))
      if not value == None:
        return json.loads(value)
      modulo_timestamp += RedisCache.timestamp_cache_period
    return None

  def set(self, symbol, timestamp, array_timestamp_price):
    modulo_timestamp = self.get_bigger_modulo_timestamp(timestamp)
    key = self.get_redis_key(symbol, timestamp, modulo_timestamp)
    r.set(key, json.dumps(array_timestamp_price)) ##### VERIFIER LES TYPES ICI ET EN ENTREE



  # private functions

  def get_redis_key(self, symbol, modulo_timestamp): # mettre exception la cle est bien modulo !!!!!
    return "{}_{}".format(symbol, int(modulo_timestamp))

  def get_bigger_modulo_timestamp(timestamp):
    if timestamp % RedisCache.timestamp_cache_period == 0:
      return timestamp
    missing_value_to_reach_period = RedisCache.timestamp_cache_period - (timestamp % RedisCache.timestamp_cache_period)
    return timestamp + missing_value_to_reach_period




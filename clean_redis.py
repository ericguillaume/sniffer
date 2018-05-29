import redis




if __name__ == "__main__":
  r = redis.StrictRedis(host='localhost', port=6379, db=0)
  for key in r.scan_iter():
    key = key.decode("utf-8")
    if not key.startswith("u-"):
      print(key)
      r.delete(key)



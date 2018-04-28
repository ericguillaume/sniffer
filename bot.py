import requests
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import json
import time
import hmac, hashlib
import sys
from operator import itemgetter

# class ThreadQueryBinance (threading.Thread):
#   def __init__(self, queue, symbol, limit, timestamp):
#     threading.Thread.__init__(self)
#     self.queue = queue
#     self.symbol = symbol
#     self.limit = limit
#     self.timestamp = int(timestamp)
#
#   def run(self):
#     try:
#       url_to_call = "https://api.binance.com/api/v1/klines?symbol={}&interval=1m&limit={}&startTime={}" \
#         .format(self.symbol, self.limit, self.timestamp)
#       html = urlopen(url_to_call)
#       print("going to call {}".format(url_to_call))
#       result_code = html.getcode()
#       if result_code == 200:
#         data = html.read().decode("utf-8")
#         data = json.loads(data)
#         self.queue.put(data)
#       else:
#         print("error result_code = {}".format(result_code))
#     except Exception as e:
#       print(e)
#       pass



# # get live price
# url_to_call = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
# html = urlopen(url_to_call)
# print("going to call {}".format(url_to_call))
# result_code = html.getcode()
# if result_code == 200:
#   data = html.read().decode("utf-8")
#   data = json.loads(data)
#   print(data)




# # get price one minute around
# def get_price(symbol, timestamp):
#   limit = 500
#   url_to_call = "https://api.binance.com/api/v1/klines?symbol={}&interval=1m&limit={}&startTime={}&endTime={}" \
#     .format(symbol, limit, timestamp - 60000, timestamp + 60000)
#   html = urlopen(url_to_call)
#   print("going to call {}".format(url_to_call))
#   result_code = html.getcode()
#   if result_code == 200:
#     data = html.read().decode("utf-8")
#     data = json.loads(data)
#     data = [[x[0], x[1]] for x in data]
#     # [[1524689820000, '9080.99000000'], [1524689880000, '9081.20000000']] # debug todo pourri
#     data = data[0]
#     print(data)
#
# symbol = "BTCUSDT"
# timestamp = (int(time.time()) * 1000) - 3600000
# print(timestamp)
# get_price(symbol, timestamp)







# hmac sha 256

# query_string = "symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559"
# secret_key = "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"

def build_signature(query_string, secret_key):
  signature = hmac.new(secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
  return signature

def build_signature_from_bytes_query_string(query_bytes, secret_key):
  signature = hmac.new(secret_key.encode("utf-8"), query_bytes, hashlib.sha256).hexdigest()
  return signature





def generate_signature(data, secret_api):
  ordered_data = order_params(data)
  query_string = '&'.join(["{}={}".format(d[0], d[1]) for d in ordered_data])
  m = hmac.new(secret_api.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
  return m.hexdigest()


def order_params(data):
  """Convert params to list with signature as last element
  :param data:
  :return:
  """
  has_signature = False
  params = []
  for key, value in data.items():
    if key == 'signature':
      has_signature = True
    else:
      params.append((key, value))
  # sort parameters by key
  params.sort(key=itemgetter(0))
  if has_signature:
    params.append(('signature', data['signature']))
  return params








# signature =  build_signature(query_string, secret_key)
# print(signature)

if not len(sys.argv) == 2:
  print("you need to call python3 bot.py <secret_key>")
secret_key = sys.argv[1]

# test false order
timestamp_sent = int(time.time() * 1000) # ERROR j avais pas le int et * 1000 ici, verifier bienb !!!
# "https://api.binance.com/api/v3/order?symbol=BTCUSDT&timestamp={}&orderId={}".format(timestamp_sent, order_id)


arguments = [("symbol", "BTCUSDT"), ("side", "BUY"), \
             ("type", "LIMIT"), ("quantity", 1.0), ("timestamp", timestamp_sent)]
query_string = urlencode(arguments)
print(query_string)
query_bytes = query_string.encode("utf-8")

#signature = build_signature(query_string, secret_key)
#signature = build_signature_from_bytes_query_string(query_bytes, secret_key)
signature = generate_signature(dict(arguments), secret_key)
arguments.append(("signature", signature))
print(arguments)
full_query_string = urlencode(arguments)

query_data = full_query_string.encode("utf-8")

api_key = "J4ESZQryhdnU17QFUZ9O855u8nMu7FHmtHnjXc7ZekzzWHrbM8GsTiNknEpiyQv5"
url_to_call = "https://api.binance.com/api/v3/order/test".format(api_key)


session = requests.session()
session.headers.update({'Accept': 'application/json',
                        'User-Agent': 'binance/python',
                        'X-MBX-APIKEY': "J4ESZQryhdnU17QFUZ9O855u8nMu7FHmtHnjXc7ZekzzWHrbM8GsTiNknEpiyQv5"})

try:
  print("going to try")
  result_code = session.post(url_to_call, data=query_data)
  print(result_code)
  #html = urlopen(url_to_call, data=query_data)
  if result_code == 200:
    data = html.read().decode("utf-8")
    data = json.loads(data)
    print(data)
except HTTPError as e:
  error_message = e.read()
  print(error_message)



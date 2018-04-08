from urllib.request import urlopen
import time
import threading
from datetime import timedelta
from queue import Queue
import json



#print(19557600 / 24 / 3600)


timestamp = 1522279200000 # 1522309140000 # 1522400040000

t = timestamp / (603600*1000)
timestamp = int(t) * 603600*1000

url_to_call = "https://api.binance.com/api/v1/klines?symbol={}&interval=1m&limit=500&startTime={}" \
	.format("BTCUSDT", timestamp)
html = urlopen(url_to_call)

data = html.read().decode("utf-8")
data = json.loads(data)
print("length of data = {}".format(len(data)))

first_row_timestamp = data[0][0]
print("first row has following timestamp: {}".format(first_row_timestamp))
first_row_dt_in_seconds = int((first_row_timestamp - timestamp)/1000)
print("first row has dt: {}".format(timedelta(seconds=first_row_dt_in_seconds)))

last_row_timestamp = data[499][0]
print("last row has following timestamp: {}".format(last_row_timestamp))
last_row_dt_in_seconds = int((last_row_timestamp - timestamp)/1000)
print("last row has dt: {}".format(timedelta(seconds=last_row_dt_in_seconds)))

time_interval = int((last_row_timestamp - first_row_timestamp) / 1000)
print("time_interval in minutes = {}".format(timedelta(seconds=time_interval)))



from urllib.request import urlopen
import time
import threading
from datetime import timedelta
from queue import Queue
import json


class ThreadQueryBinance (threading.Thread):
  def __init__(self, queue, symbol, limit, timestamp):
    threading.Thread.__init__(self)
    self.queue = queue
    self.symbol = symbol
    self.limit = 2 # limit
    self.timestamp = int(timestamp)

  def run(self):
    try:
      url_to_call = "https://api.binance.com/api/v1/klines?symbol={}&interval=1m&limit={}&startTime={}" \
        .format(self.symbol, self.limit, self.timestamp)
      html = urlopen(url_to_call)
      result_code = html.getcode()
      if result_code == 200:
        data = html.read().decode("utf-8")
        data = json.loads(data)
        queue.put(data)
      else:
        print("error result_code = {}".format(result_code))
    except Exception as e:
      print(e)
      pass


def unstring_float(elem):
  if type(elem) == int:
    return elem
  else:
    return float(elem)


if __name__ == "__main__":
  # url_to_call = "https://api.binance.com/api/v1/klines?symbol=BTCUSDT&interval=1m&limit=500&startTime=1522692560"
  # html = urlopen(url_to_call)
  # data = html.read().decode("utf-8")
  # data = json.loads(data)
  # print(len(data))
  # for idx, row in enumerate(data):
  #   if len(row) == 12:
  #     if idx == 0 or idx == 499:
  #       print(row)
  #     row = [unstring_float(elem) for elem in row]

  # exit()


  symbol = "BTCUSDT"
  nb_threads = 10
  step_in_seconds = 60
  end_timestamp = 1522692560
  start_timestamp = 1522692560 - (30 * 24 * 3600)
  limit = 500

  f = open("binance_{}.csv".format(symbol), 'w+')
  f_start_price = open("binance_{}_only_start_price.csv".format(symbol), 'w+')
  queue = Queue()
  for timestamp_group_start in range(start_timestamp, end_timestamp, nb_threads * step_in_seconds * limit):
    print("timestamp_group_start = {}".format(timestamp_group_start))
    start_small_serie_time = time.time()

    timestamps_to_call = [timestamp_group_start + (thread_idx * step_in_seconds * limit) for thread_idx in range(20)]
    timestamps_to_call = [t for t in timestamps_to_call if t <= end_timestamp]
    threads = [ThreadQueryBinance(queue, symbol, limit, t) for t in timestamps_to_call]
    for thread in threads:
      thread.start()
    for thread in threads:
      thread.join()

    # get data from queue, and sort it
    data = []
    while not queue.empty():
      data.append(queue.get())

    # flatten correct data
    data = [row for datum in data for row in datum  if len(row) == 12]

    # turn string into float
    data = [[unstring_float(elem) for elem in row] for row in data]

    # sort rows
    data = sorted(data, key=lambda x: x[0])

    # write data
    for row in data:
      row = [str(x) for x in row]
      row_to_write = ','.join(row) + "\n"
      row_to_write_start_price = ','.join(row[:2]) + "\n"
      print(row_to_write_start_price)
      f.write(row_to_write)
      f_start_price.write(row_to_write_start_price)
    
    # manage time to avoid querying too much
    duration_small_serie = time.time() - start_small_serie_time
    print("duration_small_serie = {}".format(duration_small_serie))
    if (duration_small_serie < 1.0):
      time.sleep(1.0 - duration_small_serie)

  f.close()
  f_start_price.close()





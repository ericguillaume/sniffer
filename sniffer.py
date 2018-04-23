from urllib.request import urlopen
import time
import threading
from datetime import timedelta
from queue import Queue
import json


from config import SYMBOLS, DATA_FOLDER_NAME


class ThreadQueryBinance (threading.Thread):
  def __init__(self, queue, symbol, limit, timestamp):
    threading.Thread.__init__(self)
    self.queue = queue
    self.symbol = symbol
    self.limit = limit
    self.timestamp = int(timestamp)

  def run(self):
    try:
      url_to_call = "https://api.binance.com/api/v1/klines?symbol={}&interval=1m&limit={}&startTime={}" \
        .format(self.symbol, self.limit, self.timestamp)
      html = urlopen(url_to_call)
      print("going to call {}".format(url_to_call))
      result_code = html.getcode()
      if result_code == 200:
        data = html.read().decode("utf-8")
        data = json.loads(data)
        self.queue.put(data)
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


def sniff(start_timestamp, end_timestamp, symbol):
  nb_threads = 10
  step_in_seconds = 60
  limit = 500

  start_timestamp *= 1000
  end_timestamp *= 1000
  f = open("{}/binance_{}.csv".format(DATA_FOLDER_NAME, symbol), 'w+')
  f_start_price = open("{}/binance_{}_only_start_price.csv".format(DATA_FOLDER_NAME, symbol), 'w+')
  queue = Queue()
  step_size_in_ms = step_in_seconds * limit * 1000
  for timestamp_group_start in range(start_timestamp, end_timestamp, nb_threads * step_size_in_ms):
    print("timestamp_group_start = {}".format(timestamp_group_start))
    start_small_serie_time = time.time()

    timestamps_to_call = [timestamp_group_start + (thread_idx * step_size_in_ms) for thread_idx in range(nb_threads)]
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


if __name__ == "__main__":
  # 1 month data
  # start_timestamp = 1519858800
  # end_timestamp = 1522533600

  # 2 months data
  # start_timestamp = 1518822000
  # end_timestamp = 1523311200

  # starts on 2017
  # start_timestamp = 1483225200
  # end_timestamp = 1523311200

  # 2 months 15 days data
  start_timestamp = 1518822000
  end_timestamp = 1524348000

  for symbol in SYMBOLS:
    sniff(start_timestamp, end_timestamp, symbol)
  





import csv



from config import SYMBOLS
from utils import convert_symbol_into_usdt



def convert_to_usdt(symbol):
  print("going to work here")
  print("data/binance_2_months/binance_{}_only_start_price.csv".format(symbol))

  dict_btc_usdt = {}
  with open("data/binance_2_months/binance_BTCUSDT_only_start_price.csv", 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
      dict_btc_usdt[int(row[0])] = float(row[1])

  usdt_symbol = convert_symbol_into_usdt(symbol)

  print("going to write in data/binance_2_months/binance_{}_only_start_price.csv".format(usdt_symbol))
  f_start_price = open("data/binance_2_months/binance_{}_only_start_price.csv".format(usdt_symbol), 'w+')
  with open("data/binance_2_months/binance_{}_only_start_price.csv".format(symbol), 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
      timestamp = int(row[0])
      currency_in_btc = float(row[1])
      currency_in_usdt = currency_in_btc * dict_btc_usdt[timestamp]
      new_row = [timestamp, currency_in_usdt]

      # write currency_into file
      new_row = [str(x) for x in new_row]
      row_to_write_start_price = ','.join(new_row[:2]) + "\n"
      print(row_to_write_start_price)
      f_start_price.write(row_to_write_start_price)


if __name__ == "__main__":
  for symbol in SYMBOLS:
    if symbol.endswith("BTC"):
      convert_to_usdt(symbol)



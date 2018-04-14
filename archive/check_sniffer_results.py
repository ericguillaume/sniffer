import csv
from datetime import timedelta


spamReader = csv.reader(open('data/binance_2_months/binance_BTCUSDT_only_start_price.csv', newline=''), delimiter=',', quotechar='|')

expected_first_row_timestamp = 1519858800000
expected_last_row_timestamp = 1522533600000

first_row_timestamp = 0.0
last_row_timestamp = 0.0
is_first_row = True
previous_row_timestamp = 0.0
nb_rows = 0
for row in spamReader:
	nb_rows += 1
	if is_first_row:
		previous_row_timestamp = int(row[0])
		first_row_timestamp = previous_row_timestamp
		is_first_row = False
	else:
		new_timestamp = int(row[0])
		dt_in_ms = new_timestamp - previous_row_timestamp
		if dt_in_ms != (60 * 1000):
			print("\nIncorrect dt_in_ms !!")
			print("new timestamp = {}".format(new_timestamp))
			print("previous_row_timestamp = {}".format(previous_row_timestamp))
			print("dt_in_ms = {}\n".format(dt_in_ms))
		previous_row_timestamp = int(row[0])
		last_row_timestamp = previous_row_timestamp

print("nb_rows = {}".format(nb_rows))
expected_number_rows = 60 * 24 * 31
print("we were expecting {}".format(expected_number_rows))

if expected_first_row_timestamp != first_row_timestamp:
	print("first row timestamp wrong {} instead of {}"\
		.format(first_row_timestamp, expected_first_row_timestamp))

if expected_last_row_timestamp != last_row_timestamp:
	error = int((last_row_timestamp - expected_last_row_timestamp) / 1000)
	print("last row timestamp wrong {} instead of {}, error of {}" \
		.format(last_row_timestamp, expected_last_row_timestamp, \
			timedelta(seconds = error)))
		


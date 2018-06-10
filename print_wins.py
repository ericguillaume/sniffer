import csv
import matplotlib.pyplot as plt
import numpy as np



wins = []
with open('log/new_algo_better_performance_result.txt', newline='') as csvfile:
	spamreader = csv.reader(csvfile)
	wins = [float(row[0]) for row in spamreader]


wins = np.array(wins, dtype='float32')

print(len(wins))


def display_histogram_wins(wins):
	plt.title('Histogram of wins')
	plt.xlabel('Value')
	plt.ylabel('Number of wins')
	plt.hist(wins, bins=20, range=(-0.01, 0.01))
	plt.show()


print(np.mean(wins))


print(np.sum(wins))
display_histogram_wins(wins)




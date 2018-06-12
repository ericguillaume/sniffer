import pandas as pd



class MetricsAggregator:

	def __init__(self, columns):
		self.data = []
		self.columns = columns

	def add(self, row):
		self.data.append(row)

	def get_df(self):
		self.index = [i for i in range(len(self.data))]
		return pd.DataFrame(data=self.data, columns=self.columns, index=self.index)



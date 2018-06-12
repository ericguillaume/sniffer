import pandas as pd 
import matplotlib.pyplot as plt



symbol = "BTCUSDT"
df_offline = pd.read_csv("log/metrics_aggregator/offline_{}".format(symbol), index_col=0)
print(df_offline)
df_evaluation = pd.read_csv("log/metrics_aggregator/evaluation_{}".format(symbol), index_col=0)
print(df_evaluation)




x_off = df_offline["timestamp"].values
y_off = df_offline[symbol].values
x_eva = df_evaluation["timestamp"].values
y_eva = df_evaluation[symbol].values

plt.plot(x_off, y_off, label="offline")
plt.plot(x_eva, y_eva, label="evaluation")
plt.legend(bbox_to_anchor=(1.05, 1), loc=0, borderaxespad=0.)
plt.show()



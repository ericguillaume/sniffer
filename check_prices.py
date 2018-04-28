




btc_price = 9038.61000000
old_btc_price = 8979.60000000

eth_price = 0.07197900 * btc_price
old_eth_price = 0.07206900 * old_btc_price



btc_diff = btc_price - old_btc_price
eth_diff = eth_price - old_eth_price



btc_relative_diff = btc_diff / btc_price
eth_relative_diff = eth_diff / eth_price



print("btc_relative_diff: {}".format(btc_relative_diff))
print("eth_relative_diff: {}".format(eth_relative_diff))





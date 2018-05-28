

from utils import convert_symbol_into_usdt


SYMBOLS = ["BTCUSDT", "ETHBTC", "XRPBTC", "BCCBTC", "LTCBTC", "EOSBTC", "ADABTC", "XLMBTC", "NEOBTC", "IOTABTC", \
             "XMRBTC", "DASHBTC", 
             #"XEMBTC",   seems to have problems getting data, see https://api.binance.com/api/v1/klines?symbol=XEMBTC&interval=1m&limit=500&startTime=1518821940000&endTime=1518822060000
             "TRXBTC", "VENBTC", "ETCBTC", "BNBBTC", "QTUMBTC", "OMGBTC", "XVGBTC", \
             "LSKBTC", "ONTBTC", "ICXBTC", "ZECBTC", "NANOBTC", "BTGBTC", "STEEMBTC", "WANBTC", "PPTBTC", "BTSBTC", \
             "DGDBTC", "STRATBTC", "WAVESBTC", "ZILBTC"]

USDT_SYMBOL_EXCHANGEABLE_WITH_USDT = [convert_symbol_into_usdt(x) for x in ["BTCUSDT", "ETHBTC", "BCCBTC", "LTCBTC", "ADABTC", "NEOBTC", "BNBBTC", "QTUMBTC"]]

USDT_SYMBOLS = [convert_symbol_into_usdt(x) for x in SYMBOLS]

DATA_FOLDER_NAME_READ = "data/binance_4_months_v2_finished"
DATA_FOLDER_NAME_WRITE = "data/binance_4_months_v2" # "data/binance_4_months"




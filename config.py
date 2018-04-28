

from utils import convert_symbol_into_usdt


SYMBOLS = ["BTCUSDT", "ETHBTC", "XRPBTC", "BCCBTC", "LTCBTC", "EOSBTC", "ADABTC", "XLMBTC", "NEOBTC", "IOTABTC", \
             "XMRBTC", "DASHBTC", "XEMBTC", "TRXBTC", "VENBTC", "ETCBTC", "BNBBTC", "QTUMBTC", "OMGBTC", "XVGBTC", \
             "LSKBTC", "ONTBTC", "ICXBTC", "ZECBTC", "NANOBTC", "BTGBTC", "STEEMBTC", "WANBTC", "PPTBTC", "BTSBTC", \
             "DGDBTC", "STRATBTC", "WAVESBTC", "ZILBTC"]

USDT_SYMBOL_EXCHANGEABLE_WITH_USDT = [convert_symbol_into_usdt(x) for x in ["BTCUSDT", "ETHBTC", "BCCBTC", "LTCBTC", "ADABTC", "NEOBTC", "BNBBTC", "QTUMBTC"]]

USDT_SYMBOLS = [convert_symbol_into_usdt(x) for x in SYMBOLS]

DATA_FOLDER_NAME_READ = "data/binance_2_months_15_days_finished"
DATA_FOLDER_NAME_WRITE = "data/binance_2_months_15_days" # "data/binance_4_months"


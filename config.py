

from utils import convert_symbol_into_usdt


SYMBOLS = ["BTCUSDT", "ETHBTC", "XRPBTC", "BCCBTC", "LTCBTC", "EOSBTC", "ADABTC", "XLMBTC", "NEOBTC", "IOTABTC", \
             "XMRBTC", "DASHBTC", "XEMBTC", "TRXBTC", "VENBTC", "ETCBTC", "BNBBTC", "QTUMBTC", "OMGBTC", "XVGBTC", \
             "LSKBTC", "ONTBTC", "ICXBTC", "ZECBTC", "NANOBTC", "BTGBTC", "STEEMBTC", "WANBTC", "PPTBTC", "BTSBTC", \
             "DGDBTC", "STRATBTC", "WAVESBTC", "ZILBTC"]

USDT_SYMBOLS = [convert_symbol_into_usdt(x) for x in SYMBOLS]


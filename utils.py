import sys



def is_symbol_in_usdt(symbol):
  return not symbol.endswith("BTC")

def convert_symbol_into_usdt(symbol):
  if symbol.endswith("BTC"):
    return symbol.replace("BTC", "USDT")
  else:
    return symbol

# not refactored yet because it would need comparison and testing
# def turn_row_with_price_only_into_csv(row):
#   row = [str(x) for x in row]
#   return ','.join(row[:2]) + "\n"


CATEGORY_20_PALETTE = ['#393b79', '#5254a3', '#6b6ecf', '#9c9ede', '#637939', '#8ca252', '#b5cf6b', '#cedb9c', '#8c6d31', '#bd9e39', '#e7ba52', '#e7cb94', '#843c39', '#ad494a', '#d6616b', '#e7969c', '#7b4173', '#a55194', '#ce6dbd', '#de9ed6']
def get_palette_color(index):
    index = index % len(CATEGORY_20_PALETTE)
    return CATEGORY_20_PALETTE[index]

CATEGORY_3_DASH_PATTERNS = ["solid", "dashed"] # "dotted"
def get_dash_pattern(index):
    index = index % len(CATEGORY_3_DASH_PATTERNS)
    return CATEGORY_3_DASH_PATTERNS[index]


def log(message):
	print(message)
	sys.stdout.flush()


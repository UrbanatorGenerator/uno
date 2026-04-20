import yfinance as yf
import json

symbols = {
    '^GSPC':   'spx',
    '^FTSE':   'ftse',
    '^GDAXI':  'dax',
    '^OMXSPI': 'omxspi',
    '^OMX':    'omxs30',
    '^N225':   'nikkei',
}

data = {}

for sym, key in symbols.items():
    try:
        fi = yf.Ticker(sym).fast_info
        price = fi.last_price
        prev  = fi.previous_close
        if price and prev:
            chg = (price - prev) / prev * 100
            data[key] = {
                'price': f'{price:,.2f}',
                'change': round(chg, 2)
            }
    except Exception as e:
        print(f"Skip {sym}: {e}")

fx_pairs = {
    'EURUSD=X':  ('eurusd', 4),
    'GBPUSD=X':  ('gbpusd', 4),
    'EURCHF=X':  ('eurchf', 4),
    'EURJPY=X':  ('eurjpy', 2),
    'USDCHF=X':  ('usdchf', 4),
    'USDJPY=X':  ('usdjpy', 2),
    'USDSEK=X':  ('usdsek', 4),
    'USDDKK=X':  ('usddkk', 4),
    'USDNOK=X':  ('usdnok', 4),
    'SEKCOP=X':  ('sekcop', 0),
}

for sym, (key, dec) in fx_pairs.items():
    try:
        fi = yf.Ticker(sym).fast_info
        price = fi.last_price
        if price:
            data[key] = {'price': f"{round(price, dec)}"}
    except Exception as e:
        print(f"Skip FX {sym}: {e}")

with open('market-data.json', 'w') as f:
    json.dump(data, f)

print("Done:", list(data.keys()))

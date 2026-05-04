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

crypto_pairs = {
    'BCH-USD': ('bchusd', 2),
}

for sym, (key, dec) in crypto_pairs.items():
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
        print(f"Skip crypto {sym}: {e}")

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
    'USDCOP=X':  ('usdcop', 2),
}

raw_fx = {}

for sym, (key, dec) in fx_pairs.items():
    try:
        fi = yf.Ticker(sym).fast_info
        price = fi.last_price
        if price:
            raw_fx[key] = price
            data[key] = {'price': f"{round(price, dec)}"}
    except Exception as e:
        print(f"Skip FX {sym}: {e}")

# SEK/COP cross rate: USDCOP / USDSEK
try:
    sekcop = raw_fx['usdcop'] / raw_fx['usdsek']
    data['sekcop'] = {'price': f"{round(sekcop, 0):.0f}"}
except Exception as e:
    print(f"Skip SEK/COP cross: {e}")

with open('market-data.json', 'w') as f:
    json.dump(data, f)

print("Done:", list(data.keys()))

import yfinance as yf
import requests
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

try:
    r = requests.get('https://open.er-api.com/v6/latest/EUR', timeout=10)
    R = r.json().get('rates', {})
    def fx(v, dec): return round(v, dec) if v else None
    if R.get('USD'): data['eurusd'] = {'price': f"{fx(R['USD'],4)}"}
    if R.get('GBP') and R.get('USD'): data['gbpusd'] = {'price': f"{fx(R['USD']/R['GBP'],4)}"}
    if R.get('CHF'): data['eurchf'] = {'price': f"{fx(R['CHF'],4)}"}
    if R.get('JPY'): data['eurjpy'] = {'price': f"{fx(R['JPY'],2)}"}
    if R.get('USD') and R.get('CHF'): data['usdchf'] = {'price': f"{fx(R['CHF']/R['USD'],4)}"}
    if R.get('USD') and R.get('JPY'): data['usdjpy'] = {'price': f"{fx(R['JPY']/R['USD'],2)}"}
    if R.get('USD') and R.get('SEK'): data['usdsek'] = {'price': f"{fx(R['SEK']/R['USD'],4)}"}
    if R.get('USD') and R.get('DKK'): data['usddkk'] = {'price': f"{fx(R['DKK']/R['USD'],4)}"}
    if R.get('USD') and R.get('NOK'): data['usdnok'] = {'price': f"{fx(R['NOK']/R['USD'],4)}"}
except Exception as e:
    print(f"FX fetch error: {e}")

with open('market-data.json', 'w') as f:
    json.dump(data, f)

print("Done:", list(data.keys()))

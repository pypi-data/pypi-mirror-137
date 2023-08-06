# batchquotes

yfQuotes is a simple python module for scraping/streaming quotes from Yahoo! Finance. Scraping uses threading/asyncio to increase speed of batch queries. (Valid for Yahoo!Finance layout as of 30th Nov 2021), whilst streaming opens a websocket to receive live prices from yahoo!Finance

# Requirements
- Python 3.7+
- Beautiful Soup 4==4.9.3
- aiohttp==3.8.1
- websockets-client==1.2.3

# Installation
pip install yfQuotes

# Usage
## Batch single queries

```
from yfQuotes import get_quotes_threading, get_quotes_asyncio

symbols = ['AAPL', 'AMZN', 'MSFT', 'TSLA', 
'GOOG', 'V', 'ROKU', 'PYPL', 'BIDU',
'STNE', 'SEV', 'SAVA', 'NVDA', 'ELEK',
'IQ', 'ARVL', 'BABA', 'BRZE', 'MRNA',
'TJX', 'UWMC', 'DLO', 'MA', 'JOET']

quotes = get_quotes_asyncio(symbols)

print(quotes)
[{'current_price': 154.08, 'increase_dollars': 3.08, 'increase_precent': 2.04},
...]
```

## Comparison
```
start = time.time()
for symbol in symbols:
    _ = requests.get(f"https://finance.yahoo.com/quote/{symbol}/history",
    headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36"
        })
end = time.time()
print(f'Synchronous: {end-start}s')

start = time.time()
quotes = get_quotes_threading(symbols)
end = time.time()
print(f'Multithread: {end-start}s')

start = time.time()
quotes = get_quotes_asyncio(symbols)
end = time.time()
print(f'Asyncio: {end-start}s')

Synchronous: 25.616918802261353s
Multithread: 6.701111793518066s
Asyncio: 4.443589210510254s

```

## Stream quotes 
```
from yfQuotes import Streamer

streamer = Streamer()
streamer.connect()
#expects yahoo!Finance symbols 
streamer.add(['AAPL', 'AMZN', 'btc-usd'])

streamer.disconnect()

#If not during market hours for any of the added symbols streamer will not receive updates!
```




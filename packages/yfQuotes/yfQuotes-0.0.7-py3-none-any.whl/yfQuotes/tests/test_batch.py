import pytest 
from yfQuotes import get_quotes_asyncio, get_quotes_threading
import time

@pytest.fixture
def symbols():
    return [
        'GME', 'LRC-USD',
        'PLTR', 'NVDA', 'ROO.L', 'MMED.NE', 'ETH-USD',
        'HBAR-USD', 'DOGE-USD', 'BTC-USD', 'CTXR', 'F', 'AMC',
        'BB', 'CTXR', 'MRNA', 'BNTX', 'AMC', 'HBAR-USD',
        'OTLY', '^VIX', 'SPY'
    ]

def test_multithread(symbols):
    try:
        start = time.time()
        quotes = get_quotes_threading(symbols)
        end = time.time()
        print(quotes[0])
        print(f'threading: {end - start}')
        return True 
    except Exception as e:
        print(e)
        return False 

def test_asyncio(symbols):
    try:
        start = time.time()
        quotes = get_quotes_asyncio(symbols)
        end = time.time()
        print(quotes[0])
        print(f'asyncio: {end - start}')
        return True 
    except Exception as e:
        print(e)
        return False 
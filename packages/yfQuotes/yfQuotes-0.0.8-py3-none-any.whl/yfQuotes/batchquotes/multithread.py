import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import batchquotes

thread_local = threading.local()

def get_session():
    #creates a session object for a thread if not initialized else using existing one
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session

def get_stock_quote(symbol):
    session = get_session()
    user_agent = batchquotes.USER_AGENT

    try:
        r = session.get(f"https://finance.yahoo.com/quote/{symbol}/history",
        headers={
                "User-Agent": user_agent
            })
    except:
        raise RuntimeError('Connection Error')

    if r.status_code == 302:
        raise RuntimeError(f'Invalid Symbol: {symbol}')
    #process request object 
    try:
        return batchquotes.extract_quote(r.text, symbol=symbol)
    except:
        raise RuntimeError(f'Invalid Symbol: {symbol}')

def get_quotes_threading(symbols, max_workers=None):
    assert type(symbols) == list
    #requests is not thread safe, so need to create a requests.session for each thread separately
    #thread_local looks like a global object in this namespace, but is specific to each individual thread

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        #map returns results in same order as list 
        quotes = executor.map(get_stock_quote, symbols)
    return list(quotes)

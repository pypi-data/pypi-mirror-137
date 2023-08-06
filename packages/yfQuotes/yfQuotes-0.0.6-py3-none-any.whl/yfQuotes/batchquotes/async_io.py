import asyncio 
import aiohttp
import batchquotes

#asyncio
async def fetch(session, symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}/history"
    async with session.get(url, ssl=False) as response:
        if response.status != 200:
            response.raise_for_status()
        r = await response.text()
        return batchquotes.extract_quote(r, symbol=symbol)

async def coro(symbols):
    assert type(symbols) == list
    user_agent = batchquotes.USER_AGENT

    headers = {'User-Agent': user_agent}
    #define async func to get response object 
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [fetch(session, symbol) for symbol in symbols]
        quotes = await asyncio.gather(*tasks)
    
    return quotes

def get_quotes_asyncio(symbols):
    return asyncio.run(coro(symbols))


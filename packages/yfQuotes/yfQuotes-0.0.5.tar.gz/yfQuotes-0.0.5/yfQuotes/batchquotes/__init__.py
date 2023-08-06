"""
batchQuotes:

This module is inspired by the stockquotes package and scrapes yahoo finance
for live stock/crypto quotes. Amendments to the original package include only 
acquiring the current price. Users can choose between using concurrent.futures'
multithreading or asyncio to quickly retrieve a batch of quotes

"""
from bs4 import BeautifulSoup as bs 
import requests
import os
from .multithread import get_quotes_threading 
from .async_io import get_quotes_asyncio
import re 

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'

def extract_quote(r_text, symbol=None):

    def clean(text):
        #remove non-alphanum from beginning
        blacklist = '()%+'
        cleaned = text.strip(blacklist)
        cleaned = cleaned.replace(',', '')
        return cleaned

    soup = bs(r_text, features='lxml')

    if symbol is None:
        #if you don't pass symbol argument it'll try and find one
        meta = soup.find('meta', attrs={'content': re.compile('.')})
        symbol = meta['content'].split(',')[0]
    #get current price 
    data_streams = soup.find_all('fin-streamer', attrs={'data-symbol': symbol})
    ignore = ['marketState']
    data = dict(map(str, [s['data-field'], s.string]) for s in data_streams if s['data-field'] not in ignore)
    data = {key: clean(val) for key, val in data.items()}
    
    #format out_dict with more standard names
    new_keys = ['current_price', 'increase_dollars', 'increase_percent', 
    'regular_market_time', 'post_market_time', 'current_price_PM',
    'increase_dollars_PM', 'increase_percent_PM']

    new_dict = {}

    for new, old in zip(new_keys, data):
        new_dict[new] = data[old]

    return new_dict


#optional function to update user_agents 
# def get_latest_user_agents(os='macos', file_name=USER_AGENTS_PATH):
#     assert os in ['macos', 'chrome-os', 'ios', 'windows', 'android']
#     session = requests.session()
#     r = session.get(f'https://www.whatismybrowser.com/guides/the-latest-user-agent/{os}?utm_source=whatismybrowsercom&utm_medium=internal&utm_campaign=latest-user-agent-index')
#     soup = bs(r.text, features='lxml')
#     spans = soup.find_all('span', {"class": "code"})
#     agent_strings = [span.string for span in spans]
#     if file_name is not None:
#         with open(file_name, 'w') as f:
#             for string in agent_strings:
#                 f.write(string + '\n')
#     else:
#         return agent_strings









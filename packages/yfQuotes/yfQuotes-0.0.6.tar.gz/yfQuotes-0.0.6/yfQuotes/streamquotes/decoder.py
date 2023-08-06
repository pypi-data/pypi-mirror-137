"""
module to decode protobuf messages from yahoo!finance

references these files: 
https://finance.yahoo.com/__finStreamer-worker.js --> shows base64 encoding
https://finance.yahoo.com/__finStreamer-proto.js --> shows .proto structure

for the decoding process of the streaming data 
"""

import base64
from .yfinance_pb2 import PricingData

sample_msg = 'CgdCVEMtVVNEFRKGR0cYoN6fvbJfIgNVU0QqA0NDQzApOAFFc/7EQEiAwKnKmQJVsSZIR12iFEVHZdAgOUVqC0JpdGNvaW4gVVNEsAGAwKnKmQLYAQTgAYDAqcqZAugBgMCpypkC8gEDQlRD+gENQ29pbk1hcmtldENhcIECAAAAwLkEckGJAgAAfF84FmxC'

class Decoder:
    #fields taken from fields outlines in .proto file 
    __fields__ = (
    'id', 'price', 'time', 'currency', 'exchange', 'quoteType',
    'marketHours', 'changePercent', 'dayVolume', 'dayLow', 'dayHigh', 'change',
    'shortName', 'lastSize', 'priceHint', 'vol_24hr', 'volAllCurrencies',
    'fromcurrency', 'lastMarket', 'circulatingSupply', 'marketcap')

    def __init__(self, msg):
        self.msg = msg
        self.msg_bytes = None
        #decode msg 
        self.decode()
        #parse msg 
        self.proto_obj = PricingData()
        try:
            self.proto_obj.ParseFromString(self.msg_bytes)
        except Exception as e:
            print(f'Parsing Error: {e}')
        
        #convert pricing data into a dict for access
        self.set_props()
        self.to_dict()

    def decode(self):
        self.msg_bytes = base64.b64decode(self.msg)

    def set_props(self):
        for field in Decoder.__fields__:
            setattr(self, field, getattr(self.proto_obj, field))

    def to_dict(self):
        #sets up a dictionary for later parsing of the inbound message
        self.data = {}
        for field in Decoder.__fields__:
            self.data.update({field: getattr(self.proto_obj, field)})

    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return f'Decoder({self.msg})'

    
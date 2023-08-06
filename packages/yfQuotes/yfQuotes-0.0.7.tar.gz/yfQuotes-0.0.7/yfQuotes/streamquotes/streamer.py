"""
Creating a websocket to connect to yfinance to retrieve live streaming quotes
- this is probably possible b/c the native website uses elements called fin-streamer
to constantly update prices. So in theory we can connect with a custom socket and query custom
prices???
"""
import gc
from typing import Iterable, Callable
import logging
import websocket
import threading
import ssl
import json 
from datetime import datetime
import time
from .decoder import Decoder

websocket.enableTrace(False)

#next step - see how to change subscribe dynamically? - basically need to find 
#a way to send a new msg during connection - don't use connection as context manager 
#and manually handle closing of connection

#use asyncio create_task to run async functions in background 
class Streamer:
    _socket_uri = 'wss://streamer.finance.yahoo.com/'
    _sslopt = {"cert_reqs": ssl.CERT_NONE}

    def __init__(self, subscribe: Iterable=None, on_message: Callable=None, on_error: Callable=None, 
                on_close: Callable=None, on_open: Callable=None, header: dict=None,
                run_in_background: bool=True):
        """
        Constructor for Streamer object
        Args:
        subscribe = list of yfinance symbols to subscribe to after connecting 
        on_connect: callback method for after connection initiation
        on_error: callback method for when error occurs
        on_close: callback method for connection close
        header: a dictionary for additional headers to be included 
        run_in_background: boolean to determine if non-blocking thread is created for process
        """
        self._logger = None 
        self._init_logger()
        self.subscribed = set(subscribe) if subscribe is not None else set()
        self.on_open = on_open if on_open else self.default_on_open
        self.on_error = on_error if on_error else self.default_on_error
        self.on_close = on_close if on_close else self.default_on_close
        self.header = header
        self.on_message = on_message if on_message else self.default_on_message
        self.run_in_background = run_in_background
        self.running = False 
        self._thread = None
        #initiate socket
        self.init_socket()


    def init_socket(self):
        self.socket = websocket.WebSocketApp(Streamer._socket_uri, on_message=self.on_message,
                                            on_error=self.on_error, on_close=self.on_close,
                                            on_open=self.on_open)
        self._logger.debug('WebSocketApp Initiated')
    
    def connect(self, wait=2):
        #by default doesnt use ssl certification
        if self.socket.keep_running:
            return

        self.running = True
        if self.run_in_background:
            #use _thread_run_forever here, so reconnection is automatic
            self._thread = threading.Thread(target=self._thread_run_forever)
            self._thread.daemon = True
            self._thread.start()
        else:
            self.socket.run_forever(sslopt=Streamer._sslopt)

        self._logger.debug('Connection initiated.') 
        #takes a second before socket is ready, so put a small wait time here
        time.sleep(wait)
        #initiate subscriptions
        if len(self.subscribed) and self.socket.keep_running:
            self.add(self.subscribed)
            self._logger.debug(f'initiated subscriptions: {self.subscribed}')

    def _thread_run_forever(self, retry_in: int=5):
        #if connection is closed, don't think currently run_forever reconnects itself automatically,
        #so doing this in a while loop in the thread to reconnect if an error occurs 
        while self.running:
            try:
                self.socket.run_forever(sslopt=Streamer._sslopt)
                self._logger.debug('Connection initiated.') 

            except KeyboardInterrupt:
                self.running = False 
                self._logger.debug('Keyboard Interrupt - Exiting loop')
            except Exception as e:
                gc.collect()
                self._logger.exception(f'Socket has disconnected: {e}')
            self._logger.debug(f'Reconnecting websocket in {retry_in} sec')
            time.sleep(retry_in)

    def disconnect(self):
        self.running = False 
        self.socket.close()
        if self.run_in_background:
            self._thread.join()
        self._logger.debug('Connection Closed.')


    def add(self, symbols):
        if symbols is None or len(symbols) == 0:
            return 

        #check overlaps with current subscriptions   
        new = set(symbols) - self.subscribed       
        if len(new) == 0:
            return 

        subscribe = {'subscribe': list(new)}
        msg = json.dumps(subscribe)
        try:
            self.socket.send(msg)
        except:
            self._logger.exception(f'Failed to subscribe to {new}')
        else:
            self.subscribed = self.subscribed | new
            self._logger.debug(f'subscribed to {new}')


    def remove(self, symbols):
        if symbols is None or len(symbols) == 0:
            return 
        
        exists = set(symbols) & self.subscribed
        if len(exists) == 0:
            return 
        
        unsubscribe = {'unsubscribe': list(exists)}
        msg = json.dumps(unsubscribe)
        try:
            self.socket.send(msg)
        except:
            self._logger.exception(f'Failed to send {msg}')
        else:
            self.subscribed = self.subscribed - exists 
            self._logger.debug(f'unsubscribed: {exists}')


    def _init_logger(self, stream=True, level=logging.DEBUG):
        self._logger = logging.getLogger('Streamer')
        formatter = logging.Formatter('%(asctime)s ; %(levelname)s ; %(module)s ; %(funcName)s ; %(message)s')
        file_handler = logging.FileHandler('stream.log', 'w')
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
        self._logger.setLevel(level)
        if stream:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self._logger.addHandler(stream_handler)

    @staticmethod
    def default_on_message(app, message):
        quote = Decoder(message)
        now = datetime.now().strftime('%H:%M:%S')
        print(f'{now} - {quote.id}: {quote.price}')
        return 

    @staticmethod
    def default_on_error(app, error):
        print(error)
        return

    @staticmethod
    def default_on_close(app, close_status_code, close_msg):
        print(f'close_status_code: {close_status_code}')
        print(f'close message: {close_msg}')
        return

    @staticmethod
    def default_on_open(app):
        pass

if __name__ == '__main__':
    s = Streamer(subscribe=['BTC-USD', 'LRC-USD'], run_in_background=True)
    s.connect()
    s.add(['0388.HK'])
    s.remove(['LRC-USD'])




    



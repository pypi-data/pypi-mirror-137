import pytest 
from yfQuotes import Streamer
import time

@pytest.fixture
def symbols1():
    return [
        'GME', 'LRC-USD',
        'PLTR', 'NVDA', 'ROO.L', 'MMED.NE', 'ETH-USD',
    ]


def test_streamer(symbols1):
    s = Streamer()
    s.connect()
    assert s.socket.keep_running == True 

    s.add(symbols1)
    assert s.subscribed == set(symbols1)

    s.remove(symbols1)
    assert s.subscribed == set()

    s.disconnect()

    assert s.socket.keep_running == False
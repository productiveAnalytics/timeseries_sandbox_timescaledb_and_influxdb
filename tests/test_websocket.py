#! /usr/bin/env python3
# websocket_test.py

from twelvedata import TDClient


# Refer: https://twelvedata.com/account/api-keys
TWELVEDATA_API_KEY:str = "REPLACE_ME"


def on_event(event):
    print(event) # prints out the data record (dictionary)


td = TDClient(apikey=TWELVEDATA_API_KEY)
ws = td.websocket(symbols=["BTC/USD", "ETH/USD", "AAPL", "GOOG", "NVDA"], on_event=on_event)
ws.connect()
ws.keep_alive()
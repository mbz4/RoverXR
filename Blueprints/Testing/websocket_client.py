#!/usr/bin/env python3
from websockets.sync.client import connect
import asyncio
'''
WS CLIENT ON LAPTOP
'''

def hello():
    with connect("ws://192.168.199.228:3333") as websocket:
        #websocket.send("Hello world!")
        message = websocket.recv()
        print(f"Received: {message}")

hello()
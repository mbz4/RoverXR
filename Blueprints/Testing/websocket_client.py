#!/usr/bin/env python3
from websockets.sync.client import connect
import asyncio
'''
WS CLIENT ON LAPTOP
'''

def hello():
    with connect("ws://192.168.199.228:3333") as websocket:
        message = websocket.recv().decode('utf-8')
        print(message)

hello()
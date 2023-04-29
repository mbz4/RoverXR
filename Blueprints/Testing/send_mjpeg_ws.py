#!/usr/bin/env python3
import asyncio
import websockets
import sys
'''
    Intended to be run from terminal as: 
    raspivid -vf -hf -fps 30 -t 0 -l -w 1920 -h 1080 --codec MJPEG -o - | python3 send_mjpeg_ws.py
'''
async def handle_stream(websocket):
    try:
        marker = b'\xff\xd8'
        trailer = b'\xff\xd9'
        while True:
            data = sys.stdin.buffer.readline()
            if not data:
                break
            if data.startswith(marker):
                print("Got new JPEG")
                frame = bytearray()
                while True:
                    data = sys.stdin.buffer.readline()
                    if data.startswith(trailer):
                        frame.extend(data)
                        await websocket.send(frame)
                        print("Sent frame to client")
                        break
                    frame.extend(data)
    except websockets.exceptions.ConnectionClosedError:
        pass

async def main():
    print("MJPEG WS Server started...")
    async with websockets.serve(handle_stream, '0.0.0.0', 3333): # start server on host, port
        await asyncio.Future() # run forever

if __name__ == '__main__':
    asyncio.run(main())
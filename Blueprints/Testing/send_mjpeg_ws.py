#!/usr/bin/env python3
import asyncio
import websockets
import sys
'''
    Intended to be run from terminal as: raspivid -vf -hf -fps 30 -t 0 -l -w 1920 -h 1080 --codec MJPEG -o - | python3 send_mjpeg_ws.py
'''
async def send_mjpeg_stream(websocket):
    try:
        boundary = b'\xff\xd8\r\n'
        header = b'Content-Type: image/jpeg\r\n\r\n'
        while True:
            data = sys.stdin.buffer.readline() # Read from stdin
            print(data)
            if not data:
                break
            if data.startswith(boundary):
                data = sys.stdin.buffer.readline() # Read the header and JPEG data
                if not data.startswith(header):
                    break
                jpeg_data = bytearray()
                while True:
                    data = sys.stdin.buffer.readline()
                    if data.startswith(boundary):
                        await websocket.send(jpeg_data) # Send the JPEG data over the WebSocket connection
                        break
                    jpeg_data.extend(data)
    except websockets.exceptions.ConnectionClosedError:
        pass

async def main():
    uri = f'ws://localhost:3333'
    async with websockets.connect(uri) as websocket:
        await send_mjpeg_stream(websocket)

if __name__ == '__main__':
    asyncio.run(main())
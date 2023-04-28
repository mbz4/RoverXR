#!/usr/bin/env python3
import asyncio
import websockets
import sys

async def send_mjpeg_stream(websocket):
    try:
        boundary = b'--myboundary\r\n'
        header = b'Content-Type: image/jpeg\r\n\r\n'
        while True:
            # Read from stdin until we find a boundary marker
            data = sys.stdin.buffer.readline()
            if not data:
                break
            if data.startswith(boundary):
                # Read the header and JPEG data
                data = sys.stdin.buffer.readline()
                if not data.startswith(header):
                    break
                jpeg_data = bytearray()
                while True:
                    data = sys.stdin.buffer.readline()
                    if data.startswith(boundary):
                        # Send the JPEG data over the WebSocket connection
                        await websocket.send(jpeg_data)
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
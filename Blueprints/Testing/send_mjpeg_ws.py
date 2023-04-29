#!/usr/bin/env python3
import asyncio
import websockets
import sys
# import io
'''
    Intended to be run from terminal as: 
    raspivid -vf -hf -fps 30 -t 0 -l -w 1920 -h 1080 --codec MJPEG -o - | python3 send_mjpeg_ws.py
'''
async def handle_stream(websocket):
    try:
        marker = b'\xff\xd8'
        trailer = b'\xff\xd9'
        while True:
            image_buffer = io.BytesIO()
            data = sys.stdin.buffer.readline() # Read from stdin until boundary marker
            # print(data)
            if not data:
                break        
            if data.startswith(marker): # start of JPEG frame
                print("Start of JPEG frame")
                frame = bytearray()
                while True:
                    data = sys.stdin.buffer.readline()
                    if data.startswith(marker):
                        # Send the JPEG data over the WebSocket connection
                        await websocket.send(frame)
                        break
                    frame.extend(data)
                    # data = sys.stdin.buffer.readline()
                    # # print(data)
                    # image_buffer.seek(0)
                    # image_buffer.write(data)
                    # image_buffer.truncate()
                    # frame = image_buffer.getvalue()
                    # if data.startswith(trailer): # end of JPEG frame
                    #     await websocket.send(frame)
                    #     print("\n\tSent frame\n")
                    #     break
    except websockets.exceptions.ConnectionClosedError:
        pass

async def main():
    print("MJPEG WS Server started...")
    async with websockets.serve(handle_stream, '0.0.0.0', 3333): # start server on host, port
        await asyncio.Future() # run forever

if __name__ == '__main__':
    asyncio.run(main())
#!/usr/bin/env python3
import asyncio
import websockets
import sys
import io
'''
    Intended to be run from terminal as: 
    raspivid -vf -hf -fps 30 -t 0 -l -w 1920 -h 1080 --codec MJPEG -o - | python3 send_mjpeg_ws.py
'''
async def send_mjpeg_stream(websocket):
    try:   
        boundary = b'\xff\xd8\r\n'
        header = b'Content-Type: image/jpeg\r\n\r\n'
        while True:
            buffer = io.BytesIO()
            data = sys.stdin.buffer.read() # Read from stdin
            if not data:
                break
            if data.startswith(b'\xff\xd8'):
                buffer.seek(0)    
                buffer.write(data)
                # crop buffer to exact size
                buffer.truncate()
                # save the frame
                frame = buffer.getvalue()
                # wfile.write(b'--FRAME\r\n')
                # send_header('Content-Type', 'image/jpeg')
                # send_header('Content-Length', len(frame))
                # wfile.write(frame)
                # wfile.write(b'\r\n')
                await websocket.send(frame)
                
                # data = sys.stdin.buffer.read() # Read the header and JPEG data
                # if not data.startswith(header):
                #     break
                # jpeg_data = bytearray()
                # while True:
                #     data = sys.stdin.buffer.readline()
                #     if data.startswith(boundary):
                #         await websocket.send(jpeg_data) # Send the JPEG data over the WebSocket connection
                #         break
                #     jpeg_data.extend(data)
    except websockets.exceptions.ConnectionClosedError:
        pass

async def main():
    print("MJPEG WS Server started...")
    async with websockets.serve(send_mjpeg_stream, '0.0.0.0', 3333): # start server on host, port
        await asyncio.Future() # run forever

if __name__ == '__main__':
    asyncio.run(main())
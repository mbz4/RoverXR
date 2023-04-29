#!/usr/bin/env python3

import io
import time
from websockets.server import serve
import asyncio
import picamera
from threading import Condition

'''
FrameBuffer is a synchronized buffer which gets each frame and notifies to all waiting clients.
It implements write() method to be used in picamera.start_recording()
'''

class FrameBuffer(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
    
    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame
            with self.condition:
                # write to buffer
                self.buffer.seek(0)    
                self.buffer.write(buf)
                # crop buffer to exact size
                self.buffer.truncate()
                # save the frame
                self.frame = self.buffer.getvalue()
                # notify all other threads
                self.condition.notify_all()

'''
StreamingHandler extent http.server.SimpleHTTPRequestHandler class to handle mjpg file for live stream
'''

class StreamingHandler(SimpleHTTPRequestHandler):
    def __init__(self, frames_buffer, *args):
        self.frames_buffer = frames_buffer
        print("New StreamingHandler, using frames_buffer=", frames_buffer)
        super().__init__(*args)
    
    def __del__(self):
        print("Remove StreamingHandler")
    
    def do_GET(self):
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                # tracking serving time
                start_time = time.time()
                frame_count = 0
                # endless stream
                while True:
                    with self.frames_buffer.condition:
                        # wait for a new frame
                        self.frames_buffer.condition.wait()
                        # it's available, pick it up
                        frame = self.frames_buffer.frame
                        # send it
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                        # count frames
                        frame_count += 1
                        # calculate FPS every 5s
                        if (time.time() - start_time) > 5:
                            print("FPS: ", frame_count / (time.time() - start_time))
                            frame_count = 0
                            start_time = time.time()
            except Exception as e:
                print(f'Removed streaming client {self.client_address}, {str(e)}')
        else:
            # fallback to default handler
            super().do_GET()

'''
    Main function
'''
def stream():
    # open camera
    with picamera.PiCamera(resolution='1920x1080', framerate=30) as camera:
        
        # create buffer
        frame_buffer = FrameBuffer()

        # stream to buffer
        camera.start_recording(frame_buffer, format='mjpeg')

        # run server
        try:
            address = ('', 8000)
            httpd = ThreadingHTTPServer(address, lambda *args: StreamingHandler(frame_buffer, *args))
            httpd.serve_forever()
        finally:
            camera.stop_recording()

if __name__ == "__main__":
    stream()


async def send_mjpeg_stream(websocket):
    try:
        boundary = b'\xff\xd8\r\n'
        header = b'--FRAME\r\n\r\n'
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



'''
WS CLIENT ON LAPTOP
'''
async def echo(websocket):
    async for message in websocket:
        message = message.decode("utf-8")
        print(f"Message from client: {message}")
        await websocket.send(f"Received your message: {message}")

async def main():
    async with serve(echo, "localhost", 3333):
        print("Server started")
        await asyncio.Future()

asyncio.run(main())
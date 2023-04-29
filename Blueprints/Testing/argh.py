#!/usr/bin/python3
#modified from:
# https://github.com/raspberrypi/picamera2/blob/main/examples/mjpeg_server.py
#https://github.com/raspberrypi/picamera2/blob/main/examples/mjpeg_server_2.py
# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

import io
import logging
import socketserver
from http import server
from threading import Condition
from websockets.server import serve
import asyncio
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder, Quality
from picamera2.outputs import FileOutput
from libcamera import controls, Transform


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

async def handle_stream(websocket):
    global output
    try:
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
            await websocket.send(frame)
    except Exception as e:
        logging.warning('Removed streaming client %s: %s', client_address, str(e))
    
    async for message in websocket:
        message = message.decode("utf-8")
        print(f"Message from client: {message}")
        await websocket.send(f"Received your message: {message}")
    
picam2 = Picamera2()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.video_configuration.controls.FrameRate = 30.0 # default framerate=30fps
picam2.configure(picam2.create_video_configuration(main={"size": (1920, 1080)}, transform=Transform(hflip=1, vflip=1))) 
output = StreamingOutput()
picam2.start_recording(MJPEGEncoder(), FileOutput(output), Quality.LOW) #VERY_LOW=6Mbps, LOW=12Mbps, MEDIUM=18Mbps, HIGH=27Mbps 

async def main():
    try:
        async with serve(handle_stream, "localhost", 3333):
            print("Server started")
            await asyncio.Future()
    finally:
        picam2.stop_recording()
    

asyncio.run(main())


#!/usr/bin/python3
#modified from:
# https://github.com/raspberrypi/picamera2/blob/main/examples/mjpeg_server.py
#https://github.com/raspberrypi/picamera2/blob/main/examples/mjpeg_server_2.py
# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

import io
from threading import Condition
from websockets.server import serve
import asyncio
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder, Quality
from picamera2.outputs import FileOutput
from libcamera import Transform

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            print("Frame written")
            self.condition.notify_all()

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1920, 1080)}, transform=Transform(hflip=1, vflip=1))) 
output = StreamingOutput()
picam2.start_recording(MJPEGEncoder(), FileOutput(output), Quality.LOW) #VERY_LOW=6Mbps, LOW=12Mbps, MEDIUM=18Mbps, HIGH=27Mbps 
print("Recording started")

async def handle_stream(websocket):
    global output
    try:
        while True:
            print("pinging")
            with output.condition:
                output.condition.wait()
                frame = output.frame
            print("Sending frame")
            print(frame)
            await websocket.send(frame)
    except Exception as e:
        print(e)
    finally:
        print("Closing websocket")
        await websocket.close()

async def main():
    try:
        async with serve(handle_stream, "0.0.0.0", 3333):
            print("Server started")
            await asyncio.Future()
    except KeyboardInterrupt:
        pass
    finally:
        picam2.stop_recording()
        picam2.close()

asyncio.run(main())


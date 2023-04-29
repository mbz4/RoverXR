#!/usr/bin/python3

import io
from threading import Condition
from websockets.server import serve
import asyncio
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder, Quality
from picamera2.outputs import FileOutput
from libcamera import Transform, controls

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

picam2 = Picamera2()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.configure(picam2.create_video_configuration(main={"size": (1280, 720)}, transform=Transform(hflip=1, vflip=1))) 
output = StreamingOutput()
picam2.start_recording(MJPEGEncoder(), FileOutput(output), Quality.VERY_LOW) #VERY_LOW=6Mbps, LOW=12Mbps, MEDIUM=18Mbps, HIGH=27Mbps 
print('\033[2;31;43mRecording started\033[0;0m')

async def handle_stream(websocket):
    global output
    try:
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
            await websocket.send(frame)
    except Exception as e:
        print(e)
        print('\033[2;31;43m Closing websocket\033[0;0m')
        await websocket.close()

async def main():
    try:
        async with serve(handle_stream, "0.0.0.0", 3333, ping_interval=None, max_size = 3145728):
            print('\033[2;31;43mServer started\033[0;0m')
            await asyncio.Future()
    except KeyboardInterrupt:
        pass
    finally:
        picam2.stop_recording()
        picam2.close()
        print('\033[2;31;43mRecording stopped\033[0;0m')
        print("\033[2;31;43mExiting...\033[0;0m")
asyncio.run(main())
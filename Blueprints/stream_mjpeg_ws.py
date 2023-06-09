#!/usr/bin/python3 
# shebang line - specifies the path to the python interpreter on the pi zero 1 w
import io # import the io library
from threading import Condition #  import the condition class
from websockets.server import serve # import the websockets library
import asyncio # import the asyncio library
from picamera2 import Picamera2 # import the picamera2 library
from picamera2.encoders import MJPEGEncoder, Quality # import the MJPEG encoder and quality settings
from picamera2.outputs import FileOutput # import the file output
from libcamera import Transform # import the transform class

'''
    ToDo:
    - project to a curved surface in Godot
        - test w/ lens distortion
    - test w/ different resolutions, exposure times, analogue gains, quality settings
    - check out godot async options to offload main thread on inbound frame decoding to image buffer
        - maybe instead of creating texture, replace it
    - measure delay of invoking .load_jpg_from_buffer() @1080p30 on Quest 2
'''

'''
    Streaming buffer class:
    this class is used to store the frame from the camera to be sent to the client
'''
class StreamingOutput(io.BufferedIOBase): # inherit from BufferedIOBase
    def __init__(self): # constructor
        self.frame = None # used to store the frame
        self.condition = Condition() # used to notify the client when a new frame is available

    def write(self, buf): # write function
        with self.condition: # wait for the client to request a frame
            self.frame = buf # store the frame
            self.condition.notify_all() # notify the client

'''
    Picamera2 setup:
    used to configure the camera and start recording
'''
print('\033[2;31;43mConfiguring camera...\033[0;0m')
picam2 = Picamera2() # create a new camera object
picam2.configure(picam2.create_video_configuration(main={"size": (1280, 720)}, # set the resolution
                                                   transform=Transform(hflip=1, vflip=1))) # apply transforms to image
output = StreamingOutput() # create a new streaming buffer object
#picam2.controls.ExposureTime = 10000 # set the exposure time to 10ms
#picam2.controls.AnalogueGain = 1.0 # set the analogue gain to 1.0
picam2.start_recording(MJPEGEncoder(), # use the MJPEG encoder
                       FileOutput(output), # output the frames to the streaming buffer
                       Quality.VERY_LOW) #VERY_LOW=6Mbps, LOW=12Mbps, MEDIUM=18Mbps, HIGH=27Mbps 
print('\033[2;31;43mRecording started\033[0;0m')

'''
    Handle stream function:
    used to handle the websocket connection and send the frames to the client
'''
async def handle_stream(websocket): # websocket handler           
    global output # use the global output variable
    try: # try to run the code
        while True: # run forever
            with output.condition: # wait for a new frame
                output.condition.wait() # wait for a new frame
                frame = output.frame # get the frame
            await websocket.send(frame) # send the frame to the client   
    except Exception as e: # catch exceptions
        if e == KeyboardInterrupt: # catch keyboard interrupt
            pass # do nothing
        else:
            print(e) # print the exception
        
        print('\033[2;31;43m Closing websocket\033[0;0m')
        await websocket.close() # close the websocket connection

'''
    Main function:
    used to start the server and handle the websocket connection
'''
async def main():
    try:
        async with serve(handle_stream, "0.0.0.0", # server address
                         3333, # server port
                         ping_interval=None, # ping_interval = None to prevent connection timeout
                         max_size = 3538944): # max_size = 3.275MB = 27Mbps
            print('\033[2;31;43mServer started\033[0;0m')
            await asyncio.Future() # run forever
    except KeyboardInterrupt: # catch keyboard interrupt
        picam2.stop_recording() # gracefully stop recording
        picam2.close() # shutdown the camera gracefully
        print('\033[2;31;43mRecording stopped\033[0;0m') # notify user
    finally:
        print("\033[2;31;43mExiting...\033[0;0m")
try: 
    asyncio.run(main()) # start the server
except KeyboardInterrupt:
    pass
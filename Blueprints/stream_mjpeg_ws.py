#!/usr/bin/python3 
# shebang line - specifies the path to the python interpreter on the pi zero 1 w
import io # import the io library
from threading import Condition #  import the condition class
from websockets.server import serve # import the websockets library
import asyncio # import the asyncio library
from picamera2 import Picamera2, MappedArray # import the picamera2 library
from picamera2.encoders import MJPEGEncoder, Quality # import the MJPEG encoder and quality settings
from picamera2.outputs import FileOutput # import the file output
from libcamera import Transform # import the transform class
import cv2
import time
'''
    ToDo:
    - wrap for autostart streaming in do while loop on startup
        - systemd + bash script?
    - handle remote inbound comms (optional) 
        ==> need config file & method for handling camera reconfiguration
        ==> inbound message py file for modifying configs from Godot
    - play with exposure time to lessen shaky camera
    - add lens ==> project to curved surface in VR
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
picam2 = Picamera2() # create a new camera object

picam2.configure(picam2.create_video_configuration(main={"size": (1280, 720)}, # set the resolution
                                                   transform=Transform(hflip=1, vflip=1))) # apply transforms to image
output = StreamingOutput() # create a new streaming buffer object
picam2.controls.ExposureTime = 10000 # set the exposure time to 10ms
picam2.controls.AnalogueGain = 1.0 # set the analogue gain to 1.0

def apply_timestamp(request):
    colour = (0, 255, 0)
    origin = (0, 30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1
    thickness = 2
    timestamp = time.strftime("%Y-%m-%d %X")
    with MappedArray(request, "main") as m:
        cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)

picam2.pre_callback = apply_timestamp
picam2.start_recording(MJPEGEncoder(), # use the MJPEG encoder
                       FileOutput(output), # output the frames to the streaming buffer
                       Quality.VERY_LOW) #VERY_LOW=6Mbps, LOW=12Mbps, MEDIUM=18Mbps, HIGH=27Mbps 
print('\033[2;31;43mRecording started\033[0;0m')

'''
    Handle stream function:
    used to handle the websocket connection and send the frames to the client
'''
async def handle_stream(websocket): # websocket handler 
    # async def handle_inbound_msg(websocket): # this blocks outbound stream until next message received, not ideal
    #     message = await websocket.recv()
    #     if len(message) > 0:
    #         message = message.decode("utf-8")
    #         print(f"Message from client: {message}")
            
    global output # use the global output variable
    try: # try to run the code
        while True: # run forever
            #handle_inbound_msg(websocket) # tried to add inbound messaging feature to adjust configs & restart scripts
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
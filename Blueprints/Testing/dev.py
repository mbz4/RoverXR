#!/usr/bin/env python3
# vuquangtrong.github.io
#https://www.codeinsideout.com/blog/pi/stream-picamera-mjpeg/
import io
import time
import picamera
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Condition
from datetime import datetime
from websocket_server import WebsocketServer

"""
FrameBuffer is a synchronized buffer which gets each frame and notifies to all waiting clients.
It implements write() method to be used in picamera.start_recording()
"""
class FrameBuffer(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
    def write(self, buf):
        if buf.startswith(b'\xff\xd8'): # New frame
            with self.condition:
                self.buffer.seek(0) # set buffer to start    
                self.buffer.write(buf) # write to buffer
                self.buffer.truncate() # crop buffer to exact size
                self.frame = self.buffer.getvalue() # save the frame
                self.condition.notify_all() # notify all other threads

"""
StreamingHandler extent http.server.SimpleHTTPRequestHandler class to handle mjpg file for live stream
"""
class StreamingHandler(SimpleHTTPRequestHandler):
    
    def __init__(self, frames_buffer, *args):
        self.frames_buffer = frames_buffer
        print("New StreamingHandler, using frames_buffer=", frames_buffer)
        super().__init__(*args)
    
    def __del__(self):
        print("Remove StreamingHandler")
    
    def do_GET(self):
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

# Define a MJPEG streamer class
class handleStream(object):
    
    def __init__(self, frames_buffer, *args):
        self.frames_buffer = frames_buffer
        print("stream handler, using frames_buffer=", frames_buffer)
        super().__init__(*args)

    def __init__(self):
        self.frame = None
        self.condition = Condition()
    
    def start(self): # Start MJPEG streaming
        self.server = WebsocketServer(8080, host='localhost')
        self.server.set_fn_new_client(self.new_client)
        self.server.run_forever()
       
    def stop(self): # Stop MJPEG streaming
        self.server.shutdown()

    def new_client(self, client, server):# Handle new client connection
        print(f"New client connected and was given id {client['id']}")

    # Send new MJPEG frame to all clients
    def send_frame(self, frame):
        with self.condition:
            self.frame = frame
            self.condition.notify_all()

        self.server.send_message_to_all(self.frame.getvalue())

def stream():
    with picamera.PiCamera(resolution='1920x1080', # set resolution 
                           framerate=30, # set framerate
                           annotate_background=picamera.Color('black'), # black background for text
                           annotate_text=datetime.now().isoformat(sep=' ', timespec='milliseconds'), # add timestamp to video w/ ms resolution
                           led=True # turn recording led on
                           ) as camera: # open camera
        time.sleep(2) # camera warm-up time
        frame_buffer = FrameBuffer() # create buffer class instance        
        camera.start_recording(frame_buffer, format='mjpeg') # stream to buffer    
        try:
            address = ('0.0.0.0', 8000)
            httpd = ThreadingHTTPServer(address, lambda *args: StreamingHandler(frame_buffer, *args)) # run server
            httpd.serve_forever()
        finally:
            camera.stop_recording()

if __name__ == "__main__":
    stream()
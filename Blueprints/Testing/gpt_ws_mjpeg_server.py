import io
import logging
import threading
import picamera
from websocket_server import WebsocketServer
from threading import Condition

# Define a MJPEG streamer class
class MJPEGStreamer(object):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    # Start MJPEG streaming
    def start(self):
        self.server = WebsocketServer(8080, host='localhost')
        self.server.set_fn_new_client(self.new_client)
        self.server.run_forever()

    # Stop MJPEG streaming
    def stop(self):
        self.server.shutdown()

    # Handle new client connection
    def new_client(self, client, server):
        logging.info('New client connected and was given id %d', client['id'])

    # Send new MJPEG frame to all clients
    def send_frame(self, frame):
        with self.condition:
            self.frame = frame
            self.condition.notify_all()

        self.server.send_message_to_all(self.frame.getvalue())

# Define a MJPEG output class
class MJPEGOutput(object):
    def __init__(self, streamer):
        self.streamer = streamer

    # Write MJPEG frame to output
    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, send previous frame if available
            if hasattr(self, 'output'):
                self.streamer.send_frame(self.output)
            self.output = io.BytesIO()
        self.output.write(buf)


# Define a camera thread class
class CameraThread(threading.Thread):
    def __init__(self, streamer):
        super(CameraThread, self).__init__()
        self.streamer = streamer
        self.stop_event = threading.Event()

    # Start camera thread
    def run(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (1920, 1080)
            camera.framerate = 30
            camera.start_recording(
                output=MJPEGOutput(self.streamer),
                format='mjpeg'
            )

            while not self.stop_event.is_set():
                self.stop_event.wait(1)

            camera.stop_recording()

    # Stop camera thread
    def stop(self):
        self.stop_event.set()

if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create MJPEG streamer
    streamer = MJPEGStreamer()

    # Create camera thread
    camera_thread = CameraThread(streamer)

    # Start camera thread
    camera_thread.start()

    # Start MJPEG streaming
    streamer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        # Stop MJPEG streaming
        streamer.stop()

        # Stop camera thread
        camera_thread.stop()
        camera_thread.join()
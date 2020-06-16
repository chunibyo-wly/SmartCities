from importlib import import_module
import os
from flask import Flask, render_template, Response

# if os.environ.get('CAMERA'):
#     Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#     from lib.camera import Camera

from lib.camera_opencv import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


def gen2(camera):
    """Returns a single image frame"""
    frame = camera.get_frame()
    yield frame


@app.route('/video_feed')
def image():
    """Returns a single current image for the webcam"""
    return Response(gen2(Camera()), mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, threaded=True)

import os
from io import BytesIO
import requests
from PIL import Image
import numpy as np
import cv2
import json
import base64

from lib.base_camera import BaseCamera

class Camera(BaseCamera):
    video_source = None
    detector = None

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        cnt = 0
        while True:
            cnt += 1

            r = requests.get(Camera.video_source)
            _img = np.array(Image.open(BytesIO(r.content)).convert('RGB'))

            _img = _img[:, :, ::-1]
            img = _img.copy()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

import os
import cv2

from conf import input_conf
from lib.base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = input_conf.VIDEO_SOURCE

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            ret, img = camera.read()

            if not ret:
                camera.set(cv2.CAP_PROP_POS_FRAMES, 0)
            else:
                # encode as a jpeg image and return it
                yield cv2.imencode('.jpg', img)[1].tobytes()

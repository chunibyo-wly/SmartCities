import os
from io import BytesIO
import requests
from PIL import Image
import numpy as np
import cv2

import conf
from lib.base_camera import BaseCamera

import lib.yolov4.tf as yolo


class Camera(BaseCamera):
    video_source = conf.INPUT_STREAM
    detector = yolo.YoloV4(
        names_path="./data/darknet/coco.names",
        weights_path="./data/darknet/yolov4.weights",
    )
    person_list = []
    person_number = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        while True:
            r = requests.get(Camera.video_source)
            _img = np.array(Image.open(BytesIO(r.content)).convert('RGB'))

            _img = _img[:, :, ::-1]
            img = _img.copy()
            img, boxs = Camera.detector.predict(img, Camera.detector.classes)

            Camera.person_list = [_img[int(i[1]):int(i[3]), int(i[0]):int(i[2])] for i in boxs]
            Camera.person_number = len(boxs)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

import os
import cv2

from lib.base_camera import BaseCamera


# class Camera(BaseCamera):
#     """An emulated camera implementation that streams a repeated sequence of
#     files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
#     imgs = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]
#
#     @staticmethod
#     def frames():
#         while True:
#             time.sleep(1)
#             yield Camera.imgs[int(time.time()) % 3]

class Camera(BaseCamera):
    video_source = "./data/stlucia_testloop.avi"

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

import os
from io import BytesIO
import requests
from PIL import Image
import numpy as np
import cv2
from torchvision import transforms as T
import torch
from model.attribute.net import get_model
import json
import base64

from lib.base_camera import BaseCamera


def load_network(network, model_name):
    save_path = os.path.join('./data/checkpoints', 'market', model_name, 'net_last.pth')
    network.load_state_dict(torch.load(save_path))
    print('Resume model from {}'.format(save_path))
    return network


class predict_decoder(object):

    def __init__(self, dataset):
        with open('./model/attribute/doc/label.json', 'r') as f:
            self.label_list = json.load(f)[dataset]
        with open('./model/attribute/doc/attribute.json', 'r') as f:
            self.attribute_dict = json.load(f)[dataset]
        self.dataset = dataset
        self.num_label = len(self.label_list)

    def decode(self, pred):
        pred = pred.squeeze(dim=0)
        result = {}
        for idx in range(self.num_label):
            name, chooce = self.attribute_dict[self.label_list[idx]]
            if chooce[pred[idx]]:
                # print('{}: {}'.format(name, chooce[pred[idx]]))
                result[name] = chooce[pred[idx]]
        return result


class Camera(BaseCamera):
    video_source = None
    detector = None
    person_list = []
    attribute_list = []

    ######################################################################
    # Settings
    # ---------
    dataset_dict = {
        'market': 'Market-1501',
        'duke': 'DukeMTMC-reID',
    }
    num_cls_dict = {'market': 30, 'duke': 23}
    num_ids_dict = {'market': 751, 'duke': 702}

    transforms = T.Compose([
        T.Resize(size=(288, 144)),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    ######################################################################
    # Argument
    # ---------

    model_name = '{}_nfc_id'.format('resnet50') if None else '{}_nfc'.format('resnet50')
    num_label, num_id = num_cls_dict['market'], num_ids_dict['market']

    model = get_model(model_name, num_label, use_id=None, num_id=num_id)
    model = load_network(model, model_name)
    model.eval()

    Dec = predict_decoder('market')

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
            img, boxs = Camera.detector.predict(img, Camera.detector.classes)

            if cnt % 20 == 0:

                print(torch.cuda.is_available())

                Camera.person_list = [_img[int(i[1]):int(i[3]), int(i[0]):int(i[2])] for i in boxs]
                Camera.attribute_list.clear()
                for person in Camera.person_list:
                    src = Image.fromarray(np.uint8(person)).convert('RGB')
                    src = Camera.transforms(src)
                    src = src.unsqueeze(dim=0)
                    out = Camera.model.forward(src)

                    pred = torch.gt(out, torch.ones_like(out) / 2)  # threshold=0.5

                    Dec = predict_decoder('market')
                    result = Dec.decode(pred)
                    result['img'] = base64.b64encode(
                        cv2.imencode('.jpg', person[:person.shape[0] // 3])[1]) \
                        .decode('utf-8')
                    Camera.attribute_list.append(result)

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

FROM tensorflow/tensorflow:2.2.0-gpu

EXPOSE 5000
ENV DIR=/home/app \
    STREAM=http://172.17.0.1:8888/video_feed \
    NAMES_PATH=./data/darknet/coco.names \
    WEIGHT_PATH=./data/darknet/yolov4.weights

RUN  mkdir -p /home/app \
    && apt update \
    && apt-get install -y libsm6 libxext6 libxrender-dev \
    && cd $DIR

WORKDIR $DIR
COPY . $DIR

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

ENTRYPOINT python server.py -s $STREAM -n $NAMES_PATH -w $WEIGHT_PATH

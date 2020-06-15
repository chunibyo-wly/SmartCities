FROM tensorflow/tensorflow:2.2.0-gpu

EXPOSE 5000
ENV dir /home/app

RUN  mkdir -p /home/app \
    && apt update \
    && apt-get install -y libsm6 libxext6 libxrender-dev \
#     &&  apt -y upgrade \
    && cd $dir

WORKDIR $dir
COPY . $dir

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

ENTRYPOINT ["python", "app.py"]

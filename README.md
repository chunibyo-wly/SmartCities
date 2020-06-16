<h1 align="center">
<img src="img/logo.png" alt="">

[![Actions Status][s0]][l0] [![Docker Pulls][s1]][l1]
</h1>

[s0]: https://github.com/chunibyo-wly/SmartCities/workflows/build/badge.svg
[l0]: https://github.com/chunibyo-wly/SmartCities/actions
[s1]: https://img.shields.io/docker/pulls/chunibyo/cities
[l1]: https://hub.docker.com/r/chunibyo/cities

# :jack_o_lantern: 感谢

1. [flask视频流](https://github.com/miguelgrinberg/flask-video-streaming)
2. [穷人的深度学习相机](https://github.com/burningion/poor-mans-deep-learning-camera)

# :panda_face: 如何使用

## docker

1. 修改``docker-compose`运行环境为`nvidia`

   ```yml
   {
       "default-runtime": "nvidia",
       "runtimes": {
           "nvidia": {
               "path": "nvidia-container-runtime",
               "runtimeArgs": []
           }
       },
       "registry-mirrors": ["https://r9hjzu0e.mirror.aliyuncs.com"]
   }
   ```

2. 修改`cities.yml`中`volumes`与`environment`

    ```bash
    docker-compose -f cities.yml up -d
    ```

## shell

```shell
pip3 install -r requirements
python3 server.py
```




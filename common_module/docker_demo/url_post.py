# -*- coding: utf-8 -*-
# @Time: 2020/3/10 13:08
import warnings
warnings.filterwarnings(action='ignore')

import requests

url = "http://192.168.1.202:8401/docker_demo"

r = requests.post(url, json={})
print("接口返回：\n",r.text, flush=True)









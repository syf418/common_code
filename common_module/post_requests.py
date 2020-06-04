# -*- coding: utf-8 -*-
# @Time: 2020/6/4 10:06
# -*- coding: utf-8 -*-
# @Time: 2020/5/26 9:47
import warnings
warnings.filterwarnings(action='ignore')

import requests

def post_task(url, post_data):
    try:
        response = requests.post(url, json=post_data)
        print("response:", response)
        response.encoding='utf-8'
        result=response.json()
        if result['status']==0:
            print('调用成功，返回值：')
            print(response.json())
        else:
            print('调用失败，返回值：')
            print(response.json())
    except Exception as e:
        print('调用出错，错误：')
        print(str(e))

# -*- coding: utf-8 -*-
# @Time: 2020/3/25 10:57
import warnings
warnings.filterwarnings(action='ignore')

import logging
import os
import time

def logging_func(log_path="../log/"):

    if not os.path.exists(log_path):
        os.makedirs(log_path)
    start_time = time.strftime("%Y%m%d", time.localtime())

    logger = logging.getLogger(__name__)
    logger.setLevel(level = logging.INFO)
    handler = logging.FileHandler(log_path + "{}_log.txt".format(start_time))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


# -*- coding: utf-8 -*-
# @Time: 2020/3/25 13:08
import warnings
warnings.filterwarnings(action='ignore')

import os
import shutil
import traceback

from common_project.common_module.logging_module import logging_func
logger = logging_func()

def makeDirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def deleteDirs(dirs):
    try:
        if os.path.exists(dirs):
            shutil.rmtree(dirs)
    except Exception as e:
        logger.exception(str(traceback.print_exc()))
        print("CLEARN Error %s" % (e), flush=True)
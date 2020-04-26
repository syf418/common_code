# -*- coding: utf-8 -*-
# @Time: 2020/3/25 13:08
import warnings
warnings.filterwarnings(action='ignore')

import os
import shutil


def makeDirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def deleteDirs(dirs):
    try:
        if os.path.exists(dirs):
            shutil.rmtree(dirs)
    except Exception as e:
        print("CLEARN Error %s" % (e), flush=True)
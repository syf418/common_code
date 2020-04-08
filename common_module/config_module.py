# -*- coding: utf-8 -*-
# @Time: 2020/3/25 10:47
import warnings
warnings.filterwarnings(action='ignore')

import os
from configparser import ConfigParser
from common_project.common_module.userDefinedError import ConfigReadError

def get_config(item, calling_location=0):
    '''
    :param item:
    :param calling_location: 1 -> outer calling, 0 -> inner calling
    :return:
    '''
    if calling_location:
        filename = os.getcwd() + '/config.ini'
    else:
        filename = "../config.ini"
    parser = ConfigParser()
    parser.read(filename, encoding='utf-8')
    try:
        args = parser.items(item)
        return dict(args)
    except:
        raise ConfigReadError

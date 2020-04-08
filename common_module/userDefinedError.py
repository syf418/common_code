# -*- coding: utf-8 -*-
# @Time: 2020/3/23 17:00
import warnings
warnings.filterwarnings(action='ignore')

class NonSupportError(Exception):
    def __init__(self):
        self.__str__()
    def __str__(self):
        return "Currently not supported!"

class NoResultsError(Exception):
    def __str__(self):
        return "This item was not found!"

class ConfigReadError(Exception):
    def __str__(self):
        return "Failed to read the configuration information!"

class dataTypeError(Exception):
    def __str__(self):
        return "Data type mismatched!"
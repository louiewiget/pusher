#encoding: utf-8

import sys
import logging
sys.path.append("..")
from utils import *

from abc import ABCMeta, abstractmethod


class Processor(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        pass


    @abstractmethod
    def omit(self, entity, contentMap):
        pass

    @abstractmethod
    def finish(self):
        pass

    def splitPattern(self, patternList):
        descList = []
        typeName = "Unknown"
        if isinstance(patternList, list):
            for pattern in patternList:
                if isinstance(pattern, str):
                    arr = pattern.split("=")
                    if len(arr) >= 2:
                        if arr[1] == "type":
                            typeName = arr[0]
                            continue
                        descList.append(arr)
                else:
                    logging.warning("pattern is not a str[%s]" % pattern)
        else:
            logging.warning("patternList is not List [%s]" % patternList)
        return typeName, descList

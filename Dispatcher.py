#encoding: utf-8
import logging
import importlib
import json
import traceback
import os
import sys

from DispatcherConfig import DispatchMap, WholeProcessorList



class Dispatcher(object):

    def __init__(self, entityList):
        self.entityList = entityList
        self.importmodules = {}
        self.instanceDict = {}

    def process(self):
        for one in self.entityList:
            config = one.getConfig()
            if "tags" in config:
                if isinstance(config['tags'], list):
                    tags = config['tags']
                    for tag in tags:
                        if "name" in tag and tag["name"] == u"推送对象" and "values" in tag:
                            if isinstance(tag["values"], list):
                                for value in tag["values"]:
                                    if value in DispatchMap:
                                        for processor in DispatchMap[value]:
                                            if os.environ['limit'] != processor:
                                                logging.info("processor[%s] is not allow. current[%s] " % (processor, os.environ['limit']))
                                                continue
                                            self.callProcessor(processor, one)
            for processor in WholeProcessorList:
                if os.environ['limit'] != processor:
                    logging.info("processor[%s] is not allow. current[%s] " % (processor, os.environ['limit']))
                    continue
                self.callProcessor(processor)
        self.finishProcesser()


    def callProcessor(self, processor, record):
        try:
            moduleName = "handler.%s" % processor
            m1 = None
            if moduleName in self.importmodules:
                m1 = self.importmodules[moduleName]
            else:
                m1 = importlib.import_module("handler.%s" % processor)

            className = getattr(m1, processor)
            if className in self.instanceDict:
                instance = self.instanceDict[className]
            else:
                instance = className()
                self.instanceDict[className] = instance
            ret = instance.omit(record)

        except Exception as e:
            logging.warning("no handler exists[%s][%s][%s]" % (processor, e, traceback.format_exc()));

    def finishProcesser(self):
        for k, v in self.instanceDict.iteritems():
            v.finish()

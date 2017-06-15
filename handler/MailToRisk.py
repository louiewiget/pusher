#encoding: utf-8

import os
import logging
import json

from Processor import *

class MailToRisk(Processor):

    online_vars = {"cc":"", "from":"", "to":""}
    debug_vars = {"cc":"", "from":"", "to":""}

    def __init__(self):
        if "debug" in os.environ and os.environ["debug"]:
            self.mailVals = MailToRisk.debug_vars
        else:
            self.mailVals = MailToRisk.online_vars
        self.mailContents = ""

    def finish(self):
        MailUtils.mail("guminli@baidu.com,liuguodong01@baidu.com", "", "", "每日公告",self.mailContents)

    def omit(self, entity, contentMap):
        if entity.getType() in contentMap:
            typeName, descList = self.splitPattern(contentMap[entity.getType()])
            contents = JsonLocator.JsonLocator.extractElement(entity.getContent(), descList)
            contents.insert(0, {"key": "类型", "value": "新闻"})
            contents.insert(0, {"key": "id", "value":entity.getId()})
            self.mailContents += self.printContent(contents)
        else:
            logging.warning("contentMap does not have type[%s]" % entity.getType())
        pass

    def printContent(self, contents):
        data = ""
        for content in contents:
            if content['value'] is not None:
                data += "%s: %s\r\n" % (content['key'], content['value'])
        data += "-----------------\r\n"
        return data

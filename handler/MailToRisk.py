#encoding: utf-8

import os
import logging
import json
import chardet
import sys

reload(sys)

sys.setdefaultencoding("utf-8")

from Processor import *

class MailToRisk(Processor):

    # id 类型 标题  发布时间 发布主体
    relationship = ["id", "类型","标题","发布时间", "发布主体", "url"]
    mailUnits = '''<tr><td>%s</td><td>%s</td><td><a href='%s'>%s</a></td><td>%s</td><td>%s</td></tr>\r\n'''
    online_vars = {"cc":"", "from":"", "to":""}
    debug_vars = {"cc":"", "from":"", "to":""}

    typeMap = {"WEIBO": "微博", "NEWS":"新闻", "TIEBA":"贴吧"}

    def __init__(self):
        if "debug" in os.environ and os.environ["debug"]:
            self.mailVals = MailToRisk.debug_vars
        else:
            self.mailVals = MailToRisk.online_vars
        self.mailContents = []

    def finish(self):
        if len(self.mailContents) == 0:
            return
        mailHtml = ""
        for element in self.mailContents:
            mailHtml += MailToRisk.mailUnits % (element[0], element[1], element[5], element[2], element[3], element[4])
        with open ("tpl/mail.tpl") as f:
            data = f.read()
            MailUtils.mail("guminli@baidu.com,liuguodong01@baidu.com", "", "", "风险标记报送", data.replace("${mailContent}", mailHtml))

    def omit(self, entity, contentMap):
        if entity.getType() in contentMap:
            typeName, descList = self.splitPattern(contentMap[entity.getType()])
            contents = JsonLocator.JsonLocator.extractElement(entity.getContent(), descList)
            contents.insert(0, {"key": "类型", "value": typeName})
            contents.insert(0, {"key": "id", "value":entity.getId()})
            relationshipLen = len(MailToRisk.relationship)
            resulTuple = [""] * relationshipLen
            for i in range(relationshipLen):
                for content in contents:
                    if "key" in content and MailToRisk.relationship[i] == content["key"]:
                        if "value" in content:
                            value = content["value"]

                            if isinstance(value, str):
                                try:
                                    value = value
                                except Exception as e:
                                    print "try to filter illegal character failed [%s]" % value
                            resulTuple[i] = value
                            break;
            self.mailContents.append(resulTuple)
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

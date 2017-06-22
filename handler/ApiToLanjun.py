#encoding: utf-8

import os
import logging
import json
import requests
import sys

reload(sys)

sys.setdefaultencoding("utf-8")

from Processor import *

class ApiToLanjun(Processor):


    typeMap = {"WEIBO": "微博", "NEWS":"新闻", "TIEBA":"贴吧"}

    contentMap = {}
    contentMap['NEWS'] = ["新闻=type", "标题=contents.0.title", "发布时间=contents.0.publish_time", "发布主体=contents.0.author", "url=contents.0.url", "content=todo"]
    contentMap["ZHIHU"] = ["知乎=type", "标题=question_title", "发布时间=update_time", "发布主体=random","url=url","content=todo"]
    contentMap["WEIBO"] = ["微博=type", "标题=content", "发布时间=time", "发布主体=username", "url=url","content=todo"]
    contentMap["TIEBA"] = ["贴吧=type", "标题=thread_title", "发布时间=thread_publish_time", "发布主体=thread_username", "url=url","content=todo"]
    contentMap["MANUAL"] = ["MANUAL=type", "source=real_type", "标题=title", "发布时间=publish_time", "发布主体=publisher", "url=url", "content=todo"]


    def __init__(self):
        pass

    def finish(self):
        pass
    def omit(self, entity):
        riskType = ""
        companyName = ""
        publish_time = ""

        source = entity.getType()

        riskTypeValues = JsonLocator.JsonLocator.extractTags(config, "风险类型")
        companyNameValues = JsonLocator.JsonLocator.extractTags(config, "涉及客户")

        if len(companyNameValues) > 0:
            companyName = companyNameValues[0].encode('utf-8')
        if len(riskTypeValues) > 0:
            riskType = riskTypeValues[0].encode('utf-8')

        if entity.getType() in ApiToLanjun.contentMap:
            typeName, descList = self.splitPattern(ApiToLanjun.contentMap[entity.getType()])
            source = typeName
            contents = JsonLocator.JsonLocator.extractElement(entity.getContent(), descList)
            for one in contents:
                if "key" in one and "value" in one:
                    if one["key"] == "url" and one["value"] != "":
                        if url == "":
                            url = one["value"]
                    elif one["key"] == "content" and one["value"] != "":
                        if content == "":
                            content = one["value"]
                    elif one["key"] == "real_type" and one["value"] != "":
                        source = one["value"]

        # 信息丰富程度条件判断
        if companyName == "":
            logging.warn("could not find title for record [%s]" % one)
            return

        # 此处处理发信息逻辑
        postData = {"compname":"%s" % companyName, "url":"%s" % companyName, "type":"%s" % riskType, "optime":"%s" % publish_time}
        res = requests.post('http://cp01-chengxin-ucard00.epc.baidu.com:8084/yuqingtag/getYuqingData.php', data = postData)
        print res.content

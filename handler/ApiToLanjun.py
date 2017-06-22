#encoding: utf-8

import os
import logging
import json
import chardet
import sys

reload(sys)

sys.setdefaultencoding("utf-8")

from Processor import *

class ApiToLanjun(Processor):

    # id 类型 标题  发布时间 发布主体
    relationship = ["id", "类型","标题","发布时间", "发布主体", "url"]
    mailUnits = '''<tr><td>%s</td><td>%s</td><td><a href='%s'>%s</a></td><td>%s</td><td>%s</td></tr>\r\n'''
    online_vars = {"cc":"", "from":"", "to":""}
    debug_vars = {"cc":"", "from":"", "to":""}

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
        product = ""
        riskType = ""
        industry = ""
        hotLevel = ""
        trend = ""
        title = ""
        url = ""
        content = ""
        source = entity.getType()

        productValues = JsonLocator.JsonLocator.extractTags(config, "产品线")
        riskTypeValues = JsonLocator.JsonLocator.extractTags(config, "风险类型")

        if len(productValues) > 0:
            product = productValues[0].encode('utf-8')
        if len(riskTypeValues) > 0:
            riskType = riskTypeValues[0].encode('utf-8')

        if entity.getType() in MailToRisk.contentMap:
            typeName, descList = self.splitPattern(MailToRisk.contentMap[entity.getType()])
            source = typeName
            contents = JsonLocator.JsonLocator.extractElement(entity.getContent(), descList)
            for one in contents:
                if "key" in one and "value" in one:
                    if one["key"] == "title" and one["value"] != "":
                        if title == "":
                            title = one['value']
                    elif one["key"] == "url" and one["value"] != "":
                        if url == "":
                            url = one["value"]
                    elif one["key"] == "content" and one["value"] != "":
                        if content == "":
                            content = one["value"]
                    elif one["key"] == "real_type" and one["value"] != "":
                        source = one["value"]

        # 信息丰富程度条件判断
        if title == "":
            logging.warn("could not find title for record [%s]" % one)
            return
            
        # 此处处理发信息逻辑
        with open ("tpl/singleMail.tpl") as f:
            data = f.read()
            data = data.replace("${hotLevel}", hotLevel).replace("${trend}", trend)
            MailUtils.mail("guminli@baidu.com", "", "", "【标题】风险标记报送 %s" % title , data.replace("${mailContent}", mailHtml))

#encoding: utf-8

import os
import logging
import json
import sys

reload(sys)

sys.setdefaultencoding("utf-8")

from Processor import *

class SingleMail(Processor):

    # id 类型 标题  发布时间 发布主体
    relationship = ["id", "类型","标题","发布时间", "发布主体", "url"]
    mailUnits = '''<tr><td>%s</td><td>%s</td><td><a href='%s'>%s</a></td><td>%s</td><td>%s</td></tr>\r\n'''
    online_vars = {"cc":"", "from":"", "to":""}
    debug_vars = {"cc":"", "from":"", "to":""}

    typeMap = {"WEIBO": "微博", "NEWS":"新闻", "TIEBA":"贴吧"}

    contentMap = {}
    contentMap['NEWS'] = ["新闻=type", "title=contents.0.title",  "url=contents.0.url"]
    contentMap["ZHIHU"] = ["知乎=type", "title=question_title", "url=url"]
    contentMap["WEIBO"] = ["微博=type", "title=content",  "url=url"]
    contentMap["TIEBA"] = ["贴吧=type", "title=thread_title", "url=url"]
    contentMap["MANUAL"] = ["MANUAL=type", "source=real_type", "title=title", "url=url"]


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
        searchKey = ""
        companyName = ""
        source = entity.getType()
        config = entity.getConfig()

        productValues = JsonLocator.JsonLocator.extractTags(config, "产品线")
        riskTypeValues = JsonLocator.JsonLocator.extractTags(config, "风险类型")
        industryValues = JsonLocator.JsonLocator.extractTags(config, "行业")
        hotLevelValues = JsonLocator.JsonLocator.extractTags(config, "风险等级")
        trendValues = JsonLocator.JsonLocator.extractTags(config, "传播趋势")
        titleValues = JsonLocator.JsonLocator.extractTags(config, "编辑标题")
        urlValues = JsonLocator.JsonLocator.extractTags(config, "编辑链接")

        if len(productValues) > 0:
            product = productValues[0].encode('utf-8')
        if len(riskTypeValues) > 0:
            riskType = riskTypeValues[0].encode('utf-8')
        if len(industryValues) > 0:
            industry = industryValues[0].encode('utf-8')
        if len(hotLevelValues) > 0:
            hotLevel = hotLevelValues[0].encode('utf-8')
        if len(trendValues) > 0:
            trend = trendValues[0].encode('utf-8')
        if len(titleValues) > 0:
            title = titleValues[0].encode('utf-8')
        if len(urlValues) > 0:
            url = urlValues[0].encode('utf-8')

        if entity.getType() in SingleMail.contentMap:
            typeName, descList = self.splitPattern(SingleMail.contentMap[entity.getType()])
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
            logging.warn("could not find title for record [%s]" % entity.getId())
            return
        with open ("tpl/singleMail.tpl") as f:
            data = f.read()
            data = data.replace("${hotLevel}", hotLevel).replace("${trend}", trend).replace("${source}", source)\
                   .replace("${industry}", industry).replace("${riskType}", riskType).replace("${product}", product)\
                   .replace("${title}", title).replace("${url}", url).replace("${content}", content)\
                   .replace("${companyName}", companyName).replace("${searchKey}", searchKey)
            # 此处进行标题截断处理，最多显示 20 个字符 + "..."
            titleUnicode = title.decode("utf-8")
            if len(titleUnicode) > 20:
                titleUnicode = titleUnicode[:20] + "..."
            title = titleUnicode.encode("utf-8")
            MailUtils.mail("guminli@baidu.com", "guminli@baidu.com",  "guminli@baidu.com", "【商业舆情】 %s" % title , data)

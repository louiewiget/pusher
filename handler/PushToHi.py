#encoding: utf-8
import logging
import sys
import json
import time
import requests
reload(sys)
sys.setdefaultencoding("utf-8")

from Processor import *

class PushToHi(Processor):

    jobFailReceiver = "guminli@baidu.com"
        # group = [1386356, 1557162, 1264210]   # 线上
    group = [1457875]  # 线下

    contentMap = {}
    contentMap['NEWS'] = ["title=contents.0.title", "url=contents.0.url"]
    contentMap["ZHIHU"] = ["title=question_title", "url=url"]
    contentMap["WEIBO"] = ["title=content", "url=url"]
    contentMap["TIEBA"] = ["title=thread_title", "url=url"]
    contentMap["MANUAL"] = ["title=title", "url=url"]
    NEGATIVE_STRING = "百度商业负面"
    def __init__(self):
        self.hiContents = {}
        self.hiContents["百度商业负面"] = []


    def omit(self, entity):
        config = entity.getConfig()
        informValues = JsonLocator.JsonLocator.extractTags(config, "信息类型")
        if informValues is None or len(informValues) <= 0:
            logging.warning("record has no information type id[%s]" % entity.getId())
            return
        infoType = informValues[0].strip().encode('utf-8')
        product = ""
        risk = ""
        title = ""
        url = ""

        if infoType == "百度商业负面":
            productValues = JsonLocator.JsonLocator.extractTags(config, "行业")
            riskType = JsonLocator.JsonLocator.extractTags(config, "风险类型")

            if len(productValues) > 0:
                product = productValues[0].encode('utf-8')
            if len(riskType) > 0:
                risk = riskType[0].encode('utf-8')

        titleValues = JsonLocator.JsonLocator.extractTags(config, "编辑标题")
        urlValues = JsonLocator.JsonLocator.extractTags(config, "编辑链接")
        if len(titleValues) > 0 and titleValues[0] != "":
            title = titleValues[0].encode('utf-8')
        if len(urlValues) > 0 and urlValues[0] != "":
            url = urlValues[0].encode('utf-8')

        if entity.getType() in PushToHi.contentMap:
            typeName, descList = self.splitPattern(PushToHi.contentMap[entity.getType()])
            contents = JsonLocator.JsonLocator.extractElement(entity.getContent(), descList)
            for content in contents:
                if "key" in content and "value" in content:
                    if content["key"] == "title" and content["value"] != "":
                        if title == "":
                            title = content['value']
                    elif content["key"] == "url" and content["value"] != "":
                        if url == "":
                            url = content["value"]
            if title == "":
                logging.warn("could not find title for record [%s]" % one)
                return
        hiContent = {"title": title, "url": url, "product": product, "risk": risk}
        if infoType not in self.hiContents:
            self.hiContents[infoType] = []
        self.hiContents[infoType].append(hiContent)


    def sendYixiuMsg(self, contents):
        msgArr = []
        msgArr.append("<text c=\"百度商业负面\"/>")
        if len(self.hiContents["百度商业负面"]) > 0:
            i = 1
            for singleRecord in self.hiContents["百度商业负面"]:
                prefix = ""
                if singleRecord['product'] != "" and singleRecord['risk'] != "":
                    prefix = "【%s - %s】" % (singleRecord['product'], singleRecord['risk'])
                elif singleRecord['risk'] != "":
                    prefix = "【%s】" % singleRecord['risk']
                elif singleRecord['product'] != "":
                    prefix = "【%s】" % singleRecord['product']
                title = prefix + singleRecord['title'].replace("\"", "\'")
                if singleRecord["url"] != "":
                    msgArr.append("<text c=\"\n%s. %s\n\"/><url ref=\"%s\"/>" % (i, title, singleRecord["url"]))
                else:
                    msgArr.append("<text c=\"\n%s. %s\n\"/>" % (i, title))
                i += 1
        else:
            msgArr.append("""<text c="\n暂无"/>""")

        for infoType, records in self.hiContents.iteritems():
            if infoType == "百度商业负面":
                continue
            msgArr.append("<text c=\"\n\n%s\"/>" % infoType)
            if len(records) > 0:
                i = 1
                for singleRecord in records:
                    prefix = ""
                    title = singleRecord['title'].replace("\"", "\'")
                    if singleRecord["url"] != "":
                        msgArr.append("<text c=\"\n%s. %s\n\"/><url ref=\"%s\"/>" % (i, title, singleRecord["url"]))
                    else:
                        msgArr.append("<text c=\"\n%s. %s\n\"/>" % (i, title))
                    i += 1
            else:
                msgArr.append("""<text c="\n暂无"/>""")
        msg = "".join(msgArr)
        msgContent = "<msg><text c=\"【定点报送】Dear all,%s 监测到的信息如下:\n\"/>%s</msg>" % (time.strftime("%Y年%m月%d日 %H:00"), msg)

        try:
            data = {}
            data['msg'] = msgContent
            data['instance'] = 'yixiu_robot_07'
            data['format'] = "rich"
            for id in PushToHi.group:
                data['to_group'] = id
            # ret = requests.post('http://yixiu.baidu.com:5656/talk', data=data, timeout=5)
            if ret.status_code != 200:
                return False, msgContent
            else:
                return True, msgContent
        except Exception as e:
            logging.warn(e)
            return False, msgContent

    def sendPublicHiMsg(self, contents):
        msgArr = []
        msgArr.append("百度商业负面")
        if len(self.hiContents["百度商业负面"]) > 0:
            i = 1
            for singleRecord in self.hiContents["百度商业负面"]:
                prefix = ""
                if singleRecord['product'] != "" and singleRecord['risk'] != "":
                    prefix = "【%s - %s】" % (singleRecord['product'], singleRecord['risk'])
                elif singleRecord['risk'] != "":
                    prefix = "【%s】" % singleRecord['risk']
                elif singleRecord['product'] != "":
                    prefix = "【%s】" % singleRecord['product']
                title = prefix + singleRecord['title'].replace("\"", "\'")
                if singleRecord["url"] != "":
                    msgArr.append("\n%s. %s\n%s" % (i, title, singleRecord["url"]))
                else:
                    msgArr.append("\n%s. %s" % (i, title))
                i += 1
        else:
            msgArr.append("\n暂无")

        for infoType, records in self.hiContents.iteritems():
            if infoType == "百度商业负面":
                continue
            msgArr.append("\n\n%s" % infoType)
            if len(records) > 0:
                i = 1
                for singleRecord in records:
                    prefix = ""
                    title = singleRecord['title']
                    if singleRecord["url"] != "":
                        msgArr.append("\n%s. %s\n%s" % (i, title, singleRecord["url"]))
                    else:
                        msgArr.append("\n%s. %s" % (i, title))
                    i += 1
            else:
                msgArr.append("\n暂无")
        msg = "".join(msgArr)
        msgContent = "【定点报送】Dear all,%s 监测到的信息如下:\n%s" % (time.strftime("%Y年%m月%d日 %H:00"), msg)

        try:
            data = {}
            data['msg_type'] = 'text'
            data['to'] = '公关'
            data['access_token'] = 'd39752a9cca862ef7686590430e16575'
            data['content'] = msgContent
            ret = requests.post('http://xp2.im.baidu.com/ext/1.0/sendGroupMsg', data = data, timeout=5)
            if ret.status_code != 200:
                return False, msgContent
            else:
                return True, msgContent
        except Exception as e:
            logging.warn(e.message)
        return False, msgContent

    def finish(self):

        ret, msg = self.sendYixiuMsg(self.hiContents)
        if ret == False:
            errmsg = "send yixiu msg failed, use msg to try manual[%s]" % msg
            logging.warn(errmsg)
            MailUtils.mail(PushToHi.jobFailReceiver, "", "", "一休定点报送任务失败，请重试", errmsg)
        else:
            MailUtils.mail(PushToHi.jobFailReceiver, "", "", "一休定点报送任务成功，请检查", msg)

        ret, msg = self.sendPublicHiMsg(self.hiContents)
        if ret == False:
            errmsg = "send public Hi Msg, use msg to try manual[%s]" % msg
            logging.warn(errmsg)
            MailUtils.mail(PushToHi.jobFailReceiver, "", "", "公众号定点报送任务失败", errmsg)
        else:
            MailUtils.mail(PushToHi.jobFailReceiver, "", "", "公众号定点报送任务成功，请检查", msg)
        print msg

#encoding: utf-8

import json
import sys
import logging

class JsonLocator(object):

    @staticmethod
    def extractElement(jsonObj, descList):
        if isinstance(descList, list):
            keys = []
            pathList = []
            for desc in descList:
                if len(desc) >= 2:
                     keys.append(desc[0])
                     pathList.append(desc[1])
                else:
                    logging.warning("not a validate descript[%s]", json.dumps(desc))
            retList = JsonLocator.findElement(jsonObj, pathList)
            if len(keys) == len(retList):
                retData = []
                for i in range(len(keys)):
                    retData.append({"key":keys[i], "value": retList[i]})
                return retData
            else:
                logging.warning("elemnt keys length mismatch with retList")
        else:
            logging.warning("descDict is not a dict")
        return None

    @staticmethod
    def findElement(jsonObj, pathList):
        retList = []
        for path in pathList:
            pathTokens = path.split(".")
            retList.append(JsonLocator.findElementByTokenList(jsonObj, pathTokens))
        return retList

    @staticmethod
    def findElementByTokenList(jsonObj, pathTokens):
        contentObj = jsonObj
        for token in pathTokens:
            if token in contentObj:
                contentObj = contentObj[token]
            elif isinstance(contentObj, list) and token.isdigit():
                try:
                    intToken = int(token)
                    if len(contentObj) > intToken:
                        contentObj = contentObj[intToken]
                    else:
                        logging.warning("indice is to much longer[%s][%s]", (json.dumps(contentObj, ensure_ascii=False), intToken))
                        return None
                except Exception as e:
                    logging.warning(e)
                    return None
            else:
                return None
        return contentObj.encode("utf-8")

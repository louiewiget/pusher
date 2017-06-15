#encoding: utf8
import sys
import time
import logging

from DB import DB
from Properties import Properties
from RecordEntity import RecordEntity

import json



class DbReader(object):

    UPDATE_KEY = "update_key"

    def __init__(self):
        self.properties = Properties()
        self.__try_init()

    def  __try_init(self):
        tries = 3
        while tries > 0:
            try:
                self.db = DB("cae03")
                return True
            except Exception as e:
                logging.warning('init tahiti db failed,tries left [%s]' % tries)
                tries -= 1
        return False;


    def dataReader(self):
        if not hasattr(self, "db"):
            if not self.__try_init():
                logging.warning("db connection failed")
                raise Exception("db connection failed")
        updateTime = self.properties.read(DbReader.UPDATE_KEY)
        if updateTime is None:
            updateTime = "2017-01-01 00:00:00"
            self.properties.write(DbReader.UPDATE_KEY, updateTime)
        endTime = time.strftime("%Y-%m-%d %H:%M:%S")
        varList = RecordEntity().getVars()
        sql = "select %s from stella_public_info_record" \
              " where update_time > '%s' and update_time <= '%s'" % \
              (",".join(varList) ,updateTime, endTime)
        ret, data = self.db.query(sql)
        readData = []
        if ret:
            for one in data:
                oneLen = len(one)
                record = RecordEntity()
                for i in xrange(0, oneLen):
                    try:
                        col = varList[i]
                        data = one[i]
                        if col in RecordEntity.validation:
                            if RecordEntity.validation[col] == "json":
                                data = json.loads(data, encoding='utf-8')
                        setattr(record, col, data)
                    except Exception as e:
                        logging.warning(e)
                readData.append(record)
        else:
            logging.warning("db query failed ret=[%s] data=[%s] sql=[%s]" % (ret, data, sql))
        return endTime, readData

    def setCheckPoint(self, checkTime):
        self.properties.write(DbReader.UPDATE_KEY, checkTime)

#encoding: utf-8

"""add by guminli"""
import time
import os
import sys
import log
from DbReader import DbReader
from Dispatcher import Dispatcher


if __name__ == "__main__":

    # os.environ['debug'] = True
    if len(sys.argv) > 1:
        os.environ['limit'] = sys.argv[1]
        print "limit module %s" % os.environ['limit']
    else:
        print "usage: main.py processor\ncurrent available processor[SingleMail, ApiToLanjun, PushToHi]"
        sys.exit(-1)
    DB_CLUSTER = 'cae03'
    log.init_log("./log/cronjob")
    dbReader = DbReader()
    date, data = dbReader.dataReader();
    dispatcher = Dispatcher(data)
    dispatcher.process()
    dbReader.setCheckPoint(date);

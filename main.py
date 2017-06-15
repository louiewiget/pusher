#encoding: utf-8

"""add by guminli"""
import time
import os
import sys
import log
from DbReader import DbReader
from Dispatcher import Dispatcher


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        os.environ['debug'] = True
    DB_CLUSTER = 'cae03'
    log.init_log("./log/cronjob")
    dbReader = DbReader()
    date, data = dbReader.dataReader();
    dispatcher = Dispatcher(data)
    dispatcher.process()

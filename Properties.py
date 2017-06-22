#encoding: utf8

import ConfigParser
import os

import logging

class Properties(object):

    CONFIG_FILE = "conf/config.ini"


    def __init__(self):
        self.ct = ConfigParser.ConfigParser()
        if not os.path.exists(Properties.CONFIG_FILE):
            os.makedirs(Properties.CONFIG_FILE)
        self.ct.read(Properties.CONFIG_FILE)
        self.PROP_KEY = "properties_" + os.environ['limit']

    def write(self, key, value):
        try:
            if not self.ct.has_section(self.PROP_KEY):
                self.ct.add_section(self.PROP_KEY)
            self.ct.set(self.PROP_KEY, key, value)
            self.ct.write(open(Properties.CONFIG_FILE, "w"))
            return True
        except Exception as e:
            logging.warning(e)
        return False

    def read(self, key):
        try:
            if self.ct.has_section(self.PROP_KEY):
                return self.ct.get(self.PROP_KEY, key)
        except Exception as e:
            logging.warning(e)
        return None

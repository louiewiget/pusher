#encoing: utf-8

class RecordEntity(object):

    validation = {"content":"json", "config": "json", "type":"primitive"}

    def __init__(self):
        self.content = ''
        self.config  = ''
        self.type    = ''
        self.id = 0

    def getContent(self):
        return self.content

    def getConfig(self):
        return self.config

    def getType(self):
        return self.type

    def getId(self):
        return self.id

    def getVars(self):
        return vars(self).keys()

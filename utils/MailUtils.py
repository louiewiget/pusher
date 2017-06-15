#encoding: utf-8
import commands
import logging

def mail(to, fromuser, cc, subject, content):
    string = "echo \"%s\"| mail -s \"%s\" \"%s\" " % (content, subject, to)
    ret, data = commands.getstatusoutput(string)
    if ret == False:
        logging.warning("mail failed string[%s] ret[%s]" % (string, data))
    print data

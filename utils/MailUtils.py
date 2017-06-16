#encoding: utf-8
import commands
import logging
import MySQLdb

def mail(to, fromuser, cc, subject, content):
    string = "echo \"%s\"| mail -s \"`echo  \"%s\nContent-Type: text/html;charset=utf-8\"`\" \"%s\" " % (content, subject, to)
    ret, data = commands.getstatusoutput(string)
    with open("mail.html", "w") as f:
        f.write(content)
    if ret == False:
        logging.warning("mail failed string[%s] ret[%s]" % (string, data))
    print data

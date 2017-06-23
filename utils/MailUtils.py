#encoding: utf-8
import commands
import logging
import MySQLdb

def mail(to, fromuser, cc, subject, content):
    with open("mail.html", "w") as f:
        f.write(content)
        f.flush()
    string = "mail -s \"`echo  \"%s\nContent-Type: text/html;charset=utf-8\"`\"  \"%s\"  < mail.html" % (subject.replace("\"", "\'").replace("\n", ""), to)
    ret, data = commands.getstatusoutput(string)

    #if ret == False:
    #    logging.warning("mail failed string[%s] ret[%s]" % (string, data))
    #print data

#encoding: utf-8
import commands
import logging
import MySQLdb
import smtplib

def mail(to, fromuser, cc, subject, content):
    toUsers = to.split(",")
    message = """From: CAE-YQ <%s>
To: %s
Cc: %s
MIME-Version: 1.0
Content-type: text/html
Subject: %s

%s""" % (fromuser, to, cc, subject, content)
    with open("mail.html", "w") as f:
        f.write(message)
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(fromuser, toUsers, message)
        print "Successfully sent email"
    except Exception as e:
        print "Error: unable to send email[%s]" % e
    #if ret == False:
    #    logging.warning("mail failed string[%s] ret[%s]" % (string, data))
    #print data

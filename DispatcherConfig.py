#encoding: utf-8

DispatchMap = {}
DispatchMap[u"RISK邮件组"] = ['MailToRisk']
DispatchMap[u'公关部门']   = ['RegularToPR']

contentMap = {}
contentMap['NEWS'] = ["新闻=type", "标题=contents.0.title", "发布时间=contents.0.publish_time", "发布主体=contents.0.author"]
contentMap["ZHIHU"] = ["知乎=type", "标题=question_title", "发布时间=update_time"]
contentMap["WEIBO"] = ["微博=type", "标题=content", "发布时间=time", "发布主体=username"]

#encoding: utf-8

DispatchMap = {}
DispatchMap[u"RISK邮件组"] = ['MailToRisk']
DispatchMap[u'公关部门']   = ['RegularToPR']

contentMap = {}
contentMap['NEWS'] = ["新闻=type", "标题=contents.0.title", "发布时间=contents.0.publish_time", "发布主体=contents.0.author", "url=contents.0.url"]
contentMap["ZHIHU"] = ["知乎=type", "标题=question_title", "发布时间=update_time", "发布主体=random","url=url"]
contentMap["WEIBO"] = ["微博=type", "标题=content", "发布时间=time", "发布主体=username", "url=url"]
contentMap["TIEBA"] = ["贴吧=type", "标题=thread_title", "发布时间=thread_publish_time", "发布主体=thread_username", "url=url"]
contentMap["MANUAL"] = ["MANUAL=type", "标题=title", "发布时间=publish_time", "发布主体=publisher", "url=url"]

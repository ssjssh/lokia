#-*— coding:UTF-8 -*-
#/usr/bin/env python
"""
module descript
"""
import requests
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')

xml = """<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>"""
click_event = """<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[oydEOt2x7hH4zHQA8k2VVEqHK5jY]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[CLICK]]></Event>
<EventKey><![CDATA[order]]></EventKey>
</xml>"""
headers = {'Content-Type': 'application/xml'}
file = open("response.html", "w")
print >>file,requests.post('http://lokia.sinaapp.com/', data=xml, headers=headers).text
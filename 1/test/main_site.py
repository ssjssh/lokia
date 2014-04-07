#-*— coding:UTF-8 -*-
#/usr/bin/env python
"""
module descript
"""
import json
import requests
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')
post_data = {"openid": 11000}
customer_post_msg = {"openid": 11000,
                     "msg": "客服消息"}
file = open("webresponse.html", "w")
customer_msg = {
    "touser": "OPENID",
    "msgtype":"text",
    "text":
    {
         "content":"Hello World"
    }
}
print >>file,requests.post('http://lokia.sinaapp.com/get_customer_msg/',
                           data=customer_post_msg).text
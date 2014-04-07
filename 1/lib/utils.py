#-*— coding:UTF-8 -*-
#/usr/bin/env python
"""
module descript
"""
import json
import urllib
import urllib2
import logging
import time
from django.utils.encoding import smart_str
import xml.etree.ElementTree as ET


def parse_msg_xml(root_elem):
    msg = {}
    if root_elem.tag == 'xml':
        for child in root_elem:
            msg[child.tag] = smart_str(child.text)
    return msg


def parse_request(f):
    """
    一个修饰器，用来解析微信服务器传递的数据
    一般建议在一个view函数的最后使用这个修饰器
    因为可能有其他的修饰器对request进行解析
    """

    def wrapper(request, *args, **kwargs):
        raw_str = smart_str(request.body)
        msg = parse_msg_xml(ET.fromstring(raw_str))
        return f(msg, *args, **kwargs)

    return wrapper


def ensure_effective(f, effective_func, effective_time):
    if time.time() >= effective_time:
            effective_func()
    return f


def json_loads(data):
    return json.loads(data[:data.find("}")+1])






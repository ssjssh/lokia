#-*— coding:UTF-8 -*-
#/usr/bin/env python
import requests
from django.views.decorators import csrf
from django.conf import settings
from lib.utils import parse_request, json_loads
from lib.response import BaseResponse

"""
module descript
"""


@csrf.csrf_exempt
@parse_request
def about(msg):
    resp = BaseResponse(msg, "about.xml")
    return resp.get_response()


@csrf.csrf_exempt
@parse_request
def contact(msg):
    resp = BaseResponse(msg, "contact.xml")
    return resp.get_response()


@csrf.csrf_exempt
@parse_request
def order(msg):
    post_data = {"openid": msg['FromUserName']}
    is_binding = requests.post(settings.COMPANY_URL['bind']['IS_BINDING'],
                               data=post_data)
    is_binding = json_loads(is_binding.text)
    if is_binding['success']:
        order_json = json_loads(requests.post(settings.COMPANY_URL['bind']['ORDER_LIST'],
                                              data=post_data))
        context = {"Content": order_json}
        return BaseResponse(msg).get_response(context)
    else:
        context = {"openid": msg['FromUserName']}
        return BaseResponse(msg, "login_notify.xml").get_response(context)

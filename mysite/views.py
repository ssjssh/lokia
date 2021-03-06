#-*— coding:UTF-8 -*-
#/usr/bin/env python
"""
module descript
"""
import json
import hashlib
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators import csrf
from lib.utils import parse_request
from lib.response import BaseResponse
import menu
import requests
import token
import qrcode


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        result = menu.create_menu()
        return HttpResponse(result)


@csrf.csrf_exempt
def check_signature(request):
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echo_str = request.GET.get("echostr", None)
    tok = settings.APP_ACCESS['token']
    tmp_list = [tok, timestamp, nonce]
    tmp_list.sort()
    tmp_str = "%s%s%s" % tuple(tmp_list)
    tmp_str = hashlib.sha1(tmp_str).hexdigest()
    if tmp_str == signature:
        response = HttpResponse(echo_str, mimetype="text/plain")
        return response
    else:
        return HttpResponse(None, mimetype='text/plain')


@qrcode.ensure_ticket_effective
def qr_code(request):
    return HttpResponse(qrcode.get_qrcode(), mimetype="image/jpeg")


@csrf.csrf_exempt
@parse_request
def response_msg(msg):
    resp = BaseResponse(msg)
    if msg['Content'].strip().startswith('#'):
        msg_data = {'openid': msg['FromUserName'],
                    'msg': msg['Content']}
        requests.post(settings.COMPANY_URL['customer']['POST_TO_ADMIN'],
                      data=msg_data)
        context = {'Content': '客服消息已经发送，请稍后'}
    context = {'Content': '如果在消息前面加上#，那么我就可以回复客服消息'}
    return resp.get_response(context)


@csrf.csrf_exempt
@token.ensure_access_token_effective
def customer_msg(request):
    post_dict = request.POST
    resp = {'touser': post_dict['openid'], 'msg_type': 'text',
            'text': post_dict['response']}
    msg_params = {'access_token': token.ACCESS_TOKEN}
    requests.post(settings.COMPANY_URL['customer']['POST_TO_CUSTOMER'],
                  params=msg_params, data=json.dumps(resp))
    return HttpResponse("消息发出去了")


@csrf.csrf_exempt
def get_customer_msg(request):
    msg = request.POST['msg']
    resp_msg = {'openid': request.POST['openid'],
                "response": '你好你输入的消息是：'+msg}
    resp_data = requests.post('http://lokia.sinaapp.com/customer_msg/', data=resp_msg)
    return HttpResponse(resp_data.text)


def test(request):
    import requests
    return HttpResponse(requests.get("http://www.baidu.com").text)









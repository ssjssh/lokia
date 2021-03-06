#-*— coding:UTF-8 -*-
#/usr/bin/env python
import json

from django.conf import settings

import requests
import token

TICKET = None


@token.ensure_access_token_effective
def get_ticket():
    global TICKET
    ticket_params = {"access_token": token.ACCESS_TOKEN}
    resp = requests.post(settings.COMPANY_URL['qrcode']['GET_QR_CODE_TICKET_URL'],
                         params=ticket_params,
                         data=json.dumps(settings.GET_QR_CODE_TICKET_JSON))
    url = resp.url
    ticket_json = resp.json()
    TICKET = ticket_json["ticket"]
    return TICKET


def ensure_ticket_effective(f):
    if TICKET is None:
        get_ticket()
    return f


@ensure_ticket_effective
def get_qrcode():
    code_params = {"ticket": TICKET}
    qr_data = requests.get(settings.COMPANY_URL['qrcode']['GET_QR_CODE_URL'],
                           params=code_params)
    return qr_data.raw


#-*— coding:UTF-8 -*-
#/usr/bin/env python
"""
module descipt
"""
import urllib2
import json
import time
import datetime
from models import *

LASTEST_URL = 'http://news.at.zhihu.com/api/1.2/news/latest'
BEFORE_URL = 'http://news.at.zhihu.com/api/1.2/news/before/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}


def get_before_url(before):
    return BEFORE_URL + before


def split_date(date):
    """
    知乎的日期格式比较特殊，形式是类似20130213的形式
    返回值是一个time.struct_time类型
    """
    date_object = time.strptime(date, '%Y%m%d')
    return datetime.date(date_object.tm_year, date_object.tm_mon, date_object.tm_mday)


def __make_days(clean_data):
    days = Days(date=split_date(date=clean_data['date']), display_date=clean_data['display_date'],
                is_today=clean_data.get('is_today', False))
    return days


def __make_news(clean_data):
    new = New(id=clean_data['id'], image_source=clean_data['image_source'], title=clean_data['title'],
              url=clean_data['url'], image=clean_data['image'], share_url=clean_data['share_url'],
              ga_prefix=clean_data['ga_prefix'], share_image=clean_data['share_image'],
              thumbnail=clean_data.get('thumbnail', 'www.baidu.com'))
    return new


def config_today():
    today = datetime.date.today()


def __make_content(news_content):
    content = Content(body=news_content['body'])
    css_list = []
    for c in news_content['css']:
        css = Css(url=c, content=content)
        css_list.append(css)

    js_list = []
    for j in news_content['js']:
        js = Js(url=j, content=content)
        js_list.append(js)
    return content, css_list, js_list


def hibernate(day):
    if day == 'today':
        config_today()
        url = LASTEST_URL
    else:
        url = get_before_url(day)
    json_data = download(url)
    clean_data = json.loads(json_data, encoding="UTF8")
    day = __make_days(clean_data)
    day.save()
    news_data = clean_data['news']
    news_list = []
    for news_dict in news_data:
        if New.objects.filter(pk=news_dict['id']).exists():
            continue
        n = __make_news(news_dict)
        n.days = day
        news_content = json.loads(download(n.url), encoding="UTF8")
        content, css_list, js_list = __make_content(news_content)
        content.save()
        n.content = content
        Css.objects.bulk_create(css_list)
        Js.objects.bulk_create(js_list)
        news_list.append(n)
    New.objects.bulk_create(news_list)


def download(url):
    req = urllib2.Request(url=url, headers=HEADERS)
    read_data = urllib2.urlopen(req).read()
    return read_data


if __name__ == '__main__':
    hibernate('today')


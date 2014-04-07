#-*— coding:UTF-8 -*-
#/usr/bin/env python
"""
module descipt
"""
from django.db import models


class Days(models.Model):
    date = models.DateTimeField(primary_key=True)
    display_date = models.CharField(max_length=200)
    is_today = models.BooleanField()


class New(models.Model):
    id = models.IntegerField(primary_key=True)
    image_source = models.CharField(max_length=200)
    title = models.TextField()
    url = models.URLField()
    image = models.URLField(max_length=1000)
    share_url = models.URLField()
    thumbnail = models.URLField(max_length=1000, blank=True)
    ga_prefix = models.IntegerField()
    share_image = models.URLField(max_length=1000)
    content = models.OneToOneField('Content')
    days = models.ForeignKey(Days)


class Content(models.Model):
    body = models.TextField()


class Js(models.Model):
    url = models.CharField(max_length=200)
    content = models.ForeignKey(Content)


class Css(models.Model):
    url = models.CharField(max_length=200)
    content = models.ForeignKey(Content)

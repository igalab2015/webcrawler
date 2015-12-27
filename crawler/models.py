# -*- coding: utf-8 -*

from django.db import models

class Url_list(models.Model):

    #id = models.IntegerField(u'ID', blank=True, default=0)
    url = models.URLField(u'URL', unique=True, null=False, max_length=255)
    title = models.CharField(u'タイトル',max_length=255, blank=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.url

class Crawled_url_list(models.Model):
    url = models.URLField('URL', unique=True, null=False,max_length=255)
    title = models.CharField("Title", max_length=255, blank=True)

    def __str__(self):
        return self.url

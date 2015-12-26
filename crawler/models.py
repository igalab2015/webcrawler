# -*- coding: utf-8 -*

from django.db import models

class Url_list(models.Model):

    #id = models.IntegerField(u'ID', blank=True, default=0)
    url = models.CharField(u'URL', max_length=255)
    title = models.CharField(u'タイトル', unique=True, max_length=255, blank=True)
    timestamp = models.CharField(u'最終更新日', max_length=255)

    def __str__(self):
        return self.url

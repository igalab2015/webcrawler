# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from crawler.views import UrlListView

urlpatterns = [
    # URL
    url(r'^index/$', UrlListView.as_view(), name='index'),   # 一覧

]

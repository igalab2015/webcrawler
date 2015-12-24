# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from crawler import views

urlpatterns = [
    # URL
    url(r'^index/$', views.urls_list, name='index'),   # 一覧

]

from django.contrib import admin

# -*- coding: utf-8 -*-
from django.contrib import admin
from crawler.models import Url_list

class UrlAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'title')
    list_display_links = ('url', 'title')
admin.site.register(Url_list,UrlAdmin)
#admin.site.register(Url_list)

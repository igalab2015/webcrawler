from django.contrib import admin

from django.contrib import admin
from crawler.models import Url_list,Crawled_url_list,Dictionary_about_security

class UrlAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'title')
    list_display_links = ('url', 'title')
admin.site.register(Url_list,UrlAdmin)
admin.site.register(Crawled_url_list)
admin.site.register(Dictionary_about_security)

#admin.site.register(Url_list)

#from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from crawler.models import Url_list

# from crawler.crawl import Crawler



def urls_list(request):
    # '''urlの一覧'''
    # hatena = Crawler()
    # max_depth = 1
    # target_url = "http://b.hatena.ne.jp/search/text?q=%E3%82%BB%E3%82%AD%E3%83%A5%E3%83%AA%E3%83%86%E3%82%A3"
    # hatena.crawl(target_url, max_depth)

    #index = hatena.get_titles_and_urls()
    # hatena.get_titles_and_urls()
    #return HttpResponse(u'URLの一覧')


    index = Url_list.objects.all().order_by('id')
    return render_to_response('index.html',  # 使用するテンプレート
                              {'index': index},       # テンプレートに渡すデータ
                              context_instance=RequestContext(request))  # その他標準のコンテキスト

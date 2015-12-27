# -*- coding: utf-8 -*-
from celery.task import task
import urllib.request
from bs4 import BeautifulSoup
from crawler.models import Url_list, Crawled_url_list
import re

class Crawler(object):

    words_about_security = ['マルウェア']

    def __init__(self, target_url, max_depth):
        super(Crawler, self).__init__()
        self.target_url = target_url
        self.max_depth = max_depth
        self.data_number = 0
        self.patterns = [re.compile(word) for word in words_about_security]

    def jubge_url(self, url):
        if url[0:4] == 'http' and url[-5:] == '.html':
            return True
        else:
            return False

    def get_all(self, page):
        links = []
        try:
            f = urllib.request.urlopen(page)
        except:
            return links
        soup = BeautifulSoup(f, "html.parser")
        title = soup.title.string
        if title:
            self.set_crawled_urls_and_titles(title, page)
        else:
            return []
        for atag in soup.find_all('a'):
            link = atag.get('href')
            if not link:
                continue
            if self.jubge_url(link):
                links.append(link)
        return links

    def set_crawled_urls_and_titles(self, title, page):
        crawled_data = Crawled_url_list()
        crawled_data.url = page
        crawled_data.title = title
        try:
            crawled_data.save()
            self.data_number += 1
            # print("successfully setting data" + self.data_number)
        except:
            # print("error !!")
            pass

    def crawl(self, url, max_depth):
        crawled = []
        tocrawl = [url]
        next_depth = []
        depth = 0
        while tocrawl and depth <= max_depth:
            page = tocrawl.pop()
            if page not in crawled:
                next_depth = list(set(next_depth).union(set(self.get_all(page))))
                crawled.append(page)
            if not tocrawl:
                tocrawl = next_depth
                next_depth = {}
                # print("depth " + (depth - 1) + " finished")
                depth += 1

    def select_by_title(self, title):
        for reg in self.patterns:
            if reg.search(title):
                return True
        else:
            return False

    def get_titles_from_urls(self, urls):
        titles_and_urls = []
        for url in urls:
            title = get_title(url)
            titles_and_urls.append((title, url))
            time.sleep(2)
        return titles_and_urls

    def set_titles_and_urls_to_show(self, title):
        for pair in Crawled_url_list.objects.all():
           ut = Url_list()
           if pair.title:
               if self.select_by_title(pair.title):
                  ut.url = pair.url
                  ut.title = pair.title
                  try:
                      ut.save()
                  except:
                      # print("Error occured while saving selected data")
                      pass
           else:
               next


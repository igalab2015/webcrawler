from __future__ import absolute_import
from urllib.parse import urlparse
from webcrawler.celery import app
from celery.task import task
import urllib.request
from bs4 import BeautifulSoup
from crawler.models import Url_list, Crawled_url_list
from celery.schedules import crontab
import hashlib
import re

class Crawler(object):

    words_about_security = []

    def __init__(self, target_url, max_depth):
        super(Crawler, self).__init__()
        self.target_url = target_url
        self.max_depth = max_depth
        # self.data_number = 0
        self.setup_dictionary()
        self.patterns = [re.compile(word) for word in self.words_about_security]

    def crawl(self):
        crawled = []
        tocrawl = [self.target_url]
        next_depth = []
        depth = 0
        while tocrawl and depth <= self.max_depth:
            page = tocrawl.pop()
            if page not in crawled:
                next_depth = list(set(next_depth).union(set(self.scrape(page))))
                crawled.append(page)
            if not tocrawl:
                tocrawl = next_depth
                next_depth = {}
                # print("depth " + str(depth) + " finished")
                depth += 1

    def scrape(self, page_url):
        try:
            page = urllib.request.urlopen(page_url)
        except:
            return []

        digest = hashlib.sha1(page.read()).hexdigest()
        crawled_url_data = Crawled_url_list.objects.all().filter(url=page_url)
        if crawled_url_data:
            data = crawled_url_data[0]
            if data.html_digest == digest:
                print('HTML digest equals previous crawling')
                return []
            else:
                self.update_digest(data, digest)
                print('Digest updated')

        soup = BeautifulSoup(page, "html.parser")
        if soup.title:
            title = soup.title.string
        else:
            return []

        # last_modified = page.info()['Last-Modified'] 
        # if self.set_crawled_urls_and_titles_and_lastmodified(page_url, title, last_modified):

        if self.set_crawled_urls_and_titles_and_lastmodified(page_url, title, digest):
            return self.get_all_link(soup, page_url)
        else:
            return []

    def update_digest(self, data, digest):
        data.html_digest = digest
        try:
            data.save()
        except:
            pass
        
    # def set_crawled_urls_and_titles_and_lastmodified(self, page_url, title, last_modified):
    def set_crawled_urls_and_titles_and_lastmodified(self, page_url, title, digest):
        if title:
            crawled_data = Crawled_url_list()
            crawled_data.url = page_url
            crawled_data.title = title
            crawled_data.html_digest = digest
            
            # if last_modified:
            #     crawled_data.last_modified = last_modified
            #     print('Successfully get last modified info')
            # else:
            #     print('failed getting last modified')
            try:
                crawled_data.save()
            except:
                pass
            return True
        else:
            return False

    def get_all_link(self, soup, current_url):
        links = []
        for atag in soup.find_all('a'):
            link = atag.get('href')
            if not link:
                continue
            links.append(self.get_absolute_path(current_url, link))
        return links

    def get_absolute_path(self, current_url, link):
        parsed_link = urlparse(link)
        if parsed_link.scheme:
            return link   
        else:
            if current_url[-1] == '/':
                current_url = current_url[:-1]
            return current_url + parsed_link.path

    def jubge_url(self, url):
        if url[0:4] == 'http' and url[-5:] == '.html':
            return True
        else:
            return False

    def set_titles_and_urls_to_show(self):
        for pair in Crawled_url_list.objects.all():
            if pair.title:
                if Url_list.objects.all().filter(url=pair.url):
                    pass
                elif self.select_by_title(pair.title):
                    ut = Url_list()
                    ut.url = pair.url
                    ut.title = pair.title
                    ut.save()

    def select_by_title(self, title):
        for reg in self.patterns:
            if reg.search(title):
                return True
        else:
            return False

    def setup_dictionary(self):
        dict_url = 'http://e-words.jp/p/t-Security.html'
        try:
            page = urllib.request.urlopen(dict_url)
        except:
            pass
        soup = BeautifulSoup(page, "html.parser")
        for atag in soup.find_all('a'):
            word = atag.string
            if word:
                self.words_about_security.append(word)

class JVN(Crawler):
    def __init__(self):
        self.target_url = 'https://jvn.jp/'
        self.max_depth = 1

@app.task
def run_crawler():
    max_depth = 1
    target_url = "http://b.hatena.ne.jp/search/text?q=%E3%82%BB%E3%82%AD%E3%83%A5%E3%83%AA%E3%83%86%E3%82%A3"
    # target_url = "http://japan.zdnet.com/"
    hatena = Crawler(target_url, max_depth)
    print('crawl start')
    hatena.crawl()
    hatena.set_titles_and_urls_to_show()
    print('crawl finished')


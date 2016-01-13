from __future__ import absolute_import
from urllib.parse import urlparse
from webcrawler.celery import app
from celery.task import task
import urllib.request
from bs4 import BeautifulSoup
from crawler.models import Url_list, Crawled_url_list, Dictionary_about_security
from celery.schedules import crontab
import hashlib
import re
from datetime import datetime 
from socket import timeout 

# for print debug
MYDEBUG = True
# for log file debug
MYLOG = True

class Crawler(object):

    def __init__(self, target_url, max_depth):
        # target url is seed's url
        self.target_url = target_url
        self.max_depth = max_depth

    def dictionary_from_database(self):
        # create dictionary of words about security using Dictionary_about_security
        words = []
        for data in Dictionary_about_security.objects.all():
            words.append(data.word)
        return words

    def crawl(self):
        # create regular expression list from dictionary
        self.patterns = [re.compile(word) for word in self.dictionary_from_database()]
        crawled = [] # crawled url list
        tocrawl = [self.target_url] # to crawl list
        next_depth = [] # to crawl next echelon
        depth = 0 # current depth
        while tocrawl and depth <= self.max_depth:
            page = tocrawl.pop()
            # if page is not checked yet, crawl it
            if page not in crawled:
                # set list to crawl at next depth
                # remove overlapped elements 
                # scrape page
                next_depth = list(set(next_depth).union(set(self.scrape(page))))
                crawled.append(page)
            if not tocrawl:
                tocrawl = next_depth
                next_depth = []
                depth += 1

    # scrape html
    def scrape(self, page_url):
        try:
            page = urllib.request.urlopen(page_url, timeout=10)
        except timeout:
            print('socket timed out - URL %s', page_url)
        else:
            return []

        page_html = page.read()

        # calculate hash of page's html
        digest = hashlib.sha1(page_html).hexdigest()
        crawled_url_data = Crawled_url_list.objects.all().filter(url=page_url)

        # don't check this page if html digest equals that crawled
        if crawled_url_data:
            data = crawled_url_data[0]
            if data.html_digest == digest:
                if MYLOG:
                    self.write_log(' ', page_url + ' skipped')
                return []
            else:
                self.update_digest(data, digest)
                if MYLOG:
                    self.write_log('', page_url + ' Digest updated')

        # create soup object and confirm whether title exists or not
        soup = BeautifulSoup(page_html, "html.parser")
        if soup.title:
            title = soup.title.string
        else:
            # if MYDEBUG:
            #     print('there isn\'t title')
            return []

        # save data and return all link
        if self.set_crawled_urls_and_titles_and_digest(page_url, title, digest):
            return self.get_all_link(soup, page_url)
        else:
            return []

    def update_digest(self, data, digest):
        data.html_digest = digest
        try:
            data.save()
        except:
            pass
    
    def set_crawled_urls_and_titles_and_digest(self, page_url, title, digest):
        if title:
            crawled_data = Crawled_url_list()
            crawled_data.url = page_url
            crawled_data.title = title
            crawled_data.html_digest = digest
            try:
                crawled_data.save()
                if MYLOG:
                    self.write_log('', page_url + ' saved')
            except:
                pass
            return True
        else:
            return False

    # collect all <a> tag
    def get_all_link(self, soup, current_url):
        links = []
        for atag in soup.find_all('a'):
            link = atag.get('href')
            if not link:
                continue
            abs_path = self.get_absolute_path(current_url, link)
            links.append(self.remove_trailing_slash(abs_path))
        return links

    def remove_trailing_slash(self, url):
        if url[-1] == '/':
            return url[0:-1]
        else:
            return url

    # make relative path absolute path
    def get_absolute_path(self, current_url, link):
        parsed_link = urlparse(link)
        if parsed_link.scheme:
            return link 
        else:
            if current_url[-1] == '/':
                current_url = current_url[:-1]
            return current_url + parsed_link.path

    # only set titles and urls about security
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
        black_word = ['はてなブックマーク'] 
        patterns_for_excluding = [re.compile(word) for word in black_word]

        for reg_black in patterns_for_excluding:
            if reg_black.search(title):
                return False
        for reg_white in self.patterns:
            if reg_white.search(title):
                return True
        else:
            return False

    # save log into crawler.log
    def write_log(self, mark, log_text):
        with open('crawler.log','a') as log:
            log.write(mark + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ': ' + log_text + '\n')
        log.close()

class Dictionary(object):
    black_list_of_words = ['Incept Inc.', '記号・数字']
    def __init__(self, url):
        self.dict_url = url

    def update_dictionary(self):
        try:
            page = urllib.request.urlopen(self.dict_url)
        except:
            if MYDEBUG:
                print('can\'t open '+ self.dict_url)
            return
        soup = BeautifulSoup(page, "html.parser")
        for atag in soup.find_all('a'):
            word = atag.string
            if word:
                if word in self.black_list_of_words:
                    continue
                try:
                    ut = Dictionary_about_security()
                    ut.word = word
                    ut.save()
                except:
                    pass

@app.task
def run_crawler():
    seed_sites_url = ['http://b.hatena.ne.jp/search/text?q=%E3%82%BB%E3%82%AD%E3%83%A5%E3%83%AA%E3%83%86%E3%82%A3', 'http://japan.zdnet.com', 'https://jvn.jp/']
    max_depth = 2
    if MYDEBUG:
        print('crawl start')
    for seed in seed_sites_url:
        if MYDEBUG:
            print(seed)
        crawler = Crawler(seed, max_depth)
        crawler.crawl()
        crawler.set_titles_and_urls_to_show()
        if MYDEBUG:
            print(seed)
    crawler.write_log('--- ', 'crawl finished\n')
    if MYDEBUG:
        print('crawl finished')

# update dictionary about security
@app.task
def update_dictionary():
    dict_url = 'http://e-words.jp/p/t-Security.html'
    ewords_dictionary = Dictionary(dict_url)
    print('updating dictionary start')
    ewords_dictionary.update_dictionary()
    print('updating dictionary finished')


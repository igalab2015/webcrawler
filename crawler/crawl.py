import urllib.request
from bs4 import BeautifulSoup
from crawler.models import Url_list, Crawled_url_list
# from crawler.models import Crawled_url_list
import re
from threading import Thread
import time

class Crawler(Thread):

    # titles_and_urls = []
    words_about_security = ['マルウェア']
    patterns = [re.compile(word) for word in words_about_security]

    def __init__(self, target_url, max_depth):
        super(Crawler, self).__init__()
        self.target_url = target_url
        self.max_depth = max_depth

    def run(self):
        while True:
            self.crawl(self.target_url, self.max_depth)
            self.get_titles_and_urls()
            time.sleep(10)

    def remove_overlapped_titles_and_urls(self):
        self.titles_and_urls = list(set(self.titles_and_urls))

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
        # self.titles_and_urls.append((soup.title.string, page))
        self.set_crawled_urls_and_titles(soup.title.string, page)
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
        except:
            print("error while saving data")

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
                depth += 1
        self.remove_overlapped_titles_and_urls()

    def select_by_title(self, title):
        for reg in self.patterns:
            if reg.search(title):
                return True
        else:
            return False

    def get_titles_and_urls(self):
        print("crawl finish")
        for i in self.titles_and_urls:
           ut = Url_list()
           if i[0]:
              if self.select_by_title(i[0]):
                  ut.url = i[1]
                  ut.title = i[0]
                  try:
                      ut.save()
                  except:
                      print("error")
           else:
               next
        return f

    def set_into_database(self):
        to_save = []
        for i in self.titles_and_urls:
            pass

    # def get_title(self, page_url):
    #     try:
    #         f = urllib.request.urlopen(page_url)
    #     except:
    #         return "No text"
    #     soup = BeautifulSoup(f, "html.parser")
    #     return soup.title.string
    #
    # def get_titles_from_urls(self, urls):
    #     titles_and_urls = []
    #     for url in urls:
    #         title = get_title(url)
    #         titles_and_urls.append((title, url))
    #     return titles_and_urls


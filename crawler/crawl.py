import urllib.request
from bs4 import BeautifulSoup
from crawler.models import Url_list
import re
from threading import Thread
import time

class Crawler(Thread):

    titles_and_urls = []
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
        self.titles_and_urls.append((soup.title.string, page))
        for atag in soup.find_all('a'):
            link = atag.get('href')
            if not link:
                continue
            if self.jubge_url(link):
                links.append(link)
        return links

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
        # return crawled

    def get_title(self, page_url):
        try:
            f = urllib.request.urlopen(page_url)
        except:
            return "No text"
        soup = BeautifulSoup(f, "html.parser")
        return soup.title.string

    def get_titles_from_urls(self, urls):
        titles_and_urls = []
        for url in urls:
            title = get_title(url)
            titles_and_urls.append((title, url))
        return titles_and_urls

#    def show(self):
#        for i in self.titles_and_urls:
#            if i[0] :
#                print(i[0][:5] +" : "+ i[1])
#            else:
#                print(i[1])
#                print("")

    def select_by_title(self, title):
        for reg in self.patterns:
            if reg.search(title):
                return True
        else:
            return False
           
    def get_titles_and_urls(self):
        f = []
        for i in self.titles_and_urls:
           ut = Url_list()
           if i[0]:
              if self.select_by_title(i[0]):
                  ut.url = i[1]
                  ut.title = i[0]
                  f.append((i[0],i[1]))
                  ut.save()
           else:
               ut.url = i[1]
               ut.title = ""
               f.append(("unkown",i[1]))
               ut.save()
        return f

#hatena = Crawler()
#max_depth = 2
#target_url = "http://b.hatena.ne.jp/search/text?q=%E3%82%BB%E3%82%AD%E3%83%A5%E3%83%AA%E3%83%86%E3%82%A3"
# url_list = list(set(hatena.crawl(target_url, max_depth)))
# title_url_set = get_titles_from_urls(url_list)
# for i in title_url_set:
#     if i[0] :
#         print(i[0][:5] +" : "+ i[1])
#     else:
#         print("")
#         print(i[1])
#         print("")
#hatena.crawl(target_url, max_depth)
#hatena.show()

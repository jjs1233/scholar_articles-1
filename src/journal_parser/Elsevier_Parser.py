# coding:utf-8
"""
@file:      Elsevier_Parser.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-09-06 12:16
@description:
            用于解析elsevier出版社的文章详情页
            域名：http://www.sciencedirect.com/science/article/pii/xxxx
"""
import sys,os
up_level_N = 1
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
root_dir = SCRIPT_DIR
for i in range(up_level_N):
    root_dir = os.path.normpath(os.path.join(root_dir, '..'))
sys.path.append(root_dir)
from journal_parser.JournalArticle import JournalArticle
from crawl_tools.request_with_proxy import request_with_random_ua
from bs4 import BeautifulSoup
import re

class ElsevierDetailPageParser:
    def __init__(self, article_page_url, driver):
        driver.get(article_page_url)
        if 'sciencedirect' not in article_page_url:
            raise Exception(
                '[Error] in Elsevier_Parser:\n\tUrl pattern is wrong.')
        self.soup = BeautifulSoup(driver.page_source, 'lxml')
        self.__keywords = ''

    @property
    def pdf_url(self):
        try:
            link = self.soup.select_one("#pdfLink")['href']
            if 'ShoppingCartURL' in link:
                # 被指向支付 页面，不是在学校ip里的情况
                return None
            else:
                return link
        except Exception as e:
            print('[Error] in Elsevier_Parser.pdf_url():{}'.format(str(e)))
            #print('The url of issue is:{}\n'.format(link))
            return None

    @property
    def keywords(self):
        keywords_locate = None
        try:
            keywords_locate = self.soup.find_all(class_='keyword')
            for i in keywords_locate:
                self.__keywords = self.__keywords + \
                    '{}, '.format(i.get_text().replace(';', ', '))
        except:
            pass
        if self.__keywords:
            return self.__keywords, 'Acquired'
        else:
            return None, 'Keywords not found'


class ElsevierAllItemsPageParser:
    '''
        sample_url: http://www.sciencedirect.com/science/journal/15708268
    '''
    def __init__(self,html_source):
        self.soup = BeautifulSoup(html_source,'lxml')
        self.nav = self.soup.select_one('#volumeIssueData')

    @property
    def sections(self):
        return self.soup.select_one('.articleList').select('.detail')

    @property
    def volume_year(self):
        try:
            return int(self.soup.select_one('.volumeHeader').find(re.compile("h[0-9]"))\
                .text.strip().split(' ')[-1][:-1])
        except:
            return int(self.soup.select_one('.volumeHeader').find(re.compile("h[0-9]"))\
                .text.strip().split(' ')[-1][1:5])

    @property
    def volume_area_links(self):
        volume_a_tags = self.nav.select('.volLink')
        return list(map(lambda x:'http://www.sciencedirect.com'+x['href'],volume_a_tags))

    @property
    def volume_divs(self):
        return self.nav.select('.currentVolumes')[1:]

    @property
    def volume_links(self):
        return list(map(lambda x:'http://www.sciencedirect.com'+x.select_one('a')['href'],self.volume_divs))


class ElsevierAricle(JournalArticle):
    def __init__(self,sec,JournalObj,volume_db_id,year):
        self.sec = sec
        self.JournalObj = JournalObj
        JournalArticle.__init__(self,JournalObj,volume_db_id)
        self.generate_all_method()
        self.year = year
        bad_type_keywords = ['Editor']
        for bad_type_keyword in bad_type_keywords:
            if bad_type_keyword in self.title:
                raise Exception('Elsevier Article Type Error')

    @property
    def origin_title(self):
        return self.sec.select_one('.title').text

    @property
    def type(self):
        if 'Original Research Article' in self.origin_title:
            return 'Original Research Article'
        if 'Review Article' in self.origin_title:
            return 'Review Article'
        return None

    @property
    def abstract_url(self):
        return self.sec.select_one('.absLink')['data-url']

    def generate_title(self):
        tit = self.origin_title
        if self.type:
            tit = tit[:-len(self.type)]
        self.title = tit

    def generate_abstract(self):
        #访问abstract_url直接生成
        try:
            resp = request_with_random_ua(self.abstract_url)
            self.abstract = BeautifulSoup(resp.text,'lxml').select_one('.paraText').text.strip()
        except Exception as e:
            pass
            # print('[ERROR] in Elsevier Parser:abstract():\n{}'.format(str(e)))

    def generate_pdf_url(self):
        try:
            url = self.sec.select_one('.extLinkBlock').select_one('.cLink')['href']
        except:
            return
        if '.pdf' in url:
            self.pdf_url = url
        else:
            print('[ERROR] in Elsevier Parser:pdf_url()')

    def generate_authors(self):
        self.authors = self.sec.select_one('.authors').text.split(',')

    def generate_link(self):
        self.link = self.sec.select_one('.title').find('a')['href']

    def generate_id_by_journal(self):
        self.generate_link()
        self.id_by_journal = self.link.split('/')[-1]


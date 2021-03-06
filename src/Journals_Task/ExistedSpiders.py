#coding:utf-8
"""
@file:      ExistedSpiders.py
@author:    lyn
@contact:   tonylu716@gmail.com
@python:    3.3
@editor:    PyCharm
@create:    2016-09-18 0:51
@description:
            存放已经写好的publisher爬虫包指向以及配置
"""
import sys,os
up_level_N = 1
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
root_dir = SCRIPT_DIR
for i in range(up_level_N):
    root_dir = os.path.normpath(os.path.join(root_dir, '..'))
sys.path.append(root_dir)


from Journals_Task.ElsevierSpider import ElsevierSpider
from Journals_Task.SpringSpider import SpringSpider
from Journals_Task.IEEE_Spider import IEEE_Spider
from Journals_Task.TaylorFrancisSpider import TaylorFrancisSpider
from Journals_Task.SageSpider import SageSpider
from Journals_Task.BiomedSpider import BioMedSpider
from Journals_Task.WileySpider import WileySpider
from Journals_Task.AcsSpider import AcsSpider
from Journals_Task.EmeraldSpider import EmeraldSpider
from Journals_Task.LwwSpider import LwwSpider

EXISTED_SPIDERS = [
    {
       'publisherSpiderClass': LwwSpider,
       'publisherKeywords':    ['lww.com'],
       'need_webdriver':       False
    },
    {
       'publisherSpiderClass': EmeraldSpider,
       'publisherKeywords':    ['emeraldgroup'],
       'need_webdriver':       False
    },
    {
       'publisherSpiderClass': AcsSpider,
       'publisherKeywords':    ['pubs.acs'],
       'need_webdriver':       False
    },
    {
       'publisherSpiderClass': WileySpider,
       'publisherKeywords':    ['interscience.wiley'],
       'need_webdriver':       False
    },
    {
       'publisherSpiderClass': SageSpider,
       'publisherKeywords':    ['sagepub'],
       'need_webdriver':       False
    },
    {
        'publisherSpiderClass': ElsevierSpider,
        'publisherKeywords':    ['http://www.elsevier.com','sciencedirect'],
        'need_webdriver':       False
    },
    {
        'publisherSpiderClass': SpringSpider,
        'publisherKeywords':    ['springer'],
        'need_webdriver':       False
    },
    {
        'publisherSpiderClass': TaylorFrancisSpider,
        'publisherKeywords':    ['informa'],
        'need_webdriver':       False
    },
    {
       'publisherSpiderClass': IEEE_Spider,
       'publisherKeywords':    ['ieee'],
       'need_webdriver':       False
    },
    {
       'publisherSpiderClass': BioMedSpider,
       'publisherKeywords':    ['biomedcen'],
       'need_webdriver':       False
    }
]



# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from lxml import etree
import gzip

import g_spi.utils.extractor as extractor


class ComHexunStockSpider(scrapy.Spider):

    name = "com.hexun.stock"

    allowed_domains = ["stock.hexun.com"]

    def start_requests(self):
        self.headers = {}
        self.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        self.headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
        self.headers['Cache-Control'] = 'max-age=0'
        self.headers['Connection'] = 'keep-alive'
        self.headers['Cookie'] = 'hxck_cd_sourceteacher=sR%2FuPcnSSZVIdShwHag3RAnrY9aauRbMjEnRBtq%2FNF1ooDP7obDVPgaQGWxsj76JqbJObjTyc6EwzrRgKn4VQV8Ac1ErFNBPOrblgb8RPFofY9ayaQea1C5xVn2qzLjIB1OERw5znx0DmQLYsU2gdRCM%2BsLugChikdOAcD6RTyzkMfZoAH3MOA%3D%3D; UM_distinctid=18861b8b39c96-0e11e177c3603b-17462c6c-384000-18861b8b39d11e9; Hm_lvt_cb1b8b99a89c43761f616e8565c9107f=1685266675; HexunTrack=SID=202305281738351464a48cfad64b74a86a4b39b8a3471bb64&CITY=0&TOWN=0; cn_1263247791_dplus=%7B%22distinct_id%22%3A%20%2218861b8b39c96-0e11e177c3603b-17462c6c-384000-18861b8b39d11e9%22%2C%22userFirstDate%22%3A%20%2220230528%22%2C%22%24_sessionid%22%3A%201%2C%22%24_sessionTime%22%3A%201685273401%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201685273401%2C%22initial_view_time%22%3A%20%221685265597%22%2C%22initial_referrer%22%3A%20%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DuSdw0Xxb56IdwtdGIC3x7sP1Zj9O3cbS-L-q1Ku_COvkRyyfFZLn87CxPy_L51AprNPJj2GLI6chUqlVomlEsK%26wd%3D%26eqid%3Df162b4dd003699db0000000264732110%22%2C%22initial_referrer_domain%22%3A%20%22www.baidu.com%22%2C%22%24recent_outside_referrer%22%3A%20%22192.168.1.152%22%2C%22userID%22%3A%20%220%22%2C%22userName%22%3A%20%22%22%2C%22userType%22%3A%20%22loginuser%22%2C%22userLoginDate%22%3A%20%2220230528%22%7D; hexun_popuped=2023-05-28; ADHOC_MEMBERSHIP_CLIENT_ID1.0=a100e932-febd-a5b8-c3dd-fff2bd2f759b; hxck_cd_channel_order_mark1=tKK6EMkJ7JK75WOJ%2FqluxbbMrhZQZtn9if6%2FTggkwv05ylPHXG7FciRVPZ0YEg7nHogOP%2BXj2QflBegnErZ5qZy6d4qRY2L%2Fzwq7g3P083wsgx0rHVrVyQkjSpbjyUZn; Hm_lpvt_cb1b8b99a89c43761f616e8565c9107f=1685273417'
        self.headers['Upgrade-Insecure-Requests'] = '1'
        self.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

        self.encoding = "GBK"

        self.seed = 'http://stock.hexun.com/hkstock/'
        yield Request(url=self.seed, headers=self.headers)


    def parse(self, response):

        html = response.body.decode(self.encoding)
        dom = etree.HTML(html)

        x = "//a[@class='newtit']"
        links = extractor.list_link_anchor(dom, x, response.request.url)
        if links:
            for href, anchor in links:
                self.logger.info(f"outlinks: {href}, {anchor}")
                meta = response.request.meta
                meta['anchor'] = anchor
                meta['outlink'] = href
                yield Request(url=href, callback=self.parse_detail, headers=self.headers, meta=meta)

    def parse_detail(self, response):

        #html = response.body.decode(self.encoding)
        #dom = etree.HTML(html)
        #x = '//h1/text()'
        #title = extractor.get_text(dom, x)
        #self.logger.info(f"parse_detail: title: {title}")

        #x = "//span[@class='pr20']/text()"
        #pubtime = extractor.get_text(dom, x)
        #self.logger.info(f"parse_detail: publish time: {pubtime}")

        #x = "//div[@class='art_contextBox']//text()"
        #article = extractor.get_text(dom, x) 
        #self.logger.info(f"parse_detail: article: {article[:10]}")

        meta = response.meta

        item = {}
        item['anchor'] = meta['anchor']
        item['url'] =  meta['outlink']
        #item['title'] = title
        #item['pubtime'] = pubtime
        #item['article'] = article
        item['html'] = gzip.compress(response.body)
        item['encoding'] = self.encoding

        dic = {}

        dic['_db'] = 'dim_news'
        dic['_col'] = 'finance'
        dic['_item'] = item

        yield dic









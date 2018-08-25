# -*- coding: utf-8 -*-
import scrapy
import re
import json
from jdpinglun.items import JdpinglunItem



class Jd11Spider(scrapy.Spider):
    name = 'jd11'
    allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']

    url = 'https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%94%B5%E8%84%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.V16&wq=bijiben&psort=3&click=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url,callback=self.parse_product,dont_filter=True)

    def parse_product(self,response):
        productIds = response.css('#J_goodsList .gl-warp li::attr(data-sku)').extract()
        productIds = list(set(productIds))
        # print(productIds)
        # productIds = ['7512626']
        for productId in productIds:
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv14437&productId='+productId+'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=url,callback=self.parse_page,dont_filter=True)


    def parse_page(self,response):
        pattern = re.compile('"maxPage":(\d+)',re.S)
        page = int(re.search(pattern,response.text).group(1))
        for ye in range(page):
            productId = re.search('&productId=(.*?)&',response.url).group(1)
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv14437&productId='+productId+'&score=0&sortType=5&page='+str(ye)+'&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=url,callback=self.parse_info,dont_filter=True)


    def parse_info(self,response):
        # print(response.text)
        html = response.text.replace('fetchJSON_comment98vv14437(','')
        html = html.replace(');','')
        product = json.loads(html)
        comments = product['comments']
        for comment in comments:
            item = JdpinglunItem()
            item['content'] = comment['content']
            item['referenceName'] = comment['referenceName']
            item['id'] = comment['id']
            yield item




    def parse(self, response):
        pass

# -*- coding: utf-8 -*-
import scrapy
import os
from sinaSpider.items import SinaspiderItem


class SinanewspiderSpider(scrapy.Spider):
    name = 'sinaNewSpider'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        # 父目录名
        parentNames = response.xpath('//div[@class="article"]//h3/a/text()').extract()
        # 父目录对应的url
        parentUrls = response.xpath('//div[@class="article"]//h3/a/@href').extract()
        # 子目录名
        chlidNames = response.xpath('//div[@class="article"]//ul/li/a/text()').extract()
        # 子目录对应的url
        chlidUrls = response.xpath('//div[@class="article"]//ul/li/a/@href').extract()
        items = []
        for i in range(len(parentNames)):
            parentName = "/Users/stonelqf/Desktop/sina/" + parentNames[i]
            if not os.path.exists(parentName):
                os.mkdir(parentName)
            for j in range(len(chlidUrls)):
                item = SinaspiderItem()
                if chlidUrls[j].startswith(parentUrls[i]):
                    item['childUrl'] = chlidUrls[i]
                    chlidName = parentName + "/" + chlidNames[j]
                    if not os.path.exists(chlidName):
                        os.mkdir(chlidName)
                    item["contentFileUrl"] = chlidName + "/"
                    items.append(item)
        for item in items:
            yield scrapy.Request(url=item['childUrl'], meta={"meta_1": item}, callback=self.parse_child)

    def parse_child(self, response):
        meta = response.meta["meta_1"]
        items = []
        for node in response.xpath('//div/a/@href').extract():
            if node.endswith(".shtml"):
                item = SinaspiderItem()
                item['contentFileUrl'] = meta['contentFileUrl']
                item['childUrl'] = meta['childUrl']
                item['fileUrl'] = node
                items.append(item)
        for item in items:
            yield scrapy.Request(url=item['fileUrl'], meta={"meta_2": item}, callback=self.last)

    def last(self, response):
        meta2 = response.meta["meta_2"]
        title = response.xpath("//h1[@class=main=title]/text()").extract()
        if len(title) != 0:
            item = SinaspiderItem()
            item['contentFileUrl'] = meta2['contentFileUrl']
            item["contentTitle"] = title[0]
            contents = response.xpath('//div[@class ="article"]/p/text()').extract()
            text=""
            if len(contents) != 0:
                for content in contents:
                    text += content
            item["content"]=text
            yield item

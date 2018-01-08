# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    childUrl=scrapy.Field()
    # 文章标题
    contentTitle=scrapy.Field()
    # 文章内容
    content=scrapy.Field()
    # 文章保存路径
    contentFileUrl=scrapy.Field()
    # 文章的访问url
    fileUrl=scrapy.Field()

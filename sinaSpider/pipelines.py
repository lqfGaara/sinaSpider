# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinaspiderPipeline(object):
    def process_item(self, item, spider):
        file = item['contentFileUrl'] + str(item["contentTitle"]).strip() + ".txt"
        print(file)
        with open(file, "w") as f:
            if (len(item['content']) != 0):
                f.write(item['content'])
        return item

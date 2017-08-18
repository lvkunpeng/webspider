# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 笔记：做与数据存储相关的内容
class ArtclespiderPipeline(object):
    def process_item(self, item, spider):
        return item

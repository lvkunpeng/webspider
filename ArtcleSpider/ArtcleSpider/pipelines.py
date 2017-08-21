# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#引入codecs解决文件的编码问题
import codecs

#引入json模块将itme转化为dict
import json

#导入系统的pipeline 将其自带的函数进行重载
from scrapy.pipelines.images import ImagesPipeline
#scrapy自带的json转化器
from scrapy.exporters import JsonItemExporter

# 笔记：做与数据存储相关的内容，可以拦截item
class ArtclespiderPipeline(object):
    def process_item(self, item, spider):
        return item

# 将数据保存到mysql当中

# 将数据保存到json当中
class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        # 设置文件的接收格式json,以写的方式打开w,设置为utf-8编码格式
        self.file = codecs.open('alticle.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    # 写入之后关闭写入
    def spider_closed(self, spider):
        self.file.close()

# scrapy自带的json转化函数
class JsonExporterPipleLine(object):
    # 调用scrapy提供的json export 导出json文件
    def __init__(self):
        self.file = open('articleexport.json','wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# 截取item中的results得到下载图片的文件保存路径并添加到已经定一个的items image)_file_path 路径下
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path

        return item
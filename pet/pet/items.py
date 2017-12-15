# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from models.models import petType
from elasticsearch_dsl.connections import connections
es = connections.create_connection(petType._doc_type.using)

import scrapy

def gen_suggests(index, info_tuple):
    # 根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es的anal接口分析字符串
            words = es.indices.analyze(index=index, analyzer= "ik_max_word",params={'filter':["lowercase"]},body=text)
            anylyzed_words = set([r["token"] for r in words if len(r["token"])>1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()
        if new_words:
            suggests.append({"input":list(new_words),"weight":weight})
    return suggests

class PetItem(scrapy.Item):
    kind = scrapy.Field()
    intro = scrapy.Field()
    url_object_id = scrapy.Field()
    base_info = scrapy.Field()
    image_url = scrapy.Field()
    url = scrapy.Field()
    # suggest = scrapy.Field()
    # image_path = scrapy.Field()
    pass

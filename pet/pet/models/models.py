# -*- coding: utf-8 -*-

from datetime import datetime
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

# 指定要链接的el服务器的地址
connections.create_connection(hosts=['139.219.68.228'])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer('ik_max_word',filter=['lowercase'])

class petType(DocType):
    # 定义es里面的数据类型，不需要分词的子段定义为keywrd
    suggest = Completion(analyzer = ik_analyzer)
    # 自定义建议字段
    kind = Text(analyzer='ik_max_word')
    intro = Text(analyzer='ik_max_word')
    url_object_id = Keyword
    base_info = Text(analyzer='ik_max_word')
    image_url = Keyword
    url = Keyword
    # title_suggest = Completion(analyzer=ik_analyzer, search_analyzer=ik_analyzer)
    # title = Text(analyzer='ik_max_word', search_analyzer="ik_max_word", fields={'title': Keyword()})
    #
    # tags = Text(analyzer='ik_max_word', fields={'tags': Keyword()})
    # content = Text(analyzer='ik_max_word')

    class Meta:
        # 指定要链接的服务器的索引（也就是具体的数据库和具体的表）
        index = 'worm'
        doc_type = 'youchong'
    #
    # def save(self, ** kwargs):
    #     self.lines = len(self.body.split())
    #     return super(Article, self).save(** kwargs)

    # def is_published(self):
    #     return datetime.now() < self.published_from

petType.init()
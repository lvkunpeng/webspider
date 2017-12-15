# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 引入codecs解决文件的编码问题
import codecs

# 引入json模块将itme转化为dict
import json

# 引入mysql客户端
import MySQLdb
# pip install mysqlclient 通过此命令引入mysql

# 引入cursors执行mysql的异步存储
import MySQLdb.cursors

# 导入系统的pipeline 将其自带的函数进行重载
from scrapy.pipelines.images import ImagesPipeline
# scrapy自带的json转化器
from scrapy.exporters import JsonItemExporter
# 过滤文章中的标签
from w3lib.html import remove_tags
# 引入twisted来执行mysql的异步存储
from twisted.enterprise import adbapi
from models.models import petType
from elasticsearch_dsl.connections import connections
es = connections.create_connection(hosts=['139.219.68.228'])

def gen_suggests(index, info_tuple):
    # 根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es的anal接口分析字符串
            words = es.indices.analyze(index=index, analyzer= "ik_max_word",params={'filter':["lowercase"]},body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()
        if new_words:
            suggests.append({"input":list(new_words),"weight":weight})
    return suggests


# 笔记：做与数据存储相关的内容，可以拦截item
class petspiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 将数据保存到mysql当中

# 将数据保存到json当中
class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
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
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# 截取item中的results得到下载图片的文件保存路径并添加到已经定一个的items image)_file_path 路径下
# class ArticleImagePipeline(ImagesPipeline):
#     def item_completed(self, results, item, info):
#         for ok, value in results:
#             image_file_path = value["path"]
#         item["image_path"] = image_file_path
#
#         return item


# 插入数据同步操作(不推荐)
# 连接mysql 在centos下面首先要安装  yum install python-devel mysql-devel
# 然后在虚拟环境下安装 pip3 install mysqlclient
# 将数据保存在mysql中
class MysqlPipeline(object):
    def __init__(self):
        # 配置连接mysql参数
        self.conn = MySQLdb.connect("localhost", "root", "11space123", "scrapydb", charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # , front_image_path, front_image_url, comment_nums, fav_nums, praise_nums, tags, content
        insert_sql = """    
                                     insert into youchong(url_object_id, kind, url, base_info, intro, image_url)
                                     VALUES (%s, %s, %s, %s, %s, %s)
                                """
        print(insert_sql)
        self.cursor.execute(insert_sql, (
            item["url_object_id"], item["kind"], item["url"], item["base_info"], item["intro"],item["image_url"][0]))
        self.conn.commit()


# 异步将爬取数据写入mysql当中(推荐)
class MysqlTwistedPipeline(object):
    # 对该方法进行一个实例化,并将刚才更改的dbpool传入
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 可以定义一个方法将setting的内容传递进来并使用,此处传入了mysql的配置信息
    @classmethod
    # 此处调用的是类方法 也就是下面的cls指带的就是MysqlTwistedPipeline类
    def from_settings(cls, setting):
        # 将所有参数变成一个dict 并传入adbapi方法中
        dbparms = dict(
            host=setting["MYSQL_HOST"],
            db=setting["MYSQL_DBNAME"],
            user=setting["MYSQL_USER"],
            passwd=setting["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        # 因为调用的是MysqlTwistedPipeline类,配置完成之后将参数dbpool传递到cls当中,并将cls返回
        return cls(dbpool)

    # 异步执行函数
    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        # 调用self中的dbpool方法,并会将传递进来的自定义函数异步执行,此实例中为do_insert,第二个参数为要插入的数据
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)  # 处理异常

    # 错误处理函数
    '''
        failure:捕获的错误
        spider:目前爬虫的位置
    '''

    def handle_error(self, failure):
        print(failure)

    # 自定义需要异步执行的函数（插入数据函数）
    # def do_insert(self, cursor, item):
    #     # 执行具体的插入
    #     insert_sql = """
    #                        insert into jobbole_art(title, url, create_date, fav_nums,  url_object_id, front_image_path, front_image_url, comment_nums, praise_nums, tags, content)
    #                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #                    """
    #     # 这个函数中的cursor就是下面的cursor,并会自动帮我们执行self.conn.commit()操作
    #     print(item)
    #     cursor.execute(insert_sql, (
    #     item["title"], item["url"], item["create_date"], item["fav_nums"], item["url_object_id"],
    #     item["front_image_path"], item["front_image_url"][0], item["comment_nums"], item["praise_nums"], item["tags"],
    #                    item["content"]))

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """    
                             insert into youchong(url_object_id, kind, url, base_info, intro, image_url)
                             VALUES (%s, %s, %s, %s, %s, %s)
                        """
        # 这个函数中的cursor就是下面的cursor,并会自动帮我们执行self.conn.commit()操作
        print(item)
        cursor.execute(insert_sql, (
            item["url_object_id"], item["kind"], item["url"], item["base_info"], item["intro"],item["image_url"][0]))

class ElasticSearchPipeline(object):
    # 写入数据到es中

    # def analyze_tokens(self, text):
    #     from models.models import connections
    #     es = connections.get_connection(Article._doc_type.using)
    #     index = Article._doc_type.index
    #
    #     if not text:
    #         return []
    #     global used_words
    #     result = es.indices.analyze(index=index, analyzer='ik_max_word',
    #                                 params={'filter': ['lowercase']}, body=text)
    #
    #     words = set([r['token'] for r in result['tokens'] if len(r['token']) > 1])
    #
    #     new_words = words.difference(used_words)
    #     used_words.update(words)
    #     return new_words
    #
    # @classmethod
    # def from_settings(cls, settings):
    #     dbparms = dict(
    #         host=settings["MYSQL_HOST"],
    #         db=settings["MYSQL_DBNAME"],
    #         user=settings["MYSQL_USER"],
    #         passwd=settings["MYSQL_PASSWORD"],
    #         charset='utf8',
    #         cursorclass=MySQLdb.cursors.DictCursor,
    #         use_unicode=True,
    #     )
    #     dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
    #
    #     return cls(dbpool)
    #
    # def gen_suggests(self, title, tags):
    #     global used_words
    #     used_words = set()
    #     suggests = []
    #
    #     for item, weight in ((title, 10), (tags, 3)):
    #         item = self.analyze_tokens(item)
    #         if item:
    #             suggests.append({'input': list(item), 'weight': weight})
    #     return suggests
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     ext = cls()
    #     ext.settings = crawler.settings
    #     Article.init()
    #     return ext


    def process_item(self, item, spider):
        # 将item转换为es的数据
        # pip install elasticsearch-dsl  下载python的el的写入包
        from models.models import petType
        article = petType()
        article.kind = item["kind"]
        article.intro = item["intro"]
        article.url_object_id = item["url_object_id"]
        article.base_info = item["base_info"]
        article.content = remove_tags(item["intro"]).strip().replace("\r\n", "").replace("\t", "")
        article.suggest = gen_suggests(petType._doc_type.index,((article.kind,20),(article.content,10)))
        article.image_url = item["image_url"]
        article.save()

        return item
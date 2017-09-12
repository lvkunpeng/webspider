# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
# 笔记：定义数据保存的格式
import scrapy


class ArtclespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
# 通过自定义一个数据类,来接收scrapy爬取到的子段，并将相同的子段区分传到piplines中去,同时保存,还可以将相同的子段进行去重
class JobBoleArticleItem(scrapy.Item):
    #文章标题
    title = scrapy.Field()
    #文章创建日期
    create_date = scrapy.Field()
    url = scrapy.Field()
    #封面图的外网地址
    front_image_url = scrapy.Field()
    #封面图的本地存放地址
    front_image_path = scrapy.Field()
    #点赞数
    praise_nums = scrapy.Field()
    #评论数
    comment_nums = scrapy.Field()
    #收藏数
    fav_nums = scrapy.Field()
    #文章标签
    tags = scrapy.Field()
    #正文
    content = scrapy.Field()
    #md5化url地址
    url_object_id = scrapy.Field()

# 知乎的问题item
class ZhihuQusetionItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()
    # create_time
    # update_time

# 知乎的问题回答Item
class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_num = scrapy.Field()
    update_num = scrapy.Field()
    crawl_time = scrapy.Field()


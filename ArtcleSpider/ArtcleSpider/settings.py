# -*- coding: utf-8 -*-
import os
# Scrapy settings for ArtcleSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#笔记：工程的文件名
BOT_NAME = 'ArtcleSpider'

SPIDER_MODULES = ['ArtcleSpider.spiders']
NEWSPIDER_MODULE = 'ArtcleSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ArtcleSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules  笔记：默认遵循robots协议,如果不注释,scrapy会根据目标网站的robots协议来把不符合robots协议的网站过滤掉
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ArtcleSpider.middlewares.ArtclespiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ArtcleSpider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#控制pipelines取用的item,pipline即是数据流通的管道的意思,后面的参数为数据流的处理顺序,数字越小的越先处理
ITEM_PIPELINES = {
   'ArtcleSpider.pipelines.JsonWithEncodingPipeline': 2,
   # 将数据流中你设定的子段,中的图片下载到本地
   # 'scrapy.pipelines.images.ImagesPipeline': 1,
   'ArtcleSpider.pipelines.ArticleImagePipeline': 1,
}

# 配置数据留中你想要的下载的图片的子段
IMAGES_URLS_FIELD = 'front_image_url'

# 获取当前settings的路径
project_dir = os.path.abspath(os.path.dirname(__file__))

# 配置下载的图片的保存路径   注意：执行时可能会报错没有PIL模块(图片解析模块),在虚拟环境中安装pillow即可解决
# 安装命令 pip install -i https://pypi.douban.com/simple pillow
IMAGES_STORE = os.path.join(project_dir, 'images')

# 配置下载的图片的最大最小值
# IMAGES_MIN_HEIGHT = 100
# IMAGES_MIN_WIDTH = 100

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

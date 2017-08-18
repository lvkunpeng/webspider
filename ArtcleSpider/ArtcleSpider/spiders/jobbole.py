# -*- coding: utf-8 -*-


#引入正则模块
import re
#引入scrapy
import scrapy
#引入响应模块
from scrapy.http import Request
#引入parse模块拼接完整的url
from urllib import parse


#定义一个类
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    # 可以在urls里面放入所有的要爬取的url
    start_urls = ['http://web.jobbole.com/all-posts/']
    # 所有爬取的网站url最后都会进入到parse中，response本身带有xpath方法

    #主爬取流程函数
    def parse(self, response):
        # 通过css选择器选取爬取的当前列表页并放在一个数组中
        post_urls = response.css('#archive .floated-thumb .post-thumb a::attr(href)').extract()
        # 循环整个数组,并将当前列表页每一个url交给scrapy
        for post_url in  post_urls:
            #yield 关键字会将后面的网址自动交个scrapy进行下载
            #urljoin方法会将url拼接成完整的地址
            #callback回调函数将给scrapy下载目标网址操作执行完成之后执行的方法
            yield scrapy.Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)
            #yield scrapy.Request(url= post_url, callback=self.parse_detail)
        # 提取下个列表页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers:attr(href)").extract_first("")
        # 如果下个列表页存在
        if next_url:
            # 将列表页面交给scrapy,并在完成之后通过callback交给scrapy一个parse函数(注意：此处的parse只是函数体,没有执行)
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
    #爬取动作函数
    def parse_detail(self,response):        #提取文章的具体子段
        #获取下一页的url并交给scrapy下载
        #/html/body/div[3]/div[3]/div[1]
        #提取文章标题
        print(123)
        title = response.css(".entry-header").xpath("h1/text()").extract()[0]
        print(title)
        #re_selector = response.xpath(".// *[ @ id = 'post-92238'] / div[1] / h1/text()")
        pass



# 调试阶段可以在虚拟环境中先制定某个页面,打开scrapy shell url('爬取动作网址')下载好单个网址,检测爬取动作的正确性
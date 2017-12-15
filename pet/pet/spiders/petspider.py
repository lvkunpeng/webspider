# -*- coding: utf-8 -*-


# 引入正则模块
import re
# 引入scrapy
import scrapy
# 引入datatime库进行日期格式转化
import datetime
# 引入响应模块
from scrapy.http import Request
# 引入parse模块拼接完整的url
from urllib import parse
# 引入对应的iteam
from items import PetItem
# 引入utils.common 导入转化md5模块
from utils.common import get_md5
from scrapy.utils.response import body_or_str


# 定义一个类
class petSpider(scrapy.Spider):
    name = 'petspider'
    allowed_domains = ["http://www.yc.cn"]
    # 可以在urls里面放入所有的要爬取的url
    start_urls = ['http://www.yc.cn/sitemap.xml']
    # 所有爬取的网站url最后都会进入到parse中，response本身带有xpath方法
    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    header = {
        "HOST": "http://www.yc.cn",
        "Referer": "http://www.yc.cn",
        "User-Agent": agent
    }

    # 主爬取流程函数
    def parse(self, response):
        nodename = 'loc'
        list = []
        text = body_or_str(response)
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" % (nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            list.append(url)
        # post_nodes = response.css('tbody .floated-thumb .post-thumb a')
        # 循环整个数组,并将当前列表页每一个节点交给scrapy
        for post_node in list:
            # 解析每一个节点上的url
            if re.search('breed',post_node):
                post_url = post_node
            # yield 关键字会将后面的网址自动交个scrapy进行下载
            # urljoin方法会将url拼接成完整的地址
            # callback回调函数将给scrapy下载目标网址操作执行完成之后执行的方法
            # 并将列表页取到的img地址,通过meat属性进行传递,交给parse_detail函数
                yield Request(url=post_url, callback=self.parse_detail,  dont_filter=True)
               # break
            # 提取下个列表页并交给scrapy进行下载

    # 爬取动作函数
    def parse_detail(self, response):
        youchong_item = PetItem()
        # 提取宠物名称
        kind = response.css(".basic").xpath("h1/text()").extract()[0]

        # 不容易筛选,暂时提取取全部,之后使用正则匹配出具体的值
        base_info = response.css(".basic").extract()[0]
        # name_en = re.match(".*英文名.*", base_info)

        # 提取宠物简介
        intro1 = response.css(".j-pedia").xpath("div[1]").extract()[0]
        intro2 = response.css(".j-pedia").xpath("div[2]").extract()[0]
        intro3 = response.css(".j-pedia").xpath("div[3]").extract()[0]
        intro4 = response.css(".j-pedia").xpath("div[4]").extract()[0]
        introall = intro1+intro2+intro3+intro4
        # 提取宠物的图片
        image_url = response.css(".pet-desc-l img").xpath("@src").extract()[0]

        # 为youchong_item传递值
        youchong_item["url_object_id"] = get_md5(response.url)
        youchong_item["kind"] = kind
        youchong_item["url"] = response.url
        youchong_item["base_info"] = base_info
        youchong_item["intro"] = introall
        # 此处要写成数组的格式,因为传递到pipline的时候需要传递一个数组
        youchong_item["image_url"] = [image_url]

        # 将得到的youchong_item传递到pipelines 中去,模版已经自动生成了pipeline的配置文件,需要在settings中将“ITEM_PIPELINES”参数配置打开
        yield youchong_item

        pass



        # 调试阶段可以在虚拟环境中先制定某个页面,打开scrapy shell url('爬取动作网址')下载好单个网址,检测爬取动作的正确性
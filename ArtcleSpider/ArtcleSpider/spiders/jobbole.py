# -*- coding: utf-8 -*-


#引入正则模块
import re
#引入scrapy
import scrapy
#引入datatime库进行日期格式转化
import datetime
#引入响应模块
from scrapy.http import Request
#引入parse模块拼接完整的url
from urllib import parse
#引入对应的iteam
#from items import JobBoleArticleItem
# 引入utils.common 导入转化md5模块
from utils.common import get_md5

#定义一个类
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ["python.jobbole.com"]
    # 可以在urls里面放入所有的要爬取的url
    #start_urls = ['http://python.jobbole.com/all-posts/']
    start_urls = ['http://python.jobbole.com/all-posts/']
    # 所有爬取的网站url最后都会进入到parse中，response本身带有xpath方法

    #主爬取流程函数
    def parse(self, response):
        # 通过css选择器选取爬取的当前列表页的节点并放在一个数组中
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        # 循环整个数组,并将当前列表页每一个节点交给scrapy
        for post_node in  post_nodes:
            #解析每一个节点的img上的url
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css('::attr(href)').extract_first("")
            #yield 关键字会将后面的网址自动交个scrapy进行下载
            #urljoin方法会将url拼接成完整的地址
            #callback回调函数将给scrapy下载目标网址操作执行完成之后执行的方法
            #并将列表页取到的img地址,通过meat属性进行传递,交给parse_detail函数
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)
        # 提取下个列表页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        # 如果下个列表页存在
        if next_url:
            # 将列表页面交给scrapy,并在完成之后通过callback交给scrapy一个parse函数(注意：此处的parse只是函数体,没有执行)
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
    #爬取动作函数
    def parse_detail(self,response):
        #新建一个article_item接收实例化的JobBoleArticleItem
        article_item = JobBoleArticleItem()

        #提取文章标题
        title = response.css(".entry-header").xpath("h1/text()").extract()[0]

        #提取文章的创建日期
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·","").strip()

        #提取文章的点赞数目
        praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]

        #提取文章封面图,使用get方法取字典值不会抛出异常,第二个值给了front_image_url一个默认值
        front_image_url = response.meta.get("front_image_url","")

        #提取文章的评论数
        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0


        #提取文章收藏数
        fav_nums = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        #提取文章正文
        content = response.xpath("//div[@class='entry']").extract()[0]

        #提取文章分类
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)


        #为article_item传递值
        article_item["url_object_id"] = get_md5(response.url)
        article_item["title"] = title
        article_item["url"] = response.url
        #进行日期转化,并对异常的日期进行捕获
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item["create_date"] = create_date

        # 此处要写成数组的格式,因为传递到pipline的时候需要传递一个数组
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comment_nums
        article_item["fav_nums"] = fav_nums
        article_item["tags"] = tags
        article_item["content"] = content

        #将得到的artcle_item传递到pipelines 中去,模版已经自动生成了pipeline的配置文件,需要在settings中将“ITEM_PIPELINES”参数配置打开
        yield article_item

        pass



# 调试阶段可以在虚拟环境中先制定某个页面,打开scrapy shell url('爬取动作网址')下载好单个网址,检测爬取动作的正确性
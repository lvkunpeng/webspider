# -*- coding: utf-8 -*-
import scrapy
import re
import json
# 导入parse模块进行url的拼接
# 此处对py3进行兼容操作
try:
    import urlparse as parse
except:
    from urllib import parse

from scrapy.loader import ItemLoader
from items import ZhihuQusetionItem, ZhihuAnswerItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    header = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": agent
    }
    # 爬虫逻辑中流程上没有callback函数之后,就会自动调转到parse函数
    def parse(self, response):
        # 当scrapy流程中先是进入start_requests函数,在流程中没有其他的callback函数的时候回自动转到parse函数中,所以从此函数可以开始爬取操作
        # 从response中提取url为 /question/xxx 就下载之后直接进入解析函数
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url,url) for url in all_urls]
        print("正在检索文章列表")
        all_urls = filter(lambda x:True if x.startswith("https") else False,all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                print("检索到的文章ID:"+question_id,"检索到的文章地址:"+request_url)

                yield scrapy.Request(request_url, headers=self.header, callback=self.parse_question())
            else:
                pass
    # 处理爬取中检测到的question item
    def parse_question(self, response):
        # 处理知乎新版本
        if "QuestionHeader-title" in response.text:
            item_loader = ItemLoader(item=ZhihuQusetionItem(),response=response)

        # 处理知乎老版本
        else:
            pass






    # 因为知乎是需要登录后才能浏览的,scrapy的入口函数即为start_requests,所以在这需要重写这个函数
    def start_requests(self):
        return [scrapy.Request("https://www.zhihu.com/#signin",headers=self.header, callback=self.login)]

    def login(self, response):
        response_text = response.text
        # xsrf = ""
        # match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
        # if match_obj:
        #     xsrf(match_obj.group(1))
        # if xsrf:
        #     post_data = {
        #         "_xsrf": xsrf,
        #         "phone_num": "13920988689",
        #         "password": "a135120135",
        #         "captcha":""
        #     }
        post_data = {
                "phone_num": "13920988689",
                "password": "a135120",
                "captcha":""
            }
        import time
        t = str(int(time.time() * 1000))
        # 知乎的英文验证码路径
        captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
        # 知乎的倒立验证码路径
        captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login&lang=cn".format(t)
        # 此处需要注意:因为scrapy发送的都是异步请求,所以即使使用session传递cooike值,也会因为异步导致session携带的cooike不是同一个会话产生的,所以此处要将scrapy.Request通过yield的方式传递出去,并在callback中调用登录函数,这样才是一个会话保证登录策划成功
        #yield scrapy.Request(captcha_url,headers=self.header,meta={"post_data":post_data},callback=self.login_after_captcha)

        # 汉字验证码
        yield scrapy.Request(captcha_url,headers=self.header,meta={"post_data":post_data},callback=self.login_after_captcha_cn)

    def login_after_captcha(self,response):
        post_data = response.meta.get("post_data")
        import webbrowser
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()
        from PIL import Image
        try:
            im = Image.open("captcha.jpg")
            # 本系统中没有合适的图片查看器,引入webbrowser通过浏览器的方式进行查看
            im.show()
            webbrowser.open("captcha.jpg")
        except:
            pass
        # 赋予新的验证码值
        post_data["captcha"] = input("输入验证码\n")
        post_url = "https://www.zhihu.com/login/phone_num"
        return [scrapy.FormRequest(
            url="https://www.zhihu.com/login/phone_num",
            formdata=post_data,
            headers=self.header,
            callback=self.check_login
        )]

    # 知乎汉字验证码登录
    def login_after_captcha_cn(self,response):
        with open("captcha.jpg","wb") as f:
            f.write(response.body)
            f.close()
        from zheye import zheye
        z = zheye()
        positions = z.Recognize("captcha.jpg")
        pos_arr = []
        if len(positions) == 2:
            if positions[0][1] > positions[1][1]:
                pos_arr.append([positions[1][1],positions[1][0]])
                pos_arr.append([positions[0][1],positions[0][0]])
            else:
                pos_arr.append([positions[0][1],positions[0][0]])
                pos_arr.append([positions[1][1], positions[1][0]])
        else:
            pos_arr.append([positions[0][1], positions[0][0]])
        post_data = response.meta.get("post_data")
        if len(positions) == 2:
            post_data["captcha"] = '{"img_size":[200,44],"input_points":[[%.2f,%f],[%.2f,%f]]}' % (pos_arr[0][0] / 2,pos_arr[0][1] / 2,pos_arr[1][0] / 2,pos_arr[1][1] / 2)
        else:
            post_data["captcha"] = '{"img_size":[200,44],"input_points":[[%.2f,%f]}' % (pos_arr[0][0] / 2,pos_arr[0][1] / 2)
        post_data["captcha_type"] = "cn"
        return [scrapy.FormRequest(
            url="https://www.zhihu.com/login/phone_num",
            formdata=post_data,
            headers=self.header,
            callback=self.check_login
        )]

    def check_login(self, response):
        # 验证是否成功登录服务器
        text_json = json.loads(response.text)
        print(text_json["msg"])
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.header)

        pass



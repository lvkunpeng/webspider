# -*- coding: utf-8 -*-
import scrapy


class TianyanSpider(scrapy.Spider):
    name = 'tianyan'
    allowed_domains = ['https://www.tianyancha.com/login']
    start_urls = ['http://https://www.tianyancha.com/login/']
    agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    header = {
        "HOST": "www.tianyancha.com",
        "Referer": "https://www.tianyancha.com/login",
        "User-Agent": agent
    }

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request("https://www.tianyancha.com/login", headers=self.header, callback=self.login)]

    def login(self, response):
        print(123)
        response_text = response.text
        post_url = "https://www.tianyancha.com/cd/login.json"
        post_data = {
            "phone_num": "13920988689",
            "password": "d1ab05f379b4fda85f50bc9f9c3aa5f6",
            "autoLogin":"true",
            "loginway":"PL"
        }
        scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.header,
            callback=self.check_login
        )
        print(response)



    def check_login(self, response):
        # 验证是否成功登录服务器
        print(response)
        pass

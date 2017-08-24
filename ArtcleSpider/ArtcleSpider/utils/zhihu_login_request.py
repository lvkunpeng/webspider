# 登陆模块依赖request库,首先在虚拟环境中安装
import requests

# 引入cooike解析模块
try:
    import cooikelib
except:
    # py3中该模块放在http模块下面
    import http.cookiejar as cooikelib

import re

# 引入连接session(session指代的是某一次的请求,是一个长连接,来代替requests,不需要每一次都要建立连接效率更高)
session = requests.session()
# 自定义设备类型
agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
# 自定义请求头
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent
}


# 获取xsrf字串
def get_xsrf():
    # 此处直接由requests模块对域名进行访问的时候,返回的有可能是一个500的错误而非对应的网页html,因为这种请求的请求头为python2或者python3而不是一个浏览器的请求头
    # 这是通过headers设置的请求头
    response = session.get("https://www.zhihu.com", headers=header)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""


# 知乎登陆函数
def zhuhu_login(account, password):
    if re.match("1\d{10}", account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password
        }
        # 向服务器发送登录信息
        response_text = session.post(post_url, data=post_data, headers=header)
        session.cookies.save()


zhuhu_login("13920988689","a135120")

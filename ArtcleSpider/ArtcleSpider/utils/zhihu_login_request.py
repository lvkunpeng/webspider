# 登陆模块依赖request库,首先在虚拟环境中安装
import requests
import json

# 引入cooike解析模块
try:
    import cooikelib
except:
    # py3中该模块放在http模块下面
    import http.cookiejar as cooikelib

import re

# 引入连接session(session指代的是某一次的请求,是一个长连接,来代替requests,不需要每一次都要建立连接效率更高)
session = requests.session()
# 调用cookielib中的cookiejar方法能够更好的将服务器传回来的cooike值保存成为一个本地文件,并随着session传递cooike
session.cookies = cooikelib.LWPCookieJar(filename="cookies.txt")
# cookies保存异常处理
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cooike未能加载")
# 自定义设备类型
agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"

# 自定义请求头
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/explore",
    "User-Agent": agent,
    # "Origin":"https://www.zhihu.com"
}


# 获取xsrf字串
def get_xsrf():
    # 此处直接由requests模块对域名进行访问的时候,返回的有可能是一个500的错误而非对应的网页html,因为这种请求的请求头为python2或者python3而不是一个浏览器的请求头
    # 这是通过headers设置的请求头
    # match只能匹配单行,可以使用search全局匹配
    response = session.get("https://www.zhihu.com", headers=header)
    match_obj = re.search('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""


# 通过个人中心页面返回验证码判断用户是否为登录状态
def is_login():
    inbox_url = "https://www.zhihu.com/inbox"
    # 此处的第三个属性为禁止重定向,因为重定向之后服务器会返回一个登录首页,登录首页的状态码会变成200
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True
    pass


# 获取首页并将首页的内容保存到本地
def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")


# 获取验证码手动通过验证
def get_captcha():
    import time
    import webbrowser
    t = str(int(time.time() * 1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t = session.get(captcha_url, headers=header)
    # 将链接返回的图片以f(文件的形式保存,并通过二进制打开)
    with open("captcha.jpg", "wb") as f:
        f.write(t.content)
        f.close()
    from PIL import Image
    try:
        im = Image.open("captcha.jpg")
        # 本系统中没有合适的图片查看器,引入webbrowser通过浏览器的方式进行查看
        im.show()
        webbrowser.open("captcha.jpg")
    except:
        pass
    # py3中有的 py2中为raw函数
    captcha = input("输入验证码\n")
    return captcha


# 知乎登陆函数
def zhuhu_login(account, password):
    if re.match("1\d{10}", account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "password": password,
            "captcha": get_captcha(),
            # "_xsrf": get_xsrf(),
            "remember_me": "true",
            "phone_num": account,
        }
    else:
        if "@" in account:
            print("邮箱登录方式")
            post_url = "https://www.zhihu.com/login/email"
            get_captcha()
            captcha = get_captcha()
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password,
                "captcha": captcha
            }
    # 向服务器发送登录信息
    response_text = session.post(post_url, data=post_data, headers=header)
    msg = response_text.text
    # 把str转化为dict
    msg = json.loads(msg)
    print(msg["msg"])

    # 保存session中的cooike,如需要重新发送登录请求,请将cooike清空在发送
    # session.cookies.save()


# 执行区域

# 执行登录函数
zhuhu_login("13920988689", "a135120")

# 执行判断是否登录
# is_login()

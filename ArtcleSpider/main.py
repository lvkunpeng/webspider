# 调用scrpay命令行脚本模块,这样就不用另开一个命令行调用scrpay了
from scrapy.cmdline import execute

#注入系统文件
import sys

#设置工程目录
#sys.path.append("/root/Desktop/webspiders/ArtcleSpider")

#注入os模块
import os
print(os.path.dirname(os.path.abspath(__file__)))
# 获取当前文件父目录所在的路径所在的目录 __file__指的就是当前文件
# 当前文件在的路径os.path.abspath(__file__)
# 所在文件夹的目录os.path.dirname(xxx)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


#配置执行jobbole的命令
execute(["scrapy" , "crawl" , "youchong"])
#execute(["scrapy","crawl","jobbole"])
#execute(["scrapy","crawl","tianyan"])
#execute(["scrapy","crawl","zhihu"])

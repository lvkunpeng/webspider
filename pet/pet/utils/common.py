
# md5转化函数
import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == "__main__":
    #md5装换不能接收一个unicode编码格式,要先进行转化为utf——8
    print(get_md5("http://jobbole.com".encode("utf-8")))
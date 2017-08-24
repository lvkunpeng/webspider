from zheye import zheye
z = zheye()
positions = z.Recognize('path/to/captcha.gif')
print(positions)
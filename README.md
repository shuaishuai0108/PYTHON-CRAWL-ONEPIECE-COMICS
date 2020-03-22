# PYTHON-CRAWL-ONEPIECE-COMICS
海贼王漫画爬取+推送kindle（email邮箱） 

hzw_02.py 

脚本会自动下载漫画到当前目录下，并创建Pdf文件后推送到kindle邮箱或个人邮箱内。 

## 参数：
self.num = 1000 # 起始爬取集数 

邮件设置,默认不开启邮件发送 

self.email = email # 推送发邮件需要传入参数email=True 

self.mail_host = "smtp.exmail.qq.com"  # 设置服务器 

self.mail_user = "123@qq.com"  # 用户名 

self.mail_pass = "123456"  # 口令 

self.receivers = ['123456@qq.com']  # 接收邮件，可设置为你的kindle邮箱或者QQ邮箱 

文件地址设置 

self.path = './海贼王' 


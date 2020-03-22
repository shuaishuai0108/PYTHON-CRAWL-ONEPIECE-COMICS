# -*- coding: utf-8 -*-
import requests
import fitz, glob
import re
import os
import time
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


class hzw():

    def __init__(self, email=False):
        self.num = 950 # 起始爬取集数

        # 邮件设置,默认不开启邮件发送
        self.email = email # 推送发邮件需要传入参数email=True
        self.mail_host = "smtp.exmail.qq.com"  # 设置服务器
        self.mail_user = "123@qq.com"  # 用户名
        self.mail_pass = "123456"  # 口令
        # sender = '123.qq@com'
        self.receivers = ['123456@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        # 文件地址设置
        self.path = './海贼王'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.path_ji = ''
        self.file_name = ''

        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36"}

    def run(self):
        num = self.num
        while True:
            print("海贼王第%d集" % num)
            p_urls = self.img_url(num)
            if p_urls:
                self.path_ji = self.path + '/' + '海贼王%s话' % str(num)
                if not os.path.exists(self.path_ji):
                    os.makedirs(self.path_ji)

                self.main(p_urls)
                time.sleep(2)
                num += 1
            else:
                print("海贼王第%s话内容未更新,3小时后检测" % num)
                print('-' * 50)
                while True:
                    inp = input("继续等待输入：y,退出输入：n\n")
                    if inp == 'y':
                        time.sleep(10800)
                        break
                    elif inp == 'n':
                        print('正在退出')
                        print('-' * 50)
                        exit()
                    else:
                        print('输入错误,请重新输入')
                        print('-' * 50)
                        continue

    def main(self, p_urls):
        ls = os.listdir(self.path_ji)
        num = 1
        for url in p_urls:
            name = '%s-%s.jpg' % (num, self.path_ji.split('/')[-1])
            if name in ls:
                num += 1
                # print(name + "已存在，跳过")
                continue
            self.file_name = self.path_ji + '/' + name
            self.download(url, self.file_name)
            print(self.file_name, "已创建")
            num += 1
            # print("-" * 50)
            time.sleep(1)
        pdf_path = self.path_ji + '/' + '%s.pdf' % self.path_ji.split('/')[-1]

        # 如果pdf文件不存在的话，创建pdf文件，发送邮件
        if pdf_path.split('/')[-1] not in ls:
            self.pic2pdf(pdf_path)
        if self.email:
            ret = self.send_email(pdf_path)
            print(ret)

    def img_url(self, num):

        pic_list = []
        i = 0
        while True:
            url = "https://manhua.fzdm.com/02/%s/index_%s.html" % (str(num), str(i))

            requests.packages.urllib3.disable_warnings()
            req = requests.get(url, headers=self.headers, verify=False)
            if req.text == "404!":
                break
            # 提取图片地址
            rt = r'\d+/\d+/\d+\.jpg'
            html_url = re.findall(rt, req.text)
            # print(html_url[0])
            # from lxml import etree
            # html = etree.HTML(req.text)
            # html_url = html.xpath('//img[@id="mhpic"]/@src')
            # print(html_url[0])
            try:
                pic = "http://p1.manhuapan.com/%s" % html_url[0]
            except:
                # print(req.url,'请求发生错误')
                break
            pic_list.append(pic)
            i += 1

        print(pic_list)
        return pic_list

    def download(self, url, path):
        req = requests.get(url, headers=self.headers, verify=False).content
        with open(path, 'wb') as file:
            file.write(req)

    def pic2pdf(self, pdf_path):

        imgs = glob.glob(self.path_ji + '/' + "*.jpg")

        doc = fitz.open()
        for img in range(len(imgs)):  # 读取图片，确保按文件名排序
            img = img + 1
            img_file = "%s/%s-%s.jpg" % (self.path_ji, img, self.path_ji.split('/')[-1])
            imgdoc = fitz.open(img_file)  # 打开图片

            pdfbytes = imgdoc.convertToPDF()  # 使用图片创建单页的 PDF
            imgpdf = fitz.open("pdf", pdfbytes)

            doc.insertPDF(imgpdf)  # 将当前页插入文档

        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        doc.save(pdf_path)  # 保存pdf文件

    def send_email(self, pdf_path):
        print("正在推送")
        pdf_name = pdf_path.split("/")[-1]
        mail_host = self.mail_host  # 设置服务器
        mail_user = self.mail_user  # 用户名
        mail_pass = self.mail_pass  # 口令
        # sender = '123@qq.com'
        receivers = self.receivers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = mail_user
        message['To'] = receivers[0]
        message['Subject'] = pdf_name
        # 邮件正文内容
        # message.attach(MIMEText('', 'plain', 'utf-8'))
        # 构造附件1，传送当前目录下的 test.txt 文件
        b = open(pdf_path, 'rb')
        att1 = MIMEApplication(b.read())
        b.close()
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        # 文件名中文时候用
        att1.add_header("Content-Disposition", "attachment", filename=("gbk", "", pdf_name))
        # 文件名英文时用
        # att1["Content-Disposition"] = 'attachment; filename="hzw947.pdf"'
        message.attach(att1)
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(mail_user, receivers, message.as_string())
            return "邮件发送成功"
        except smtplib.SMTPException:
            return "无法发送邮件"


if __name__ == '__main__':
    hzw().run()
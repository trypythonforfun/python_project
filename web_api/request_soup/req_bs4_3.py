#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import os
import logging
import json
import re

#入口网址
firstUrl = 'https://www.5442.com/keywords/gaoyuanyuantupian.html'
#设置图片目录
folder = 'gaoyuanyuan'

LOG_FORMAT = "%(levelname)s : %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

class GetPicture():
    ''' 下载指定链接图片 '''
    def __init__(self):
        '''just init'''
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = firstUrl  #要访问的网页地址
        self.next_url = ''  #下一个网页地址
        self.folder_path = folder  #设置图片要存放的文件目录
        self.picName = 0  #遍历所有图片链接，将图片保存到本地指定文件夹，图片名字用0，1，2...
        self.webNum = 1  #遍历所有下一页
        logging.debug('1.初始化')
        #logging.debug("This is a debug log.")
        #logging.info("This is a info log.")
        #logging.warning("This is a warning log.")
        #logging.error("This is a error log.")

    def do_request(self, url):
        '''返回网页的response'''
        self.r_page = requests.get(url, headers=self.headers)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        logging.debug('2.do_request code：' + str(self.r_page.status_code))


    def do_soup(self):
        '''指定使用lxml解析，lxml解析速度比较快，容错高'''
        self.soup_obj = BeautifulSoup(self.r_page.content, 'lxml')
        logging.debug('3.do_soup')

    def creat_fold(self):
        '''创建文件夹'''
        isExists = os.path.exists(self.folder_path)
        if not isExists:
            logging.info('创建名字叫做' + self.folder_path + '的文件夹')
            os.makedirs(self.folder_path)
            logging.info('创建成功！')
        else:
            logging.info('文件夹已经存在')

    def save_html(self):
        '''保存页面到本地'''
        with open('page.html', 'wb') as f_html:
            f_html.write(self.r_page.content)
        logging.info('保存page.html')

    def get_next_url(self):
        '''取得下个页面'''
        logging.debug('4.get_next_url')
        self.next_url = ''
        nexts = self.soup_obj.find_all('a')
        for next in nexts:
            if '下一页' in str(next):
                self.next_url = next['href']
        if self.next_url.strip() == '':
            logging.warning('next_url没有了')
            
    def save_img(self):
        '''保存图片到本地'''
        
        logging.debug('5.save_img')
        imgs = self.soup_obj.find_all('img')
        
        urls = []
        for img in imgs:
            if 'data-src' in str(img):
                urls.append(img['data-src'])
            else:
                urls.append(img['src'])
        
        for url in urls:#看下文章的图片有哪些格式，一一处理
            if url.endswith('jpg'):
                try:
                    r = requests.get(url, timeout=10)
                    t = os.path.join(self.folder_path, str(self.picName) + '.jpg')#指定目录
                    fw = open(t,'wb')  # 指定绝对路径
                    fw.write(r.content)#保存图片到本地指定目录
                    self.picName += 1
                    fw.close()
                    logging.info('图片' + str(self.picName) + '保存中')
                except Exception as e:
                    logging.error(str(e))
        logging.info('保存完成！')

    def get_pic(self):
        logging.info('*******处理第' + str(self.webNum) + '页*******')
        self.do_request(self.web_url)
        #self.save_html()
        self.do_soup()
        self.get_next_url()
        self.save_img()
        if self.next_url.strip() != '':
            self.web_url = self.next_url
            self.webNum += 1
            self.get_pic()

if __name__ == '__main__':
    beauty = GetPicture()  #创建类的实例
    beauty.creat_fold()  #建立文件夹
    beauty.get_pic()  #执行类中的方法

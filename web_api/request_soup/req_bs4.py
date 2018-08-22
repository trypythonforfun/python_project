#!/usr/local/bin/python3
from bs4 import BeautifulSoup
import requests
import os

class BeautifulPicture():

    def __init__(self):
        '''just init'''
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'http://www.cnblogs.com/nancyzhu/p/8146408.html'  #要访问的网页地址
        self.folder_path = '/Users/jack/Desktop/BeautifulPicture'  #设置图片要存放的文件目录
        print('1.创建类BeautifulPicture的实例')

    def do_request(self, url):
        '''返回网页的response'''
        self.r_page = requests.get(url, headers=self.headers)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        print('2.requests函数的状态：' + str(self.r_page.status_code))

    def do_soup(self):
        '''指定使用lxml解析，lxml解析速度比较快，容错高'''
        self.soup_obj = BeautifulSoup(self.r_page.content, 'lxml')
        print('4.获得soup')
        #print(self.soup_obj)

    def save_html(self):
        '''保存页面到本地'''
        with open('page.html', 'wb') as f_html:
            f_html.write(self.r_page.content)
        print('3.保存page.html')

    def save_img(self):
        '''保存图片到本地'''
        imgs = self.soup_obj.find_all('img')
        print('imgs')
        print(imgs)

        urls = []
        for img in imgs:
            if 'data-src' in str(img):
                urls.append(img['data-src'])
                print('data-src')
                print(img)
            else:
                urls.append(img['src'])
                print('src')
                print(img)

    def get_pic(self):
        self.do_request(self.web_url)
        self.save_html()
        self.do_soup()
        self.save_img()

if __name__ == '__main__':
    beauty = BeautifulPicture()  #创建类的实例
    beauty.get_pic()  #执行类中的方法
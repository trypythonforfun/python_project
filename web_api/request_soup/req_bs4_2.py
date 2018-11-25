#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import os

class BeautifulPicture():

    def __init__(self):
        '''just init'''
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://baike.baidu.com/item/%E6%9D%A8%E5%AD%90%E5%A7%97/10966877?fr=aladdin'  #要访问的网页地址
        self.folder_path = 'BeautifulPicture'  #设置图片要存放的文件目录
        self.domain = 'http://www.cnblogs.com'
        print('1.__init__')

    def do_request(self, url):
        '''返回网页的response'''
        self.r_page = requests.get(url, headers=self.headers)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        print('2.do_request code：' + str(self.r_page.status_code))

    def do_soup(self):
        '''指定使用lxml解析，lxml解析速度比较快，容错高'''
        self.soup_obj = BeautifulSoup(self.r_page.content, 'lxml')
        print('3.do_soup')

    def creat_fold(self, path):
        '''创建文件夹'''
        isExists = os.path.exists(path)
        if not isExists:
            print('4.1创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('4.1.1创建成功！')
        else:
            print('4.1文件夹已经存在')

    def save_html(self):
        '''保存页面到本地'''
        with open('page.html', 'wb') as f_html:
            f_html.write(self.r_page.content)
        print('3.保存page.html')

    def save_img(self):
        '''保存图片到本地'''
        print('4.save_img')
        imgs = self.soup_obj.find_all('img')

        self.creat_fold(self.folder_path)
        
        urls = []
        for img in imgs:
            if 'data-src' in str(img):
                urls.append(img['data-src'])
            else:
                urls.append(img['src'])
        print('4.2获取图片的urls')
        
        #遍历所有图片链接，将图片保存到本地指定文件夹，图片名字用0，1，2...
        i = 0
        for url in urls:#看下文章的图片有哪些格式，一一处理
            if url.startswith('//'):
                new_url = 'http:' + url
                r = requests.get(new_url)
            elif url.startswith('/') and url.endswith('gif'):
                new_url = self.domain + url
                r = requests.get(new_url)
            elif url.endswith('.png') or url.endswith('jpg') or url.endswith('gif'):
                r = requests.get(url)
            t = os.path.join(self.folder_path, str(i) + '.jpg')#指定目录
            fw = open(t,'wb')  # 指定绝对路径
            fw.write(r.content)#保存图片到本地指定目录
            i += 1
            #update_file(url,t)#将老的链接(有可能是相对链接)修改为本地的链接，这样本地打开整个html就能访问图片
            fw.close()
            print('4.3图片%d保存中'%i)
                
    def get_pic(self):
        self.do_request(self.web_url)
        #self.save_html()
        self.do_soup()
        self.save_img()
        print('5.处理完成！')

if __name__ == '__main__':
    beauty = BeautifulPicture()  #创建类的实例
    beauty.get_pic()  #执行类中的方法

#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
from lxml import etree

import os
import time
import logging
import json
import random
import threading
from concurrent.futures import ThreadPoolExecutor, wait, as_completed

#LOG设置
LOG_FORMAT = "%(levelname)s : %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

#入口网址
target_url = 'https://www.baidu.com'

#保存文件夹
my_folder = 'baidu'

header_list = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
]
retry_num = 1
my_header = {}
my_proxy = {}
web_url_list = []
pic_urls = []
executor = ThreadPoolExecutor(max_workers=4)
thread_list = []
main_part = 'https://www.baidu.com/'
middle_part= '' # mnzuop
next_part = ''  # 8264.html
pic_name_url = '' # 8264_2
pic_name_no = 1

def do_init():
    global my_proxy
    global my_header
    
    logging.info('1.初始化变量')
    with open('proxy.json', 'r') as proxy_file:
        json_dict = json.loads(proxy_file.read())
    proxy_list = json_dict['https']
    my_header['User-Agent'] = header_list[1]
    my_proxy['https'] = proxy_list[3]   #从代理列表中选取代理
    # ~ logging.debug(my_header)
    logging.debug(my_proxy)
    
    #logging.debug("This is a debug log.")
    #logging.info("This is a info log.")
    #logging.warning("This is a warning log.")
    #logging.error("This is a error log.")

def creat_fold():
    isExists = os.path.exists(my_folder)
    if not isExists:
        logging.info('2.创建名文件夹:' + my_folder)
        os.makedirs(my_folder)
        os.chdir(my_folder)
        logging.debug(os.getcwd())
    else:
        logging.info('2.文件夹已经存在')
        os.chdir(my_folder)
        logging.debug(os.getcwd())

def get_web_url():
    global target_url
    global web_url_list
    web_url_list = []
    logging.info('3.取得web url list')
    try:
        # ~ r_page = requests.get(web_url, headers=my_header, proxies=my_proxy, timeout=5)
        r_page = requests.get(target_url, headers=my_header, timeout=30)
        logging.info('get web url list code:' + str(r_page.status_code))
        soup_obj = BeautifulSoup(r_page.content, 'lxml') #指定使用lxml解析，lxml解析速度比较快，容错高
        
        pic_divs = soup_obj.find_all('div', class_='piclist')
        logging.info('pic_divs len:' + str(len(pic_divs)))
        # ~ logging.info(pic_divs)
        for div in pic_divs:
            div_as = div.find_all('a')
            logging.info('div_as len:' + str(len(div_as)))
            for div_a in div_as:
                web_url_list.append(div_a['href'])
        # ~ logging.info(web_url_list)

        del_list = []
        for i in range(len(web_url_list)):
            web_url_list[i] = main_part.rstrip('/') + web_url_list[i]
        # ~ logging.info(web_url_list)
        for j in range(len(web_url_list)):
            if web_url_list[j].count('/') != 4:
                del_list.append(j)
        for k in del_list:
            web_url_list.pop(k)
        logging.info(web_url_list)
        # ~ jsObj = json.dumps(web_url_list, indent=4)
        # ~ with open('web_url_list_after.json', 'w') as proxy_file:
            # ~ proxy_file.write(jsObj)
            
    except Exception as e:
        logging.error(str(e))

def get_pic_url(web_url):
    global pic_urls
    global main_part
    global middle_part
    global next_part
    global pic_name_url
    logging.info('4.取得pic list')
    pic_urls = []
    next_part = ''
    pic_name_url = ''
    try:
        # ~ r_page = requests.get(web_url, headers=my_header, proxies=my_proxy, timeout=5)
        r_page = requests.get(web_url, headers=my_header, timeout=30)
        # ~ logging.info('get url code:' + str(r_page.status_code))
        soup_obj = BeautifulSoup(r_page.content, 'lxml') #指定使用lxml解析，lxml解析速度比较快，容错高
        
        #取得pic urls
        pic_divs1 = soup_obj.find_all('div', class_='article')
        pic_divs2 = soup_obj.find_all('div', class_='tFocus_box')
        pic_divs = pic_divs1 + pic_divs2
        # ~ logging.info('pic_divs len:' + str(len(pic_divs)))
        for div in pic_divs:
            imgs = div.find_all('img')
            # ~ logging.info('imgs len:' + str(len(imgs)))
            for img in imgs:
                pic_urls.append(img['src'])
        # ~ logging.info(pic_urls)
        
        #取得next url
        next_spans = soup_obj.find_all('span', class_='next')
        if len(next_spans):
            for span in next_spans:
                next_a = span.find_all('a')
            next_str = str(next_a)
            next_part = next_str[next_str.find('href')+6:next_str.find('target')-2]
        else:
            logging.warning('没有下一页！')
        # ~ logging.info('next_part:' + next_part)
    except Exception as e:
        logging.error(str(e))
        
    middle_part = web_url.replace(main_part,'')
    middle_part = middle_part[0:middle_part.find('/')]
    pic_name_url = web_url[web_url.find('org')+5+len(middle_part):web_url.find('html')-1]

def save_picture(pic_url):
    global pic_name_no
    global pic_name_url
    logging.info('5.保存图片')
    # ~ logging.info(threading.activeCount())
    # ~ logging.info(threading.currentThread())
    try:
        # ~ r_page = requests.get(pic_url, headers=my_header, proxies=my_proxy, timeout=5)
        r_pic = requests.get(pic_url, headers=my_header, timeout=30)
        logging.debug(r_pic.status_code)
        pic_name = pic_name_url + '_' + str(pic_name_no) + '.jpg'
        with open(pic_name,'wb') as fw:
            fw.write(r_pic.content)#保存图片到本地指定目录
            fw.flush()
        logging.info('图片' + pic_name + '保存中')
        pic_name_no += 1
    except Exception as e:
        logging.error(str(e))

def download_manager(web_url):
    global executor
    global thread_list
    
    logging.info('处理网页：' + web_url)
    get_pic_url(web_url)
    for pic_url in pic_urls:
        thread_list.append(executor.submit(save_picture,pic_url))
        wait(thread_list)
        # ~ save_picture(pic_url)
    if next_part.strip():   #有下一页
        web_url = main_part + middle_part + '/' + next_part
        download_manager(web_url)

def download_list():
    global web_url_list
    for web_url in web_url_list:
        download_manager(web_url)
    
    
if __name__ == '__main__':
    start_time = time.time()
    do_init()
    creat_fold()
    get_web_url()
    download_list()
    # ~ jsObj = json.dumps(pic_urls[0], indent=4)
    # ~ with open('pic_url.json', 'w') as proxy_file:
        # ~ proxy_file.write(jsObj)
    # ~ executor = ThreadPoolExecutor(max_workers=2)
    # ~ thread_list = []
    # ~ use_json()
    # ~ if get_proxy() == True:
        # ~ check_proxy('http')
        # ~ check_proxy('https')
        # ~ future_http = executor.submit(check_proxy,'http')
        # ~ thread_list.append(future_http)
        # ~ future_https = executor.submit(check_proxy,'https')
        # ~ thread_list.append(future_https)
        # ~ wait(thread_list)
        # ~ as_completed(future_http)
        # ~ as_completed(future_https)
        # ~ save_json()
    end_time = time.time()
    print('--'*30)
    print('耗时:' + str(end_time-start_time))

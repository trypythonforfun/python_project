# -*- coding: UTF-8 -*-    
import threading, requests, datetime
from bs4 import BeautifulSoup
import random
import queue
from time import ctime,sleep
import threadpool
from concurrent.futures import ThreadPoolExecutor

URLS = ['http://www.163.com', 'https://www.baidu.com/', 'https://github.com/']
def load_url(url):
    with urllib.request.urlopen(url, timeout=60) as conn:
        print('%r page is %d bytes' % (url, len(conn.read())))

executor = ThreadPoolExecutor(max_workers=3)

for url in URLS:
    future = executor.submit(load_url,url)
    print(future.done())

print('主线程')

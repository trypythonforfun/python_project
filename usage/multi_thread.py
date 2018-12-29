# -*- coding: UTF-8 -*-    
import threading, requests, datetime
from bs4 import BeautifulSoup
import random
import queue
from time import ctime,sleep
import threadpool
from concurrent.futures import ThreadPoolExecutor

def music(func):
    for i in range(2):
        print("I was listening to music." + func + ctime())
        sleep(2)

def move(func):
    for i in range(2):
        print("I was at the movies.", func, ctime())
        sleep(3)

threads = []
t1 = threading.Thread(target=music,args=('music_name',))
threads.append(t1)
t2 = threading.Thread(target=move,args=('move_name',))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    
    t.join()
        
    print("all over!", ctime()) 

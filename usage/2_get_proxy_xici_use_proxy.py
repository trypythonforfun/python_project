import requests
from lxml import etree
import time
import json
import random

proxy_list_http = []
proxy_list_https = []
valid_proxy_list_http = []
valid_proxy_list_https = []
json_dict = {}
retry_num = 3
my_headers = [
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
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

def use_json():
    global json_dict
    proxy_dictionary = {}
    proxy_dictionary['http'] = valid_proxy_list_http
    proxy_dictionary['https'] = valid_proxy_list_https
    jsObj = json.dumps(proxy_dictionary, indent=4)
    with open('proxy1.json', 'r') as proxy_file:
        json_dict = json.loads(proxy_file.read())
    
def get_proxy():
    global retry_num
    url = 'http://www.xicidaili.com/nn/1'

    # ~ headers = {
        # ~ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    # ~ }
    headers = {'User-Agent': random.choice(my_headers)}
    proxy_dict = {'http': random.choice(json_dict['http']),}
    try:
        response = requests.get(url, proxies=proxy_dict, headers=headers, timeout=5)
        # ~ response = requests.get(url, headers=headers)
        if response.status_code != 200:
            retry_num -= 1
            print('retry_num:',retry_num)
            if retry_num != 0:
                get_proxy()
            else:
                return False
    except:
        retry_num -= 1
        print('retry_num:',retry_num)
        if retry_num != 0:
            get_proxy()
        else:
            return False
        
    html_ele = etree.HTML(response.text)
    
    ip_eles = html_ele.xpath('//table[@id="ip_list"]/tr/td[2]/text()')
    port_eles = html_ele.xpath('//table[@id="ip_list"]/tr/td[3]/text()')
    type_eles = html_ele.xpath('//table[@id="ip_list"]/tr/td[6]/text()')

    for i in range(0,len(ip_eles)):
        # proxy_str = 'http://' + ip_eles[i] + ':' + port_eles[i]
        proxy_str = type_eles[i].lower() +  '://' + ip_eles[i] + ':' + port_eles[i]
        if type_eles[i].lower() == 'http':
            proxy_list_http.append(proxy_str)
        elif type_eles[i].lower() == 'https':
            proxy_list_https.append(proxy_str)
        else :
            pass
            
    return True
    
def check_proxy(type_proxy):
    url = 'http://www.baidu.com/s?wd=ip'
    urls = 'https://www.baidu.com/s?wd=ip'
    if type_proxy == 'http' :
        for proxy in proxy_list_http:
            proxy_dict = {
                'http': proxy
            }
            try:
                response = requests.get(url, proxies=proxy_dict, timeout=3)
                if response.status_code == 200:
                    print('http代理可用：' + proxy)
                    # ~ print('proxy_dict:',proxy_dict)
                    valid_proxy_list_http.append(proxy)
                else:
                    print('代理超时')
            except:
                pass
                #print('代理不可用--------------->')
        
    elif type_proxy == 'https' :
        for proxy in proxy_list_https:
            proxy_dict = {
                'https': proxy
            }
            try:
                response = requests.get(urls, proxies=proxy_dict, timeout=3)
                if response.status_code == 200:
                    print('https代理可用：' + proxy)
                    valid_proxy_list_https.append(proxy)
                else:
                    print('代理超时')
            except:
                pass
                #print('代理不可用--------------->')
        
    else :
        print('type_proxy输入错误--------------->')

def save_json():
    proxy_dictionary = {}
    proxy_dictionary['http'] = valid_proxy_list_http
    proxy_dictionary['https'] = valid_proxy_list_https
    jsObj = json.dumps(proxy_dictionary, indent=4)
    # ~ proxy_file = open('proxy.json', 'w')
    with open('proxy.json', 'w') as proxy_file:
        proxy_file.write(jsObj)  
        # ~ proxy_file.close()

if __name__ == '__main__':
    start_time = time.time()
    use_json()
    if get_proxy() == True:
        check_proxy('http')
        check_proxy('https')
        save_json()
    end_time = time.time()
    print('--'*30)
    print('耗时:' + str(end_time-start_time))

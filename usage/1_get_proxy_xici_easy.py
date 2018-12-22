import requests
from lxml import etree
import time
import json

proxy_list_http = []
proxy_list_https = []
valid_proxy_list_http = []
valid_proxy_list_https = []

def get_proxy():
    url = 'http://www.xicidaili.com/nn/1'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    proxy_dict = {'http': 'http://171.113.38.160:8888'}
                        # ~ "http://115.222.10.198:80",
                        # ~ "http://61.135.217.7:80",
                        # ~ "http://171.37.162.92:8123",
                        # ~ "http://114.223.163.70:8118",
                        # ~ "http://61.176.223.7:58822"
    
    # ~ response = requests.get(url, proxies=proxy_dict, headers=headers)
    response = requests.get(url, headers=headers)

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
                    print('proxy_dict:',proxy_dict)
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
                    print('proxy_dict:',proxy_dict)
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
    proxy_file = open('proxy1.json', 'w')
    proxy_file.write(jsObj)  
    proxy_file.close() 

if __name__ == '__main__':
    start_time = time.time()
    get_proxy()
    check_proxy('http')
    check_proxy('https')
    save_json()
    end_time = time.time()
    print('--'*30)
    print('耗时:' + str(end_time-start_time))

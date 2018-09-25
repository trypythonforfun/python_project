from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/page1.html")
print(html.read())
bsObj = BeautifulSoup(html.read(),'lxml')
print(bsObj.h1)

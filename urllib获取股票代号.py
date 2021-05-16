import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import shutil
import sys
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        fp = urllib.request.urlopen(request)
        html = fp.read().decode('gbk') 
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    soup = BeautifulSoup(html,features="lxml")
    return soup


def parseData(soup):
    num_data_raw = soup.find_all("td",{"class":"e1"})
    num_data = []
    name_data_raw = soup.find_all("td",{"class":"e2"})
    name_data = []
    # pattern = re.compile(r'\d+')
    for item in num_data_raw:
        item = str(item)
        cp = re.search(r'[\d]{6,6}',item)
        if cp != None:
            num_data.append(cp.group(0))
    for item in name_data_raw:
        item = str(item)
        cp = re.search(r'k">.*</a>',item)
        if cp != None:
            name_data.append(cp.group(0)[3:-4])
    return num_data, name_data

def getURL(url):
    base = 'https://q.stock.sohu.com/cn/'
    soup = askURL(url)
    tail = []
    url_raw = soup.find_all("td",{"class":"e2"})
    for item in url_raw:
        item = str(item)
        cp = re.search(r'href="bk.*shtml',item)
        if cp != None:
            tail.append(base + cp.group(0)[6:-1])
    return tail

def main():
    tail = getURL(r'https://q.stock.sohu.com/cn/bk.shtml')[0:50]
    num = []
    name = []
    for item in tail:
        soup = askURL(item)
        num_tmp, name_tmp = parseData(soup)
        num.append(num_tmp)
        name.append(name_tmp)
    
    num_new = np.array(sum(num,[]))
    name_new = np.array(sum(name,[]))
    df = pd.DataFrame({'code':num_new, 'stock':name_new})
    df.to_csv("股票代号及其股票名.csv",index=False,sep=',', encoding='gbk')
    #为了避免scrapy操作的时候找不到相关csv文件，先提前复制好
    try:
        shutil.copy('股票代号及其股票名.csv', 'stock_history/stock_history/spiders')
        shutil.copy('股票代号及其股票名.csv', 'stock_history/stock_history')
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())

if __name__ == '__main__':
    main()

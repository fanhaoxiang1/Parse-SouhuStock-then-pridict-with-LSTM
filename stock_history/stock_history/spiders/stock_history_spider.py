import scrapy
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import random

class StockHistoryFileItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()

class StockHistorySpider(scrapy.Spider):
    collection = 'stock_list'
    name = 'stock_history_spider'
    headers = {
		'Referer': 'http://quotes.money.163.com/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
        }
    def __init__(self):
        scrapy.Spider.__init__(self)
        self.df = pd.read_csv('股票代号及其股票名.csv', encoding = 'gbk', converters = {'code':str})
        self.stock_list = self.df['code'][0:200]
        self.current_code = ''
    def start_requests(self):
        for code in list(self.stock_list):
            self.current_code = code
            url = 'http://quotes.money.163.com/trade/lsjysj_{}.html'.format(self.current_code)
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)
            
    def parse(self, response):
        text = response.text
        soup = bs(text, 'lxml')
        start_time = soup.find('input', {'name': 'date_start_type'}).get('value').replace('-', '')
        end_time = soup.find('input', {'name': 'date_end_type'}).get('value').replace('-', '')
        time.sleep(random.choice([1, 2]))
        file_item = StockHistoryFileItem()
        if len(self.current_code) > 0:
            stock_code = str(self.current_code)
            if int(stock_code[0]) in [0, 2, 3, 6, 9]:
                if int(stock_code[0]) in [6, 9]:
                    new_stock_code = '0' + stock_code
                if int(stock_code[0]) in [0, 2, 3]:
                    if not int(stock_code[0:3]) in [201, 202, 203, 204]:
                        new_stock_code = '1' + stock_code
            download_url = "http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP".format(new_stock_code, start_time, end_time)
            file_item['file_urls'] = [download_url]
            yield file_item
import os
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('股票代号及其股票名.csv', encoding = 'gbk', converters = {'code':str})
    stock_list = list(df['code'][0:200])
    name_list = list(df['stock'][0:200])
    d = dict(zip(stock_list,name_list))
    path = 'stock_history\\stock_history\\history_data'
    FileList = os.listdir(path)
    for file in FileList:
        name = file[1:7]
        if d[name][0] == '*':
            d[name] = d[name][1:]
        try:
            os.rename(path + '\\' + file, path + '\\' + name + d[name] + '.csv')
        except Exception as e:
            print(e)
            print('rename file fail\r\n')
        else:
            print('rename file success\r\n')
                

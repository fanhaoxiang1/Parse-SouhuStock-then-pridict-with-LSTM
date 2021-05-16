python版本：python3.8

# 必要插件及测试时版本：
numpy     1.18.5
pandas     1.0.5
urllib3      1.25.9
Beautifulsoup4    4.9.1
scikit-learn    0.23.1 （尽量保证版本相近，不同版本指令差异较大）
tensorflow-gpu    2.3.1（tensorflow也可以替代）
Keras     2.4.3
matplotlib    3.2.2

# 运行顺序：
## 先阅读目录下的docx文件
## 为了方便理解，我录制了一个长约10分钟的介绍视频，包含了第二部分的大部分内容，以下是视频链接：https://www.bilibili.com/video/bv1cT4y1M78m （可以采用1.25倍速观看）

## 1.运行pythonDesign下的urllib获取股票代号.py
## 2.scrapy 爬虫
    1）运行cmd，cd + 保存路径\pythonDesign\stock_history\stock_history
    2）输入 scrapy crawl stock_history_spider
    3）数据保存在  保存路径\pythonDesign\stock_history\stock_history\history_data

## 3.运行pythonDesign路径目录下的stock_csv文件名更改.py
## 4.运行pythonDesign下的RNN神经网络-LSTM股票预测.py

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline


class StockHistoryPipeline:
    def process_item(self, item, spider):
        return item



class SelfDefineFilePipline(FilesPipeline):
    """
    继承FilesPipeline，更改其存储文件的方式
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def file_path(self, request, response=None, info=None):
        str_temp = str(request.url)
        name = str_temp[54:61]
        name = name + '.csv'
        return name
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd

items = [] #collection of returned items

class WicompcostPipeline:   
    def process_item(self, item, spider):
        items.append(item)
        

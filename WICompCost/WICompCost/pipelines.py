# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd

class WicompcostPipeline:
    def process_item(self, item, spider):
        df = pd.DataFrame.from_dict(item)
        print(df) #unwrap and print the dataframe to verify function
        #result.append(dict(item))
        return df

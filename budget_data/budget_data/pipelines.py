# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import hashlib
import mimetypes
from pathlib import Path

from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
from scrapy.http.request import NO_CALLBACK

items = [] #collection of returned items


class BudgetDataPipeline(FilesPipeline):

   def file_path(self, request, response=None, info=None, *, item=None):
      media_guid = request.url
      file_name = media_guid.rsplit('/',1)[1]
      #2013 filepath starts with random 'd' for some reason, this removes it
      if file_name.startswith('d'):
         file_name = file_name[1:]
      #from 2018 and newer, descriptions filename and type changes.  below checks for new
      #filename, and change it to match the rest of the files before saving
      if "COA" in file_name:
         file_name= file_name.split('_',1)[1]
         #capture first year, which matches first 4 characters
         year = int(file_name[:4])
         next_year = year+1
         file_name = str(year) + "-"+ str(next_year) +"-01-Budget-Accout-Descriptions.xlsx"
         print("\n\n",file_name)
      return f"full/{file_name}"
   
   #def process_item(self, item, spider):
   #     items.append(item)
   
   
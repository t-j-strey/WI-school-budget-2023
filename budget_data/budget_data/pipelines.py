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
      print("\n\nFile Name: ",file_name)
      return f"full/{file_name}"

   def get_media_requests(self, item, info):
      urls = ItemAdapter(item).get(self.files_urls_field, [])
      print("\n\n\n URL: ",urls)
      return [scrapy.Request(u, callback=NO_CALLBACK) for u in urls]
   
   #def process_item(self, item, spider):
   #     items.append(item)
   
   
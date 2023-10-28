# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline

items = [] #collection of returned items


class BudgetDataPipeline(FilesPipeline):
   def file_path(self, request, response=None, info=None):
      print('!!!!!!!!!!!!!!!!!!!!!!!!!')
      file_url = request.meta['file_urls'] +'description'
      print('\nFile Name: ',file_url)
      files = request.meta['files']
      return '%s.csv' % (file_url)

   def get_media_requests(self, item, info):
      print('- - - - - - - - - - - - - - - - - -')
      urls = item['file_urls']
      for each in item['file_urls']:
         print ("\nEach Item: ",each)
         yield  scrapy.Request(url=each)  

         print("\n\n\n Renaming file...")
      
   #   print("\nResulting file URL: ",url)
      #return request.meta.get('filename','')
   


   #def process_item(self, item, spider):
   #     items.append(item)
   
   
import scrapy
from scrapy import FormRequest
from scrapy.shell import inspect_response

class CompcostSpider(scrapy.Spider):
    name = "compcost"
    allowed_domains = ["x"]
    start_urls = ["https://sfs.dpi.wi.gov/sfsdw/CompCostReport.aspx"]

    def parse(self, response):
        headers = {
            'Content-Type': 'text/html; charset=utf-8'
        }

        formdata= {
            '__EVENTTARGET'	: 'ctl00$MainContent$selFiscalYear',
        }
        yield FormRequest.from_response(response,
                                  formdata=formdata,
                                  headers=headers,
                                  callback=self.tab2)
        
    def tab2(self,response):
        inspect_response(response,self)

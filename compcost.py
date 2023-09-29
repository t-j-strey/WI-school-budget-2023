import scrapy
from scrapy import FormRequest
from scrapy.shell import inspect_response

class CompcostSpider(scrapy.Spider):
    name = "compcost"
    #allowed_domains = ["https://sfs.dpi.wi.gov"]
    start_urls = ["https://sfs.dpi.wi.gov/sfsdw/CompCostReport.aspx"]

    def parse(self, response):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        formdata= {
            '__EVENTTARGET' : '',
            '__EVENTARGUMENT':'',
            '__VIEWSTATEGENERATOR' : 'E4E6F4A2',
            'ctl00$MainContent$selFiscalYear' : '2022',
            'ctl00$MainContent$selSchoolDist' : '0007',
            'ctl00$MainContent$rbOrderListBy':	'Name',
            'ctl00$MainContent$btnSubmitAllAgencies':	'Show+All+Agencies',
            'ctl00$MainContent$SortValue':	'NAME',
            'ctl00$MainContent$SortOrder':	'ASC'
        }
        inspect_response(self,response)
        #yield FormRequest.from_response(response,
        #                          formdata=formdata,
        #                          headers=headers,
        #                          callback=self.tab2)
       
       

    def tab2(self,response):
        inspect_response(response,self)
        print("Tab2Running")

import scrapy
from scrapy import FormRequest
from scrapy.shell import inspect_response

class CompcostSpider(scrapy.Spider):
    name = "compcost"
    start_urls = ["https://sfs.dpi.wi.gov/sfsdw/CompCostReport.aspx"]

    custom_settings = {
        'FEEDS' : {'data/%(name)s/%(name)s_%(time)s.csv': {'format':'csv','overwrite':True}}
    }

    def parse(self, response):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        formdata= {
            'ctl00$MainContent$selFiscalYear' : '2021',
            'ctl00$MainContent$selSchoolDist' : '0007',
            'ctl00$MainContent$rbOrderListBy':	'Name',
            'ctl00$MainContent$btnSubmitAllAgencies':	'Show+All+Agencies',
        }
        yield FormRequest.from_response(response,
                                  formdata=formdata,
                                  headers=headers,
                                  callback=self.tab2)
        
       
    def datacapture(self,response):
        for resp in response.xpath('/html/body/form/div[2]/div[3]/div/table/tbody/tr[1]/td[1]'):
            data = {"data":resp.get()}
            yield data


    def tab2(self,response):
        inspect_response(response,self)

import scrapy
from scrapy import FormRequest
from scrapy.shell import inspect_response
import pandas as pd

class CompcostSpider(scrapy.Spider):
    name = "compcost"
    start_urls = ["https://sfs.dpi.wi.gov/sfsdw/CompCostReport.aspx"]

    custom_settings = {
        #'FEEDS' : {'data/%(name)s/%(name)s_%(time)s.csv': {'format':'csv','overwrite':True}}
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
                                  callback=self.datacapture)
                                  #callback=self.tab2)
        
        
       
    def datacapture(self,response):
        #dfs = pd.read_html(response.text)
        dfs = pd.read_html(response,match='Data For Comparative Cost Per Member')
        #dfs = pd.read_html(response,attrs={'id':'ct100_MainContent_Grid_StandardReport'})
        writer = pd.ExcelWriter('data.xlsx',engine='xlsxwriter')
        dfs[0].to_excel(writer,index = False, header = True)
       

    

    def tab2(self,response):
        inspect_response(response,self)

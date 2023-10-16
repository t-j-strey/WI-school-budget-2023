import scrapy
from scrapy import FormRequest
import pandas as pd
import numpy as np


class CompcostSpider(scrapy.Spider):
    name = "compcost"
    allowed_domains = ["sfs.dpi.wi.gov"]
    start_urls = ["https://sfs.dpi.wi.gov/sfsdw/CompCostReport.aspx"]
    custom_settings = {
        'FEEDS' : {
            'output.csv' : {
                'format': 'csv'
            }
        }
    }
    year = 2021
    stryear = str(year)

    def parse(self, response):
        headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
        formdata= {
            'ctl00$MainContent$selFiscalYear' : self.stryear,
            'ctl00$MainContent$selSchoolDist' : '0007',
            'ctl00$MainContent$rbOrderListBy':	'Name',
            'ctl00$MainContent$btnSubmitAllAgencies':	'Show+All+Agencies',
        }
        return FormRequest.from_response(response,
                                formdata=formdata,
                                headers=headers,
                                callback=self.datacapture)
                               
    def datacapture(self,response):
        dfs = pd.read_html(response.text)
        df = dfs[3]
        length = len(df.index)
        yrdata = np.full((length),self.year)
        df.insert(1,"Year",yrdata)
        print(df)
        yield df
        

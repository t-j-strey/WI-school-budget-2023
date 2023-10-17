import scrapy
from scrapy import FormRequest,Request
import pandas as pd
import numpy as np
import io
import logging


class CompcostSpider(scrapy.Spider):
    name = "compcost"

    def __init__(self,year=None, stdreport="", *args, **kwargs):
        super(CompcostSpider,self).__init__(*args,**kwargs)
        self.stryear = year
        self.url = stdreport
        logging.getLogger('scrapy').setLevel(logging.WARNING)

    def start_requests(self):
        yield Request(self.url,self.parse)

    allowed_domains = ["sfs.dpi.wi.gov"]
    #start_urls = ["https://sfs.dpi.wi.gov/sfsdw/CompCostReport.aspx"]
    custom_settings = {
    #    'FEEDS' : {
    #        'CompCostout.csv' : {
    #            'format': 'csv'
    #        }
    #    }
    }
    
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
        iostring = io.StringIO(response.text)
        dfs = pd.read_html(iostring)
        df = dfs[3]
        length = len(df.index)
        yrdata = np.full((length),self.stryear)
        df.insert(1,"Year",yrdata)
        print(df)
        yield df

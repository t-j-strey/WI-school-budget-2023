import scrapy
from scrapy import FormRequest,Request
import pandas as pd
import numpy as np
import io
import logging


class StdReportsSpider(scrapy.Spider):
    name = "std_reports_spider"
    def __init__(self,year=None, stdreport="", *args, **kwargs):
        super(StdReportsSpider,self).__init__(*args,**kwargs)
        self.stryear = year
        self.url = stdreport
        logging.getLogger('scrapy').setLevel(logging.WARNING)

    def start_requests(self):
        yield Request(self.url,self.parse)

    allowed_domains = ["sfs.dpi.wi.gov"]
    custom_settings = {}
    
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

        #add a column to the dataframe indicating which year the data is from
        yrdata[0] = ""
        yrdata[1] = "Year"
        df.insert(1,"",yrdata) #add year # to column 1

        #split the district name column so there is a separate column fro the name and the ID#
        df_district = df[0].str.split('(',expand=True)
        df_district[1] = df_district[1].str.replace(r'\D','',regex=True)
        df.insert(1,"ID",df_district[1])
        df.insert(1,"Name",df_district[0])
        df.drop(df.columns[0],axis=1,inplace=True)
        #format the column header cell text to reflect new data
        df.iloc[0,0] = ""
        df.iloc[1,0] = "District Name"
        df.iloc[1,1] = "District ID"

        yield df.to_dict()
        

import scrapy
from scrapy import FormRequest,Request
import pandas as pd
import numpy as np
import io
import logging
from scrapy.shell import inspect_response



class DistProfilesSpdrSpider(scrapy.Spider):
    name = "dist_profiles_spdr"
    allowed_domains = ["sfs.dpi.wi.gov"]
    start_urls = ["https://sfs.dpi.wi.gov/sfsdw/Agency_Financial_profile.aspx"]

    def __init__(self,year=None, stdreport="", *args, **kwargs):
        super(DistProfilesSpdrSpider,self).__init__(*args,**kwargs)
        self.stryear = year
        logging.getLogger('scrapy').setLevel(logging.WARNING)

        #def start_requests(self):
        #yield Request(self.url,self.parse)

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
            'ctl00$MainContent$btnSubmitAllAgencies':	'Show+Agency+Profile',
        }
        return FormRequest.from_response(response,
                                formdata=formdata,
                                headers=headers,
                                #callback=self.datacapture)
                                callback = self.tab2)
    
    def datacapture(self,response):
        iostring = io.StringIO(response.text)
        dfs = pd.read_html(iostring)
        #Re-arrange Code-and-class table such that it is in 2 columns
        df1 = dfs[2]
        df2 = df1[[2,3]].copy()
        df2.columns = ['Attribute','Value']
        df1 = df1.drop(df1.columns[[2,3]],axis = 1)
        df1.columns = ['Attribute','Value']
        frame = [df1,df2]
        candc = pd.concat(frame)
        #pull only current year data from table
        df3 = dfs[3]
        df3.drop(df3.columns[[2,3,4,5]],axis=1,inplace = True)
        df3.rename(columns={df3.columns[0]:'Attribute'},inplace = True)
        df3.rename(columns={df3.columns[1]:'Value'},inplace = True)
        result = [candc,df3]
        out = pd.concat(result) # this is stitched frame, containing all current year data
        #print("\nOutput Dataframe: ",out)
        length = len(out.index)
        yrdata = np.full((length),self.stryear)

        #add a column to the dataframe indicating which year the data is from
        yrdata[0] = "Year"
        out.insert(1,"",yrdata) #add year # to column 1
        #print("\nOutput Dataframe: ",out)
        rawschool = response.selector.xpath('//html/body/form/div[4]/div[2]/h2').extract()
        print("\nSchool Name: ",rawschool)

        #split the district name column so there is a separate column fro the name and the ID#
    #    df_district = df[0].str.split('(',expand=True)
    #    df_district[1] = df_district[1].str.replace(r'\D','',regex=True)
    #    df.insert(1,"ID",df_district[1])
    #    df.insert(1,"Name",df_district[0])
    #    df.drop(df.columns[0],axis=1,inplace=True)
        #format the column header cell text to reflect new data
    #    df.iloc[0,0] = ""
    #    df.iloc[1,0] = "District Name"
    #    df.iloc[1,1] = "District ID"

    #    yield df.to_dict()

    def tab2(self,response):
        inspect_response(response,self)
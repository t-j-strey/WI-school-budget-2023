import scrapy
from scrapy import FormRequest,Request
import pandas as pd
import numpy as np
import io
import logging
from scrapy.shell import inspect_response

class ProfileInitItem(scrapy.Item):
    years = scrapy.Field()
    district = scrapy.Field()
            

class DistProfilesSpdrSpider(scrapy.Spider):
    name = "dist_profiles_spdr"
    allowed_domains = ["sfs.dpi.wi.gov"]
    start_urls = ["https://sfs.dpi.wi.gov/sfsdw/Agency_Financial_profile.aspx"]

    def __init__(self,year=None,district = None, init = False, stdreport="", *args, **kwargs):
        super(DistProfilesSpdrSpider,self).__init__(*args,**kwargs)
        self.stryear = year
        self.strdist = district
        self.init = init
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
            'ctl00$MainContent$selSchoolDist' : self.strdist,
            'ctl00$MainContent$rbOrderListBy':	'Name',
            'ctl00$MainContent$btnSubmitAllAgencies':	'Show+Agency+Profile',
        }


        if not self.init:
            yield FormRequest.from_response(response,
                                    formdata=formdata,
                                    headers=headers,
                                    callback=self.datacapture)
                                    #callback = self.tab2)
        else:
            district_list = list()
            years_list = list()
            for district in response.xpath('//*[@id="ctl00_MainContent_selSchoolDist"]/option/@value').extract():
                district_list.append(district)
            for year in response.xpath('//*[@id="ctl00_MainContent_selFiscalYear"]/option/@value').extract():
                years_list.append(year)
            item = ProfileInitItem(years=years_list,district=district_list)
            yield item
            
            
                                     


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
        df3.drop(index = [0,16,20,25],inplace = True)
        result = [candc,df3]
        dfcmplt = pd.concat(result) # this is stitched frame, containing all current year data
        out = dfcmplt.T #transpose so it is a single row of relevant data
        length = len(out.index)
        yrdata = np.full((length),self.stryear)

        #add a column to the dataframe indicating which year the data is from
        yrdata[0] = "Year"
        out.insert(0,"",yrdata) #add year # to column 1
        rawschool = response.xpath("//html/body/form/div[2]/div[2]/h2/text()").get()
        district, sep, tail = rawschool.partition(')')
        name, sep, id = district.partition('(')
        #create arrays full of the district name and ID
        namedata = np.full((length),name)
        iddata = np.full((length),id)
        out.insert(0,"ID",iddata)
        out.insert(0,"Name",namedata)
        #format the column header cell text to reflect new data
        #out.iloc[0,0] = ""
        out.iloc[0,0] = "District Name"
        out.iloc[0,1] = "District ID"
        #rename the column indexes so they are unique
        out.columns=[str(i) for i in range(out.shape[1])]

        yield out.to_dict()

    def tab2(self,response):
        inspect_response(response,self)
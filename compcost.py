import scrapy
from scrapy import FormRequest
from scrapy.shell import inspect_response
import pandas as pd
import numpy as np

class CompcostSpider(scrapy.Spider):
    name = "compcost"
    start_urls = ["https://sfs.dpi.wi.gov/sfsdw/CompCostReport.aspx"]

    custom_settings = {
        #'FEEDS' : {'data/%(name)s/%(name)s_%(time)s.csv': {'format':'csv','overwrite':True}}
    }

    CostCompDF = pd.DataFrame()

    for yrs in range(2020,2021): 
        stryears = str(yrs)
        
        def parse(self, response):
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            formdata= {
                'ctl00$MainContent$selFiscalYear' : self.stryears,
                'ctl00$MainContent$selSchoolDist' : '0007',
                'ctl00$MainContent$rbOrderListBy':	'Name',
                'ctl00$MainContent$btnSubmitAllAgencies':	'Show+All+Agencies',
            }
            print("\n\n")
            print("FormRequest Command next")
            print("\n\n")
            return FormRequest.from_response(response,
            #results = FormRequest.from_response(response,
                                    formdata=formdata,
                                    headers=headers,
                                    callback=self.datacapture)
                                    #callback=self.tab2)
            print("\n\n")
            print("FormRequest Commanded")
            print("\n\n")



        print("\n\n")
        print("FormRequest Complete")
        #print(self.CompCostDF)
        print("\n\n")

    def datacapture(self,response):
        dfs = pd.read_html(response.text)
        print("\n\n")
        print("datacapture")
        print(dfs[3])
        print("\n\n")
        CompCostDF = CompCostDF.append(dfs[3])
        print("\n\n")
        print("appended Data")
        print(CompCostDF)
        print("\n\n")
        #yield dfs[3]


     #   length = len(df.index)
     #   yrdata = np.full((length),self.yrs)
     #   df.insert(1,"Year",yrdata)
        #dfs = pd.read_html(response,attrs={'id':'ctl00_MainContent_Grid_StandardReport'})
        
        
    #with pd.ExcelWriter(
    #    "CompCostPerMember.xlsx",
    #    engine = 'openpyxl',
    #    mode ='w'
    #) as writer:
    #    self.results.to_excel(writer,
    #                    sheet_name='Comp Cost Per Member',
    #                    index = False, 
    #                    header = True, 
    #                    merge_cells=True
    #                    )
           

        

    

    def tab2(self,response):
        inspect_response(response,self)


from twisted.internet import reactor, defer
from budget_data.budget_data.spiders.budget_data_spdr import BudgetDataSpdrSpider
from budget_data.budget_data import pipelines as budget_data_pipeline
from budget_data.budget_data.settings import FILES_STORE
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import os
import pandas as pd
#from excel_utils import export_dist_profiles
from scrapy.utils.log import configure_logging
from pathlib import Path


PROJECT_ROOT =  os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)

def main():

    configure_logging(
        {"LOG_LEVEL":"INFO"}
    )
    start_year = 2012
    end_year = 2019
    settings_file_path = 'budget_data.budget_data.settings'   #Relative Location of Settings File
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE',settings_file_path)
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    #@defer.inlineCallbacks #type: ignore
    #def crawl():
    #    yield runner.crawl(BudgetDataSpdrSpider)
    #    reactor.stop() # type: ignore      
    #crawl()  
    #reactor.run() # type: ignore
    out = pd.DataFrame()

    for i in range(start_year,end_year+1):
        print("\n\n i: ",i)
        #format description files to generate consistent dataframe.  format changes over the years
        if i >= 2012 and i <=2013:
            desc_file = FILES_STORE + '\\full\\'+ str(i) + '-' + str(i+1) + '-Budget-Account-Descriptions.csv'
            df_desc = pd.read_csv(desc_file,encoding = "ISO-8859-1",dtype=str)
            cols_name = ['Account Number','Description']
            df_desc.columns = cols_name
            df_desc_rdy = df_desc
           

        elif i > 2013 and i <= 2017:
            desc_file = FILES_STORE + '\\full\\'+ str(i) + '-' + str(i+1) + '-Budget-Account-Descriptions.csv'
            df_desc = pd.read_csv(desc_file,encoding = "ISO-8859-1",dtype=str)
            df_desc.drop(df_desc.columns[[0,1]],axis = 1, inplace=True)
            cols_name = ['Account Number','Description']
            df_desc.columns = cols_name
            df_desc_rdy = df_desc
           

        elif i >= 2018:
            desc_file = FILES_STORE + '\\full\\'+ str(i) + '-' + str(i+1) + '-Budget-Account-Descriptions.xlsx'
            df_temp = pd.read_excel(desc_file,index_col=None,dtype=str)
            df_temp.drop(df_temp.columns[[0,1,2,8]],axis=1,inplace=True)
            #rename the columns so they are consistent each year
            cols_name = ['Fund','Account Type','Function','Subfunction','Object/Source','Description']
            df_temp.columns = cols_name
            cols_merge = ['Fund','Account Type','Function','Subfunction','Object/Source']
            df_temp['ACCOUNTNUMBER'] = df_temp[cols_merge].apply(
                lambda x: ''.join(x.dropna()),
                axis=1
                )
            df_temp.drop(cols_merge,axis=1,inplace=True)
            swap_cols = ['ACCOUNTNUMBER','Description']
            df_temp=df_temp.reindex(columns = swap_cols)
            cols_name = ['Account Number','Description']
            df_temp.columns = cols_name
            df_desc_rdy = df_temp
            
        else:
            desc_file = ""
            df_desc = pd.read_csv(desc_file,encoding = "ISO-8859-1")
            df_desc_rdy = df_desc
        

        #format description files to generate consistent dataframe.  format changes over the years
        budget_file = FILES_STORE + '\\full\\'+ str(i) + '-' + str(i+1) + '-Budget-Data-AtoZ-with-Rollups.csv'
        df_budget = pd.read_csv(budget_file,encoding = "ISO-8859-1",dtype=str)

        if i == 2012:
            cols_name = ['Fiscal Year','Report Type','District Number','District Name','Account Number','Account Type',str(i)]
        elif i == 2013:
            cols_name = ['Fiscal Year','District Number','District Name','Account Number','Account Type',str(i)]
        else: 
            cols_name = ['Fiscal Year','Report Type','District Number','District Name','Account Number',str(i)] 
        
        df_budget.columns = cols_name
        if 'Report Type' in df_budget:
            df_budget.drop(columns='Report Type',inplace = True)

        yrdata = pd.merge(df_budget,df_desc_rdy,on="Account Number",how = "left")
        yrdata = yrdata.reindex(columns = ['Fiscal Year','Report Type','District Number','District Name','Account Number', 'Description', 'Account Type', str(i)])
        yrdata.drop(labels=['Fiscal Year','Report Type'] ,axis = 1,inplace=True)
        yrdata['Account Number'] = yrdata['Account Number'].apply(lambda x: x.replace(' ', ''))
        yrdata.rename(columns={'Description': 'Description '+ str(i)},inplace=True)
        yrdata.rename(columns={'District Number': 'District Number '+ str(i)},inplace=True)
        if i == start_year:
            out = yrdata
        else:     
            if 'Account Type' in yrdata:
                yrdata.drop(columns=['Account Type'],inplace = True)
            outtemp = out
            out = pd.merge(outtemp,yrdata,on=["District Name","Account Number"],how = "outer")
            print(out.size)
        out.to_csv('Output.csv')


 #this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
    
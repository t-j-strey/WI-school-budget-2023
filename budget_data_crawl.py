
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
    end_year = 2013
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

        desc_file = FILES_STORE + '\\full\\'+ str(i) + '-' + str(i+1) + '-Budget-Account-Descriptions.csv'
        print("\n\n Description File: ",desc_file)
        df_desc = pd.read_csv(desc_file)
        budget_file = FILES_STORE + '\\full\\'+ str(i) + '-' + str(i+1) + '-Budget-Data-AtoZ-with-Rollups.csv'
        df_budget = pd.read_csv(budget_file)
        df_budget.rename(columns = {'COA_ACCT':'ACCOUNTNUMBER'},inplace= True)
        df_budget.rename(columns = {'AMOUNT': str(i)},inplace=True)
        yrdata = pd.merge(df_budget,df_desc,on="ACCOUNTNUMBER",how = "left")
        yrdata = yrdata.reindex(columns = ['FISCAL_YEAR', 'REPORT_TYPE', 'DISTRICT_ NMBR', 'DISTRICT_NAME','ACCOUNTNUMBER', 'DESCRIPTION', 'ACCTTYPE', str(i)])
        yrdata.drop(labels=['FISCAL_YEAR','REPORT_TYPE'] ,axis = 1,inplace=True)
        if i == start_year:
            out = yrdata
        else:    
            out = pd.merge(out,yrdata,on="ACCOUNTNUMBER",how = "left")

        out.to_csv('Output.csv')


 #this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
    
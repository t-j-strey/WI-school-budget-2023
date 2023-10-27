
from twisted.internet import reactor, defer
from budget_data.budget_data.spiders.budget_data_spdr import BudgetDataSpdrSpider
from budget_data.budget_data import pipelines as budget_data_pipeline
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import os
import pandas as pd
#from excel_utils import export_dist_profiles
from scrapy.utils.log import configure_logging


PROJECT_ROOT =  os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)

def main():

    configure_logging(
        {"LOG_LEVEL":"INFO"}
    )

    settings_file_path = 'budget_data.budget_data.settings'   #Relative Location of Settings File
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE',settings_file_path)
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks #type: ignore
    def crawl():
        #First spider Test
        yield runner.crawl(BudgetDataSpdrSpider)
        
       
        #generate dataframe from returned spider information information
        #comp_df = pd.DataFrame()
        #for item in dist_profiles_pipeline.items:
        #    df = pd.DataFrame.from_dict(item)
        #    if dist_profiles_pipeline.items.index(item) != 0 : #type:ignore if not the first iteration, drop the column headers 
        #        df = df.drop(index = ['Attribute'])
        #    comp_df = pd.concat([comp_df,df])
        #dist_profiles_pipeline.items.clear()

        #build the excel spreadsheet
        #title = 'District Profiles.xlsx' 
        #export_dist_profiles(title,comp_df)# take dataframe and turn it into a formatted Excel Workbook

        reactor.stop() # type: ignore
        
    crawl()
     
    reactor.run() # type: ignore

 #this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
    

from twisted.internet import reactor, defer
from dist_profiles.dist_profiles.spiders.dist_profiles_spdr import DistProfilesSpdrSpider
from dist_profiles.dist_profiles import pipelines as dist_profiles_pipeline
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import os
import pandas as pd
from excel_utils import create_title, export_workbook
from scrapy.utils.log import configure_logging


PROJECT_ROOT =  os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)

def main():

    configure_logging(
        {"LOG_LEVEL":"INFO"}
    )

    settings_file_path = 'dist_profiles.dist_profiles.settings'   #Relative Location of Settings File
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE',settings_file_path)
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks #type: ignore
    def crawl():
        #for report in std_reports:  #loop through the list of available standard reports
            
         #   for i in range(start_year,end_year + 1):  #loop through range of years            
        yield runner.crawl(DistProfilesSpdrSpider,year = '2021',district = '0007',init =True)
                #add more spiders here
        
        comp_df = pd.DataFrame()
        for item in dist_profiles_pipeline.items:
                result = item
                #print("\n District List: ",result['district'])
                years = result['years']
                #years = ['2016','2017','2018']
                #districts = result['district']
                districts = ['0007']
                dist_profiles_pipeline.items.clear()
                

        for idistrict in districts: #type:ignore 
            for iyear in years: #type: ignore
                yield runner.crawl(DistProfilesSpdrSpider,year = iyear,district = idistrict,init =False)#type:ignore
        comp_df = pd.DataFrame()
        for item in dist_profiles_pipeline.items:
            df = pd.DataFrame.from_dict(item)
            if dist_profiles_pipeline.items.index(item) != 0 : #type:ignore if not the first iteration, drop the column headers 
                df = df.drop(index = ['Attribute'])
            comp_df = pd.concat([comp_df,df])
        dist_profiles_pipeline.items.clear()

        title = 'District Profiles.xlsx' 
        export_workbook(title,comp_df)# take dataframe and turn it into a formatted Excel Workbook

        reactor.stop() # type: ignore
        
    crawl()
     
    reactor.run() # type: ignore

 #this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
    
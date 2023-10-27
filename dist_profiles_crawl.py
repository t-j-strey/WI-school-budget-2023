
from twisted.internet import reactor, defer
from dist_profiles.dist_profiles.spiders.dist_profiles_spdr import DistProfilesSpdrSpider
from dist_profiles.dist_profiles import pipelines as dist_profiles_pipeline
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import os
import pandas as pd
from excel_utils import export_dist_profiles
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
        #First spider pulls all the district number and year data from the page's dropdown
        yield runner.crawl(DistProfilesSpdrSpider,year = '2021',district = '0007',init =True)
        
        #return and format lists of the years and districts
        comp_df = pd.DataFrame()
        for item in dist_profiles_pipeline.items:
                result = item
                years = result['years']
                #years = ['2016','2017','2018']
                districts = result['district']
                #districts = ['0007','0014']
                dist_profiles_pipeline.items.clear()
                
        #loop through the returned district and year lists to generate dataframe.  Note, this takes a while! (>1 hour)
        for idistrict in districts: #type:ignore
            for iyear in years: #type: ignore
                yield runner.crawl(DistProfilesSpdrSpider,year = iyear,district = idistrict,init =False)#type:ignore
        
        #generate dataframe from returned spider information information
        comp_df = pd.DataFrame()
        for item in dist_profiles_pipeline.items:
            df = pd.DataFrame.from_dict(item)
            if dist_profiles_pipeline.items.index(item) != 0 : #type:ignore if not the first iteration, drop the column headers 
                df = df.drop(index = ['Attribute'])
            comp_df = pd.concat([comp_df,df])
        dist_profiles_pipeline.items.clear()

        #build the excel spreadsheet
        title = 'District Profiles.xlsx' 
        export_dist_profiles(title,comp_df)# take dataframe and turn it into a formatted Excel Workbook

        reactor.stop() # type: ignore
        
    crawl()
     
    reactor.run() # type: ignore

 #this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
    
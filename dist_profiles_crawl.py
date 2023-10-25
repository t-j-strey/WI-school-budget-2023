
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
        yield runner.crawl(DistProfilesSpdrSpider,year = '2021')
                #add more spiders here
        
          #  comp_df = pd.DataFrame()
          #  for item in std_report_pipeline.items:
           #     df = pd.DataFrame.from_dict(item)
           #     df = df.drop(index = (len(df)-1)) #remove last row from table
            #    if std_report_pipeline.items.index(item) != 0 : #if not the first iteration, drop the column headers
            #       df = df.drop(index = [0,1])
             #   comp_df = pd.concat([comp_df,df])
            #std_report_pipeline.items.clear()
        
         #   title = create_title(report) #create a Spreadsheet title from site address
         #   export_workbook(title,comp_df)# take dataframe and turn it into a formatted Excel Workbook

        reactor.stop() # type: ignore
        
    crawl()
     
    reactor.run() # type: ignore

 #this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
    
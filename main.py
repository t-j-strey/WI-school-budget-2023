
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from WICompCost.WICompCost.spiders.compcost import CompcostSpider
from WICompCost.WICompCost import pipelines
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import os
import pandas as pd
from excel_utils import create_title, export_workbook

#PROJECT_ROOT = "D:\\Github\\WI-school-budget-2023"
PROJECT_ROOT =  os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)


std_reports = ["https://sfs.dpi.wi.gov/sfsdw/CompCostReport.aspx"]
              # "https://sfs.dpi.wi.gov/sfsdw/CompRevReport.aspx"]
start_year = 2018
end_year = 2018 #inclusive

def main():
    
    configure_logging(
        {"LOG_LEVEL":"INFO"}
    )

    settings_file_path = 'WICompCost.WICompCost.settings'   #Relative Location of Settings File
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE',settings_file_path)
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        for report in std_reports:  #loop through the list of available standard reports
            for i in range(start_year,end_year + 1):  #loop through range of years            
                yield runner.crawl(CompcostSpider,year = str(i),stdreport= report)
                #add more spiders here
            comp_df = pd.DataFrame()
            for item in pipelines.items:
                df = pd.DataFrame.from_dict(item)
                last_row = len(df)-1
                df = df.drop(index = (len(df)-1))
                if pipelines.items.index(item) != 0 : #if not the first iteration, drop the column headers
                    df = df.drop(index = [0,1])
                comp_df = pd.concat([comp_df,df])

            title = create_title(report) #create a Spreadsheet title from site address
            export_workbook(title,comp_df)# take dataframe and turn it into a formatted Excel Workbook

        reactor.stop() # type: ignore
        
    crawl()
    reactor.run() # type: ignore

   
    


# this only runs if the module was *not* imported
if __name__ == "__main__":
    main()


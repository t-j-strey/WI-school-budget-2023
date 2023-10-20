
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from std_reports.std_reports.spiders.std_reports_spider import StdReportsSpider
from std_reports.std_reports import pipelines
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import os
import pandas as pd
from excel_utils import create_title, export_workbook

PROJECT_ROOT =  os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)


std_reports = ["https://sfs.dpi.wi.gov/sfsdw/CompCostReport.aspx",
               #"https://sfs.dpi.wi.gov/sfsdw/CompRevReport.aspx",
               #"https://sfs.dpi.wi.gov/sfsdw/EqualizationAidReport.aspx",
               #"https://sfs.dpi.wi.gov/sfsdw/EqualizedValueReport.aspx",
               #"https://sfs.dpi.wi.gov/sfsdw/MembershipFTEReport.aspx",
               #"https://sfs.dpi.wi.gov/sfsdw/MillRateReport.aspx",
               "https://sfs.dpi.wi.gov/sfsdw/RevenueLimitReport.aspx"]
start_year = 2004
end_year = 2005 #inclusive

def main():
    
    configure_logging(
        {"LOG_LEVEL":"INFO"}
    )
    #small change

    settings_file_path = 'std_reports.std_reports.settings'   #Relative Location of Settings File
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE',settings_file_path)
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        for report in std_reports:  #loop through the list of available standard reports
            
            for i in range(start_year,end_year + 1):  #loop through range of years            
                yield runner.crawl(StdReportsSpider,year = str(i),stdreport= report)
                #add more spiders here

            comp_df = pd.DataFrame()
            for item in pipelines.items:
                df = pd.DataFrame.from_dict(item)
                df = df.drop(index = (len(df)-1)) #remove last row from table
                if pipelines.items.index(item) != 0 : #if not the first iteration, drop the column headers
                    df = df.drop(index = [0,1])
                comp_df = pd.concat([comp_df,df])
            pipelines.items.clear()



            


            title = create_title(report) #create a Spreadsheet title from site address
            export_workbook(title,comp_df)# take dataframe and turn it into a formatted Excel Workbook

        reactor.stop() # type: ignore
        
    crawl()
    reactor.run() # type: ignore

   
    


# this only runs if the module was *not* imported
if __name__ == "__main__":
    main()


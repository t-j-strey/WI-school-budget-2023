
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from WICompCost.WICompCost.spiders.compcost import CompcostSpider
from WICompCost.WICompCost import pipelines
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import os
import pandas as pd


PROJECT_ROOT = "D:\\Github\\WI-school-budget-2023"
os.chdir(PROJECT_ROOT)

std_reports = ["https://sfs.dpi.wi.gov/sfsdw/CompCostReport.aspx"]
               #"https://sfs.dpi.wi.gov/sfsdw/CompRevReport.aspx"]
start_year = 2018
end_year = 2020 #inclusive

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
                comp_df = pd.concat([comp_df,df])
            print(comp_df)

            #with pd.ExcelWriter(
            #    "ReportName.xlsx",
            #    engine = 'openpyxl',
            #    mode = 'w'
            #) as writer:
            #    comp_df.to_excel(writer,
            #                     sheet_name='sheet1',
            #                     index = False,
            #                     header = True,
            #                     merge_cells = True)
            
        reactor.stop() # type: ignore
        
    crawl()
    reactor.run() # type: ignore

   
    


# this only runs if the module was *not* imported
if __name__ == "__main__":
    main()

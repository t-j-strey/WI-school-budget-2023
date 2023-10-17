
from scrapy.utils.log import configure_logging
from twisted.internet import task, reactor, defer
from WICompCost.WICompCost.spiders.compcost import CompcostSpider
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

std_reports = ["https://sfs.dpi.wi.gov/sfsdw/CompCostReport.aspx",
               "https://sfs.dpi.wi.gov/sfsdw/CompRevReport.aspx"]
start_year = 2018
end_year = 2019 #inclusive


def main():
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    

    @defer.inlineCallbacks
    def crawl():
        for report in std_reports:  #loop through the list of available standard reports
            for i in range(start_year,end_year + 1):  #loop through range of years            
                yield runner.crawl(CompcostSpider,year = str(i),stdreport= report)
                #add more spiders here
        reactor.stop() # type: ignore

    crawl()
    reactor.run() # type: ignore


# this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
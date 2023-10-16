#import scrapy

from scrapy.utils.log import configure_logging

from twisted.internet import task, reactor, defer
#from scrapy.crawler import CrawlerProcess
from WICompCost.WICompCost.spiders.compcost import CompcostSpider
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings


def main():
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(CompcostSpider)
        #d.addBoth(lambda _: reactor.stop())
        #add more spiders here
        reactor.stop()

    crawl()
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
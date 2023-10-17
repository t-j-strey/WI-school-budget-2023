
from scrapy.utils.log import configure_logging
from twisted.internet import task, reactor, defer
from WICompCost.WICompCost.spiders.compcost import CompcostSpider
from WICompCost.WICompCost.spiders.comprev import ComprevSpider
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings


def main():
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(CompcostSpider)
        yield runner.crawl(ComprevSpider)
        #add more spiders here
        reactor.stop() # type: ignore

    crawl()
    reactor.run() # type: ignore


# this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
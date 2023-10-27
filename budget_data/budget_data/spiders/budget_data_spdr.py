import scrapy
from scrapy.shell import inspect_response



class BudgetDataSpdrSpider(scrapy.Spider):
    name = "budget_data_spdr"
    allowed_domains = ["dpi.wi.gov"]
    start_urls = ["https://dpi.wi.gov/sfs/reporting/safr/budget/data-download"]

    def parse(self, response):
        for result in response.xpath('//div[@class="s-item-container"]'):
            print("\nLooping through results:")
            print(result.xpath('.//a[contains(@href,".xlsx")]).extract_first()'))
        #inspect_response(response,self)


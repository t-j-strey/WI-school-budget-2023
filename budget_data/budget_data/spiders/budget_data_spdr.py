import scrapy
from scrapy.shell import inspect_response
from budget_data.budget_data.items import BudgetDataItem
from budget_data.budget_data.pipelines import BudgetDataPipeline


class BudgetDataSpdrSpider(scrapy.Spider):
    name = "budget_data_spdr"
    allowed_domains = ["dpi.wi.gov"]
    start_urls = ["https://dpi.wi.gov/sfs/reporting/safr/budget/data-download"]



    def parse(self, response):
        for result1 in response.xpath('//div[@class="template-inner"]'):
            for result2 in result1.xpath('.//a/@href[(contains(., "Descriptions")) or (contains(., "COA")) or (contains(., "AtoZ"))]'): #returns Account Descriptions
                file_url =  "https://dpi.wi.gov/" + result2.extract()
                item = BudgetDataItem()
                item['file_urls'] = [file_url]
                yield item

        #inspect_response(response,self)

import scrapy
from scrapy.shell import inspect_response
from budget_data.budget_data.items import BudgetDataItem



class BudgetDataSpdrSpider(scrapy.Spider):
    name = "budget_data_spdr"
    allowed_domains = ["dpi.wi.gov"]
    start_urls = ["https://dpi.wi.gov/sfs/reporting/safr/budget/data-download"]

    def parse(self, response):
        for result1 in response.xpath('//div[@class="template-inner"]'):
            for result2 in result1.xpath('.//a/@href[(contains(., "Descriptions"))]'): #returns Account Descriptions
                file_url =  "https://dpi.wi.gov/" + result2.extract()
                print("\nDescriptions URLs: ", file_url)
                item = BudgetDataItem()
                item['file_urls'] = [file_url]
                yield item

            for result3 in result1.xpath('.//a/@href[(contains(., "AtoZ"))]'): #returns only AtoZ URLs
                print("\nBudget Data: ",result3.extract())
                file_url =  "https://dpi.wi.gov/" + result3.extract()
                item = BudgetDataItem()
                item['file_urls'] = [file_url]
                yield item
            
    
        #inspect_response(response,self)

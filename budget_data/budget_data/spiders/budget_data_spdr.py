import scrapy
from scrapy.shell import inspect_response



class BudgetDataSpdrSpider(scrapy.Spider):
    name = "budget_data_spdr"
    allowed_domains = ["dpi.wi.gov"]
    start_urls = ["https://dpi.wi.gov/sfs/reporting/safr/budget/data-download"]

    def parse(self, response):
        for result1 in response.xpath('//div[@class="template-inner"]'):
            print("\n\n\nLooping through results: ")
           
            for result2 in result1.xpath('.//a/@href[(contains(., "Descriptions"))]'):
                print("\nDescriptions: ", result2.extract())
            for result3 in result1.xpath('.//a/@href[(contains(., "AtoZ"))]'): #returns only AtoZ URLs
                print("\nBudget Data: ",result3.extract())
            
        
            
        #inspect_response(response,self)

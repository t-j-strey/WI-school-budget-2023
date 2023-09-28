import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class ComparativecostSpider(scrapy.Spider):
    name = "comparativeCost"
    allowed_domains = ["sfs.dpi.wi.gov"]
    start_urls = ["https://sfs.dpi.wi.gov/sfsdw/CompCostReport.aspx"]

    def parse(self, response):
         
        yield FormRequest.from_response(response,
                                        formnumber=1,
                                        value = "Show All Agencies")

    def parse1(self,response):
        open_in_browser(response)    
    


print("Hello World")
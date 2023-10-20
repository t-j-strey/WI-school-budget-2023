import scrapy


class DistProfilesSpdrSpider(scrapy.Spider):
    name = "dist_profiles_spdr"
    allowed_domains = ["sfs.dpi.wi.gov"]
    start_urls = ["https://sfs.dpi.wi.gov/sfsdw/Agency_Financial_profile.aspx"]

    def parse(self, response):
        pass

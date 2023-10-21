import scrapy
from scrapy import FormRequest,Request
import pandas as pd
import numpy as np
import io
import logging


class DistProfilesSpdrSpider(scrapy.Spider):
    name = "dist_profiles_spdr"
    allowed_domains = ["sfs.dpi.wi.gov"]
    start_urls = ["https://sfs.dpi.wi.gov/sfsdw/Agency_Financial_profile.aspx"]

    def __init__(self,year=None, stdreport="", *args, **kwargs):
        super(DistProfilesSpdrSpider,self).__init__(*args,**kwargs)
        logging.getLogger('scrapy').setLevel(logging.WARNING)

    def parse(self, response):
        pass

# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import os
import json
import datetime

# property scraper class
class ResidentialSale(scrapy.Spider):
    # scraper name
    name = 'therapists'
    base_url = 'https://www.tutorified.com/live-tutoring-classes/'
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    try:
       os.remove('abx.csv')
    except OSError:
       pass   
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
    }

    # general crawler
    def start_requests(self):
       
            # initial HTTP request
            yield scrapy.Request(
                url=self.base_url,
                headers=self.headers,
               
                callback=self.parse
               )
    def parse(self, res):
       content = ''
       with open('res.html', 'r') as html_file:
          for line in html_file.read():
              content += line 
       res = Selector(text = content)
       print(res)
       
       
       
       
       
       
       
       
#       yield response.follow(
#             url = ,
#             headers = self.headers,
#             callback = 
#       )

if __name__ == '__main__':
    # run scraper
#    process = CrawlerProcess()
#    process.crawl(ResidentialSale)
#    process.start()
    
    ResidentialSale.parse(ResidentialSale, '')
    

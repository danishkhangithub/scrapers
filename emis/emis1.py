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
    base_url = 'https://www.emis.com/php/company-profile/index/search?cmpy_tr_usd_min=0&cmpy_tr_usd_max=300000000000'
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    
    current_page = 0
    try:
       os.remove('companies.csv')
    except OSError:
       pass   
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
    }

    # general crawler
    def start_requests(self):
         for page in range(1,50):
            base_url = 'https://www.emis.com/php/company-profile/index/search?page='+ str(page) +'&rpp=50&cmpy_tr_usd_min=0&cmpy_tr_usd_max=300000000000' 
            # initial HTTP request
            yield scrapy.Request(
                url=base_url,
                headers=self.headers,
               
                callback=self.parse
                      )
                 
    def parse(self, response):
        comp_links =   [comp for comp in response.css('div[class = "br-e7"]').css('a::attr(href)').getall()]
        for company in comp_links:
            comp_links =  'https://www.emis.com' + company

        
            yield response.follow(
               url =comp_links ,
               headers = self.headers,
               callback = self.parse_cards
               )
            break
           
    def parse_cards(self, response):
        pass
        print('\nok\n')
        
        self.current_page +=1
        self.log('\n current_page %s' % self.current_page)
        
        '''
        content = ''
        
        with open('emis1.html', 'r') as f:
        for line f.read():
              content +=line
        response = Selector(text=content)      
        
        features = {
          'Name' : response.css('h1::text').get().replace('\n',''),
          'Description' : response.css('p[class = "c-66 ff-grbk"]::text').get(),
          'Website' : response.css('div[class = "d-tc w-50 va-t"]').css('a::attr(href)').get()
         
        }     

        '''
         
    
    
        '''
        with open('companies.csv', 'a') as csv_file:
             writer = csv.DictWriter(csv_file, fieldnames=features.keys())
             writer.writerow(features)
        '''
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ResidentialSale)
    process.start()
    
    #ResidentialSale.parse(ResidentialSale, '')
    

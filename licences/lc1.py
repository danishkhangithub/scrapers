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
    base_url = 'https://registers.consumer.vic.gov.au/EaSearch/PerformSearch?'
    params = {
      'NameOrLicenceNumber' : 'LicenceNumber',
      'LicenceNumber' : 1,
      'SoundsLike' : 'False',
      'IncludeNonCurrentLicensees' : 'False'
    }
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    '''
    try:
       os.remove('abx.csv')
    except OSError:
       pass 
    '''
    file = 'data.csv'
    try:
      if(os.path.exists(file) and os.path.isfile(file)):
         os.remove(file)
         print('file deleted')
      else:      
         print('file not found')
    except OSError:
       pass 
    
         
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
    }

    # general crawler
    def start_requests(self):
            for i in range(1,5):
                url = self.base_url + urllib.parse.urlencode(self.params)
                # initial HTTP request
                yield scrapy.Request(
                    url=url,
                    headers=self.headers,
                   
                    callback=self.parse
                          )
                self.params['LicenceNumber'] +=1
                          
    def parse(self, response):
        try:
          
           if 'View Details' in response.text:
              print('found')
              link = response.css('.search-btn::attr(href)').get()
              link =  'https://registers.consumer.vic.gov.au'  + link
              print(link)
              
              yield response.follow(
                  url = link,
                  headers = self.headers,
                  callback = parse_content
               )

           else:
              print('No Agent found') 
               
        except:
          pass 
       
    def parse_content(self,response):
        # define keys to which all the content will be appended
        keys = {}
        
        keys = response.css('.dl-horizontal')
        # titles
        for key in keys:
            titles = key.css('dt::text').getall()
            titles =[ title.strip() for title in titles]
        
        # values
        for t in titles:
          values = response.css('dd::text').getall()
          values =[ val.strip() for val in values];  print(values)
           
        for v in range(0,len(titles)):
           keys[titles[v]] = values[v]
        print('\nkeys: ',keys)
        '''
        with open('data.csv', 'a') as csv_file:
             writer = csv.DictWriter(csv_file, fieldnames=items.keys())
             writer.writerow(items)
        '''

if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ResidentialSale)
    process.start()
    
    #ResidentialSale.parse(ResidentialSale, '')
    

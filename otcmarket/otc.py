# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import os
import json
import datetime
import csv

# property scraper class
class ResidentialSale(scrapy.Spider):
    # scraper name
    name = 'therapists'
    
    base_url = 'https://www.otcmarkets.com/'
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    try:
       os.remove('armuranks.csv')
    except OSError:
       pass   
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
    }
   
    # on create
    def __init__(self):

        # inti postcodes
        company = ''

        # open "postcodes.json"
        with open('comp.txt', 'r') as html_file:
            for line in html_file.read():
                company += line
        self.company = company
    # general crawler
    def start_requests(self):
            for item in self.company:
            # initial HTTP request
                yield scrapy.Request(
                    url=self.base_url,
                    headers=self.headers,
                    meta = {'company': item},
                    callback=self.parse
                )
            
    def parse(self, response):  
         count = 0
         #company = response.meta.get('company') 
         company = ''
              
         with open('output2.txt') as f:
            links = f.read().split('\n')  
                
         for item in links:       
         
             url = 'https://backend.otcmarkets.com/otcapi/company/profile/full/' + str(item) + '?symbol=' + str(item)
          
            
             yield response.follow(
                 url = url,
                 headers = self.headers,
                 meta = {'count': count},
                 callback = self.parse_listing
               )
             count += 1 
             print('count:', count)
             break
    def parse_listing(self, res):
      company = res.meta.get('company')
      count = res.meta.get('count')
      data = json.loads(res.text)
      
      features = {
         'symbol': res.url.split('?symbol=')[1] ,
         'OTCMarketUrl' : res.url,
         'Phone No' : data['phone'],
         'ContactName1' : '',
         'ContactTitle1' : '',
         'Address' : '',
         'Email' : '',
         'Website': ''
      }       
      
      try:
       ceo =  ''.join([card['name'] for card in data['officers']][0])
      except:
       ceo =   ''.join([card['name'] for card in data['officers']])  
      
      ceoo= ceo
      features['ContactName1'] = ceoo
      
      try:
       title =  ''.join([card['title'] for card in data['officers']][0])
      except:
       title =   ''.join([card['title'] for card in data['officers']])  
      
      ceoo= title
      features['ContactTitle1'] = ceoo
      
      try:
         address = data['address1'] + '\n' + data['address2'] 
      except:
        address = data['address1']  
        
      city = data['city'] + ' ' + data['state'] + ' ' + data['zip']
      
      full_address =  address + ' ' + city

      features['address'] = full_address
      
      try:
         email = data['email']
      except:
         email = 'N/A'  
      features['email'] = email
      
      try:
         website = data['website']
      except:
         website = 'N/A'   
      features['website'] = website
      
      
     
      
      print(features)
      with open('Stock_Screener_OTC_USA_Canada_Under10-3.csv', 'a') as csv_file:
         writer = csv.DictWriter(csv_file, fieldnames = features.keys())
         writer.writerow(features)      
      
# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ResidentialSale)
    process.start()
    
    #ResidentialSale.parse(ResidentialSale, '')
    
    

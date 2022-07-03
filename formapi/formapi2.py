import json
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import FormRequest
import urllib
import os
import json
import csv
import datetime


class MySpider(scrapy.Spider):
    name = 'myspider'

    #different url

    start_urls = ['https://www.obagi.com/medical/hcpfinder']
    url = 'https://www.obagi.com/api/ajax/api/hcpfinder'

    formdata = {
        'city' : 'boston',
        'state' : 'MA',
        'distance' : '25',
                }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
   
    try:
       os.remove('clinics.csv')
    except OSError:
       pass  

    def parse(self,response):
        yield scrapy.FormRequest(
                url=self.url,method='POST',
                headers=self.headers,
                formdata=self.formdata,
                callback=self.parse_page,
            )

    def parse_page(self, response):
        data = json.loads(response.text)
        
        for i in data['clinics']:
           features = {
              'Name' : i['name'],
              'Address1' : i['address1'],
              'City' : i['city'],
              'State' : i['state'],
              'Zip' : i['zip'],
              'Phone' : i['phone'],
              'Website' :  i['website'],
              'Speciality' : i['specialty'],
              'Email' : i['email']
           }
           print(features)
           
           with open('clinics.csv', 'a') as csv_file:
              writer = csv.DictWriter(csv_file, fieldnames = features.keys())
              writer.writerow(features)
        
        
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
    
    #ResidentialSale.parse(ResidentialSale, '')
            

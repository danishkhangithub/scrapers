# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
import urllib
import os
import json
import datetime
import csv
import time

# property scraper class
class ResidentialSale(scrapy.Spider):
    # scraper name
    name = 'therapists'
    base_url = 'https://www.yellowpages.com.au/'
    tag = ''
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
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
        'DOWNLOAD_DELAY': 2
    }


    def __init__(self):
         
        chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'

        chrome_options = Options()
        #chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(
          executable_path=chrome_driver_path, options=chrome_options
        )
        
    # general crawler
    def start_requests(self):
        url = self.base_url #+ self.tag
        # initial HTTP request
        yield scrapy.Request(
            url=url,
            headers=self.headers,
           
            callback=self.parse
                  )
    def parse(self, response):
        '''
        content = ''
        with open('instra2.html', 'r') as f:
           for line in f.read():
             content +=line
        
        res = Selector(text = content)
        '''
      
        url =  'https://www.yellowpages.com.au/'
        base_url = url 
        self.driver.get(base_url)

        time.sleep(2)
        
        print(self.driver.get_cookies())
        self.driver.delete_all_cookies()
        #self.driver.refresh()
        
        time.sleep(2)
        
        
        electrician = Selector(text = self.driver.page_source)
        electricians = electrician.css('a[class = "homepage-quicklinks"]::attr(href)').get()
        yield response.follow(
             url = 'https://www.yellowpages.com.au/' + electricians,
             headers = self.headers,
             callback = self.parse_lists
        )
        time.sleep(2) 
        #self.driver.close()
        
    def parse_lists(self, response):
        self.driver.delete_all_cookies()
        
        links = response.css('a[class= "MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary"]::attr(href)').getall()
        print('\nlinks:',links)
        for link in links:
           link = 'https://www.yellowpages.com.au' + link
           
           yield response.follow(
           url = link,
           headers = self.headers,
           callback = self.parse_card
           )

    def parse_card(self,response):
        self.driver.delete_all_cookies()
        name = response.css('.listing-name::text').get()
        print('\nname:',name)
        self.driver.close()
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ResidentialSale)
    process.start()
    
    #ResidentialSale.parse(ResidentialSale, '')
    

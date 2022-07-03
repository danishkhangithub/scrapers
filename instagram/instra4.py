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
    base_url = 'https://www.instagram.com/onaka.vegan/'
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
        
        content = ''
        with open('instra2.html', 'r') as f:
           for line in f.read():
             content +=line
        
        response = Selector(text = content)
        data = [script for script in response.css('script::text').getall() if 'window._sharedData = ' in script]
        data = [d.split('window._sharedData = ')[-1].replace(' ', '').rstrip(';') for d in data]
        data = data
        for i in data:
          data = json.loads(i)
          #data = json.dumps(data, indent = 2)
          data = data['entry_data']['ProfilePage']#[0]
          #data = json.dumps(data, indent = 2)
          #print('\n\n',json.dumps(data, indent = 2) ,'\n\n')
          for user in data:
              user_data = user['graphql']['user']
              print(json.dumps(user_data,indent =2))
        
          #print(data)
        '''
        login_url = 'https://www.instagram.com/'
        username = 'danishkhan11'
        password = 'danishinstra3.1'
        
        # retrive url in headless browser
        self.driver.get(login_url)
    
        # find search box
        username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
       
        
        username.clear()
        username.send_keys("danishkhankd11")
        password.clear()
        password.send_keys("danishinstra3.1")
        
        # target button
        button = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        
        time.sleep(5)
        alert = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()  
      
        alert2 = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
      
        #driver.get(base_url)
        time.sleep(5)
        
        
         
        url =  'https://www.instagram.com/veganfoodplug/'
        base_url = url 
        self.driver.get(base_url)
 
        profiles = self.driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "Y8-fY", " " )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "-nal3", " " ))]')
      
        profiles.click()
        time.sleep(10)
        
        
        profiles_url = self.driver.find_elements_by_xpath('//span/a')
        
        profiles_urls = [i.get_attribute('href') for i in profiles_url]
        print(profiles_urls)
        
        
            
        for prof in profiles_urls:     
           yield response.follow(
              url = prof ,
              headers = self.headers,
              callback = self.parse_card
           )
           
           with open('instragram1.csv', 'a') as csv_file:
             writer = csv.DictWriter(csv_file, fieldnames=names)
             writer.writerow(details)
        '''

    def parse_card(self, response):
        
        data = [script for script in response.css('script::text').getall() if 'window._sharedData = ' in script]
        data = [d.split('window._sharedData = ')[-1].replace(' ', '').rstrip(';') for d in data]
        for i in data:
          data = json.loads(i)
          #data = json.dumps(data, indent = 2)
          data = data['entry_data']['ProfilePage']#[0]
          #data = json.dumps(data, indent = 2)
          #print('\n\n',json.dumps(data, indent = 2) ,'\n\n')
          for user in data:
              user_data = user['graphql']['user']
        
              email =  user_data['business_email']
              phone_no = user_data['business_phone_number']
            
              details = {
                 
                 'Email' : email,
                 'Phone ': phone_no,
           
              }        
              print(details)
              
            
        


if __name__ == '__main__':
    # run scraper
#    process = CrawlerProcess()
#    process.crawl(ResidentialSale)
#    process.start()
    
     ResidentialSale.parse(ResidentialSale, '')
    

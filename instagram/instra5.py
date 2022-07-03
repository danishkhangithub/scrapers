import scrapy 
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib
import time
import re
import os
import csv
import json

class Googlescraper(scrapy.Spider):
    name = 'google'
    base_url = 'https://www.google.com/search?'
    
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    
    file = 'contact.csv'
    try:
      if(os.path.exists(file) and os.path.isfile(file)):
         os.remove(file)
         print('file deleted')
      else:      
         print('file not found')
    except OSError:
       pass 
    
    # append results to data
    data = []
         
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 2
    }
   #params will be attached to url
    params = {
      "q" : "vegan gmail.com+site:instagram.com",
      "sxsrf": "ALeKk03piC9RwREGzXOYcAuhZzAgZuWilw:1621918781372",
      "ei": "PYSsYLmDFuCC9u8P06KdmAw",
      "start": 0,
      "sa": "N",
      "ved": "2ahUKEwj5lcWmhuTwAhVggf0HHVNRB8MQ8NMDegQIARBG",
      "biw": "974",
      "bih": "624"
    }

    # write csv file columns names
    def __init__(self):
       with open('contact.csv','w') as f:
           f.write('Email, Phone_no\n')
    
    
    # general crawler
    def start_requests(self):
    
            for i in range(0,3): 
                 
                url = self.base_url + urllib.parse.urlencode(self.params)
                # initial HTTP request
                yield scrapy.Request(
                    url= url,
                    headers=self.headers,
                    callback=self.parse,
                    meta = {'page': self.params['start']}
                          )
                self.params['start'] +=10  
                print('\nstrat:', self.params['start'])
    def parse(self, response):
            page = response.meta.get('page')
            page = int(page/10) 
            self.log('\n Page no %s out of 10' % (page))
            '''
            content = ''
            with open('instra4.html','r') as f:
              for line in f.read():
                 content +=line
            response = Selector(text = content)
            '''
            links = response.xpath('//div[@class="yuRUbf"]/a/@href').getall()    
            
            for link in links:
            
                yield response.follow(
                     url = link,
                     headers = self.headers,
                     callback = self.instagram
                )
                break
    def instagram(self, response):
        
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
              '''
              if email != None or email != [] or email != '' : 
                  email = email
                            
              else:
                  email = re.findall('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}',str(response))
              '''
              email = ''
              if '@gmail.com' in data:
                 
                  emails = re.findall('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}',str(data))
                  email = emails
                
              details = {
                     
                     'Email' : email,
                     'Phone ': phone_no,
               
                  }    
              self.data.append(details)  
               
              print(self.data) 
              with open('contact.csv','a') as f:
                writer = csv.DictWriter(f, fieldnames = details.keys())
                writer.writerow(details)  
        
        
#        # increment start
#        self.start +=10
#        self.params['start'] = self.start      
#        next_page =  self.base_url + urllib.parse.urlencode(self.params)
#        print('\nnext_page:',next_page)  
        
if __name__ == '__main__':
   process = CrawlerProcess()
   process.crawl(Googlescraper)
   process.start()        
   
   #Googlescraper.parse(Googlescraper, '')

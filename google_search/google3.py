import scrapy 
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib
import time
import re
import csv
import pandas as pd

class Googlescraper(scrapy.Spider):
    name = 'google'
    start_urls = ['https://www.google.com/search?']
    params = {
      "tbs": "lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2",
      "tbm": "lcl",
      "sxsrf": "ALeKk01BW86aXeyv0NqmJYfOhvFCjtqsGg:1623217868172",
      "q": "beverages in atlanta georgia",
      "rflfq": "1",
      "num": "10",
      "sa": "X",
      "ved": "2ahUKEwjQkbPj7YnxAhVUgFwKHTUIDQsQjGp6BAgMEE0",
      "biw": "1366",
      "bih": "624",
      "rlst": "hd:;si:;mv:[[33.9412923,-84.25019669999999],[33.6955892,-84.6178867]];",
      "start": 0

    
    }
    def __init__(self):
     
        url = 'https://www.google.com/search?'
        chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'

        chrome_options = Options()
        #chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(
          executable_path=chrome_driver_path, options=chrome_options
        )


    def parse(self,response):
    
            url =  'https://www.google.com/search?'
            for page in range(0,10):
                base_url = url + urllib.parse.urlencode(self.params)
                self.driver.get(base_url)
                self.params['start'] +=10 
       
                links = self.driver.find_elements_by_xpath('//a[@class="C8TUKc rllt__link a-no-hover-decoration"]')
                
                for i in links:

                    i.click()

                    time.sleep(5)
                    
                    details = {
                     'Name' : '',
                     'Address' : '',
                     'Phone ' : '',
                     'Website ' : '',
                     'Email' : ''
                      }
                      
                    try: 
                      Name = self.driver.find_element_by_xpath('//div[@class="SPZz6b"]/h2/span').text
                    except:    
                      Name = ''
                      
                    try: 
                      Address = self.driver.find_element_by_xpath('//div[@class="zloOqf PZPZlf"]/span[@class="LrzXr"]').text
                    except:    
                      Address = ''  
                      
                    try: 
                      Phone = self.driver.find_element_by_xpath('//div[@class="zloOqf PZPZlf"]/span//a/span').text
                    except:    
                      Phone = ''  
                    
                    try: 
                      Website = self.driver.find_element_by_xpath('//div[@class="QqG1Sd"]/a').get_attribute('href')
                    except:    
                      Website = ''  
                      pass
                      
                    details['Name'] = Name
                    details['Address'] = Address 
                    details['Phone'] = Phone 
                    details['Website'] = Website 
                      
                      
                    print('\ndetails:',details)
                    try:
                       website_url = self.driver.find_element_by_xpath('//div[@class="QqG1Sd"]/a')
                       website_url = website_url.get_attribute('href')
                       print(website_url)
                    except NoSuchElementException:
                       print('err')
                       pass   
                    try:
                      #print('\ndetails:',details)
                      yield scrapy.Request(website_url,meta = {'details' : details},callback=self.parse2)
                    except Exception as e:
                        print('error:', e)
                        website_url = 'N/A'
                        pass
                

                self.driver.close()

    def parse2(self,response):
        details = response.meta.get('details')
        res = response.text
        try:
          email = re.findall('(\w+\@\w+\.\w+)',res)
          email = email[0]
          email = ''.join(email)
        except:
          email = 'N/A'
        
        details['Email'] = email
        
        print('\n\n\ndetails\n\n', details)
        
        with open('dentists.csv','a') as f:
          writer = csv.DictWriter(f, fieldnames = details.keys())
          writer.writeheader()
          writer.writerow(details)
         
        with open('dentists.xlsx','w') as f:
          writer = csv.DictWriter(f, fieldnames = details.keys())
          writer.writeheader()
          writer.writerows(details)   
    
        
if __name__ == '__main__':
   process = CrawlerProcess()
   process.crawl(Googlescraper)
   process.start()        

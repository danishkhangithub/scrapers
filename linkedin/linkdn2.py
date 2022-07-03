from selenium import webdriver
import time
from bs4 import BeautifulSoup
import urllib
from scrapy.selector import Selector
import os
import csv


class Linkedin():

    google_url = 'https://www.google.com/search?'
    
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
         
    
   #params will be attached to url
    params = {
      "q": "site:linkedin.com dentist germany gmail",
      "sxsrf": "ALeKk00gx1jKzwDRrTG4Smn4-dcOr7Z6ig:1622175126605",
      "ei": "lm2wYN2uJKmC9u8PzLivwAY",
      "start": 0,
      "sa": "N",
      "ved": "2ahUKEwjd0byhwevwAhUpgf0HHUzcC2gQ8tMDegQIARA0",
      "biw": "1366",
      "bih": "624"
    }



    # write csv file columns names
    def __init__(self):
      
       with open('contact.csv','w') as f:
           f.write('Email, Phone_no\n')


    def getData(self):
        driver = webdriver.Chrome('/home/danish-khan/scrapers/researchgate/chromedriver')
        google_url = self.google_url + urllib.parse.urlencode(self.params)
        
        for page in range(0,3):
            driver.get(google_url)
            time.sleep(2)
            self.params['start'] += 10
            print(self.params)
        '''
        driver = webdriver.Chrome('/home/danish-khan/scrapers/researchgate/chromedriver')
        driver.get('https://www.linkedin.com/login')
        driver.find_element_by_id('username').send_keys('danishkhankd237@gmail.com') #Enter username of linkedin account here
        driver.find_element_by_id('password').send_keys('dankhanish446')  #Enter Password of linkedin account here
        driver.find_element_by_xpath("//button[@type='submit']").click()
        '''
        content = Selector(text = driver.page_source) 
        urls = []
        links = content.xpath('//div[@class="yuRUbf"]/a/@href').getall()  
        for link in links:

           print(link)  
               
       
        time.sleep(3)        
        driver.close()
 
    def start(self):
        self.getData()
 
if __name__ == "__main__":
    obJH = Linkedin()
    obJH.start()
    
  

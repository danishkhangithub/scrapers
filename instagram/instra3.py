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
from explicit import waiter, XPATH
import itertools
import urllib
import os
import json
from random import randint
import datetime
import csv
import time

# property scraper class
class Instagram(scrapy.Spider):
    # scraper name
    name = 'Instagram'

    base_url = 'https://www.instagram.com/unscriptedposingapp/?utm_medium=copy_link&fbclid=IwAR2Ri-YEC4fbIBlgzDXx2-r9xdBMz_TbKs995MP0QsxyM5ugF_JY2J2_RoM'

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

        response = Selector(text = content)
        '''



        login_url = 'https://www.instagram.com/'
        username = '============='
        password = '-------------'

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



        url =  'https://www.instagram.com/unscriptedposingapp/?utm_medium=copy_link&fbclid=IwAR2Ri-YEC4fbIBlgzDXx2-r9xdBMz_TbKs995MP0QsxyM5ugF_JY2J2_RoM'
        base_url = url
        self.driver.get(base_url)

        follower_list = []


        allfoll = (self.driver.find_element_by_xpath("//li[2]/a/span").text)
        print('\n\nallfoils\n',allfoll)
        allfoll = allfoll.replace('k','000')
        allfoll = int(allfoll)

        self.driver.find_element_by_xpath('//ul/li[2]/a').click()
        time.sleep(2)



        pop_up_window = WebDriverWait(
        self.driver, 2).until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='isgrP']")))
        check = self.driver.execute_script("return arguments[0].scrollHeight > arguments[0].offsetHeight;", pop_up_window)
        print('\ncheck\n\n', check)
#        if check:
#            while True:
        #self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight/100);", pop_up_window)
        self.driver.execute_script("return arguments[0].scrollTo(0, 500);", pop_up_window)
        # time.sleep(1)
        time.sleep(randint(1, 3))
        #scroll_height = self.driver.execute_script("return arguments[0].scrollHeight;", pop_up_window)





        # Scroll till Followers list is there
#        while True:
#            self.driver.execute_script(
#                'arguments[0].scrollTop = arguments[0].scrollTop + (arguments[0].offsetHeight/1000);',
#              pop_up_window)
#            time.sleep(1)
#

        time.sleep(randint(10, 20))

        follower = self.driver.find_elements_by_css_selector('._0imsa')
        for name in follower:
             names = name.get_attribute('href')
             print('\nfollower\n', len(names))
             follower_list.append(names)
        print(follower_list)
        '''
        yield response.follow(
               url = prof ,
               headers = self.headers,
               callback = self.parse_card
               )
        '''
        time.sleep(10)
        self.driver.quit()
        '''
        def parse_card(self, response):
            try:



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
                  #user_data = json.dumps(user_data,indent =2)

                  details = {
                     'Id' : user_data['id'],
                     'User name' : user_data['username'],
                     'Full Name' : user_data['full_name'],
                     'Followers count' : user_data['edge_followed_by']['count'],
                     'Followings' : user_data['edge_follow']['count'],
                     'Biography' : ','.join(user_data['biography'].split('\n')),
                     'Email' : user_data['business_email']
                  }

                  print(details)

                  with open('instragram1.csv', 'a') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=details.keys())
                    writer.writerow(details)
        except:
          pass




    '''



if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Instagram)
    process.start()

    #Instagram.parse(Instagram, '')

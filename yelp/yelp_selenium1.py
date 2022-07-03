# import packages
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import time
import sys
from urllib.parse import urlparse
from urllib.parse import unquote
import urllib
import json

class Yelp():

    def __init__(self):
        self.url = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Los%20Angeles%2C%20CA'
        chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
        chrome_options = Options()
        #chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(
        executable_path=chrome_driver_path, options=chrome_options,
        desired_capabilities=capabilities
        )
        self.page_counts = 0

    def parse(self):

       res = requests.get(self.url)

       soup = BeautifulSoup(res.content, 'lxml')

       #total_pages = soup.select_one('div[class =" border-color--default__09f24__3Epto text-align--center__09f24__2qZj2"]+ span[class = " css-e81eai"]')
       total_pages = soup.find("div", { "class" : "border-color--default__09f24__3Epto text-align--center__09f24__2qZj2" }).find("span", recursive=False).text

       total_pages = total_pages.split()[2]

       print(total_pages)
       try:
           if int(self.page_counts/10) <= int(total_pages):


            for i in range(0,len(total_pages)):
               url = self.url + '&start=' + str(self.page_counts)
               self.driver.get(url)
               print(self.url + '&start=' + str(self.page_counts))
               self.page_counts += 10
           else:
              print('error')
       except Exception as e:
           print(e)
           '''
           logs = self.driver.get_log('performance')
           for log in logs:
             if log['message']:
                d = json.loads(log['message'])
                try:
                    content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
                    response_received = d['message']['method'] == 'Network.responseReceived'
                    if content_type and response_received:
                        print(d['message']['params']['response']['status'])
                except:
                    pass
           '''

#           soup = BeautifulSoup(self.driver.page_source,'lxml')
#           WebDriverWait(self.driver,10)
#
#           card_links = []
#
#           # extracts links
#           links = soup.select('a[class = "css-166la90"]')[2:12]
#           for link in links:
#                link = 'https://www.yelp.com'  + link.get('href')
#                card_links.append(link)
#           print('\ncard_links\n',card_links,'\n', len(card_links))
#           #return card_links
           self.driver.close()

    def parse_links(self, links):
        count = 1
        links = links
        for link in links[:5]:
            self.driver.get(link)

#            logs = self.driver.get_log('performance')
#            for log in logs:
#              if log['message']:
#                 d = json.loads(log['message'])
#                 try:
#                     content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
#                     response_received = d['message']['method'] == 'Network.responseReceived'
#                     if content_type and response_received:
#                         print(d['message']['params']['response']['status'])
#                 except:
#                     pass
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            response  = Selector(text = self.driver.page_source)
            print('\nscrapy selectior\t', response)
            print('\n\n\n Ok\t& count :', count )
            count +=1
            time.sleep(2)
            features = {
                'Name' : soup.find('h1',{'class' : 'css-11q1g5y'}).text,
                'Address' :  soup.find('p',{'class' : 'css-chtywg'}).text,
                'Link' : link,
                'Website' :  '',
                'Phone_No' :'',
                'Rating' : '',
                'Reviews' : '',
                'Opening_Status' : '',
                'Image'  : ''
            }


            try:
                url = soup.select_one('.css-aml4xx+ .css-1h1j0y3 .css-ac8spe').get('href')
                url = unquote(url)
                url = [url.split('?')[1]]
                url = [u.split('&')[0] for u in url]
                url = url[0]
                features['Website'] = url
            except Exception as e:
               features['Website'] = 'N/A'
               print('error:\t',e)
               pass


            try:
               features['Phone_No'] = soup.select_one('.border-color--default__373c0__1WSID+ .border-color--default__373c0__1WSID .css-aml4xx+ .css-1h1j0y3').text
            except Exception as e:
               features['Phone_No'] = 'N/A'
            try:
               features['Rating'] =soup.select_one('.overflow--hidden__373c0__1TJqF').get('aria-label')
            except Exception as e:
               features['Rating'] = 'N/A'
               print('error:\t', e)
               pass

            try:
               features['Image'] = soup.select_one(' .photo-header-media-image__373c0__rKqBU').get('src')
            except Exception as e:
               features['Image'] = 'N/A'
               print('error:\t', e)
               pass

            try:
               features['Reviews'] = soup.select_one('.arrange-unit-fill__373c0__3cIO5.nowrap__373c0__AzEKB .css-bq71j2').text
            except Exception as e:
               features['Reviews'] = 'N/A'
               print('error:\t', e)
               pass



            key_features = {}

            opening_status = [s.text for s in soup.select(' .day-of-the-week__373c0__14i-X')]

            values =   [s.text for s in soup.select('.no-wrap__373c0__HMqyD')]

            for index in range(0,len(opening_status)):
                 key_features[opening_status[index]] = values[index]
            #print(key_features)
            try:
               features['Opening_Status'] = key_features
            except Exception as e:
                features['Opening_Status'] = 'N/A'
                print('error:\t', e)
                pass

            print(features)



        self.driver.quit()





if __name__ == '__main__':
   scraper = Yelp()
   #links =
   scraper.parse()
   #scraper.parse_links(links)

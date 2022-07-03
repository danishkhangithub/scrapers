# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import urllib
import requests
import os
import re
import json
import datetime
import csv
import pandas as pd


# property scraper class
class Yelp(scrapy.Spider):
    # scraper name
    name = 'home bussiness'
    base_url = 'https://www.yelp.com/search?'
    params = {
     'find_desc': 'vehicle+dealerships',
     'find_loc':'canada',
     #'start' : ''
     }
    results = []
    current_page = 1

    page = 0
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"

     }
    page = 10
    filename = 'links2.csv'
    try:
      if (os.path.exists(filename) and os.path.isfile(filename)):
         os.remove(filename)
         print('Filed Removed')
    except OSError:
       print('File Not Found')
       pass

    all_links = []
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 3,
        'DOWNLOAD_DELAY': 10,
        'DOWNLOAD_TIMEOUT': 10,
    }

    # general crawler
    def start_requests(self):
            url = self.base_url + urllib.parse.urlencode(self.params)
            # initial HTTP request
            yield scrapy.Request(
                url=url,
                headers=self.headers,

                callback=self.parse
            )

    def parse(self, response):
        with open('links.csv', newline='') as csvfile:
          reader = csv.DictReader(csvfile)
          count  = 1
          for row in reader:
              url = row["Links"]


              yield response.follow(
                 url = url,
                 headers = self.headers,
                 callback = self.parse_cards
              )


    def parse_listing(self, response):

            lists = response.css('h3[class="css-1yx1rzi"]')

            try:
              for link in lists:
                  link = link.css('a[target = "_blank"]::attr(href)').get()
                  link =  'https://www.yelp.com/' + link
                  self.all_links.append(link)
                  print('\n\nlink:',link,'\n\n')
                  #yield response.follow(link, headers = self.headers, callback = self.parse_cards)
            except Exception as e:
                  print(e)


            #total_pages =  response.css('.text-align--center__09f24__1P1jK .css-e81eai::text').get()[5:7]
            total_pages = 24

            for i in range(0,total_pages):
                #self.page +=10
                if (int(self.page/10) < int(total_pages)):
                    self.page +=10
                    self.log('\n\n %s | %s\n\n ' %(self.page/10, total_pages))
                    next_page = response.url + '&start=' + str(self.page)
                    #print('\n\nnext_page:', next_page)

                    yield scrapy.Request(url = next_page, headers = self.headers, callback = self.parse_listing)

    def parse_cards(self,response):
         '''
         content = ''
         with open('Yelp1.html', 'r' ) as f:
           for line in f.read():
             content += line
         response = Selector(text=content)
         '''
         #response = Selector(text= contents)

         try:
          name =  response.css('h1[class="css-dyjx0f"]::text').get()

         except Exception as e:
          print(e)
          name = None
          pass


         try:
           address = response.xpath('//p[@class = " css-1p9ibgf" and contains(.,"Get Directions")]').xpath('following-sibling::p/text()').get()

         except Exception as e:
           address = None
           print(e)
           pass


         try:
           phone =  response.css('.border-color--default__09f24__NPAKY+ .border-color--default__09f24__NPAKY .css-na3oda+ .css-1p9ibgf::text').get()
         except Exception as e:
           phone = None
           print(e)
           pass


         try:
           website =  response.xpath('//p[@class = " css-na3oda" and contains(.,"Business website")]').xpath('following-sibling::p/a/text()').get()
         except Exception as e:
           website = None
           print(e)
           pass



         features = {
            'Name' : name,
            'Phone' : phone,
            'Address' : address,
            'Website_url': website,
            'Email' : ''
         }


         #self.results.append(features)
         #print('\n\nresults\n', features)

         self.find_email(website, features)

    def find_email(self,website, features):

        try:
          if website!= None:
             req = requests.get(website, headers = self.headers)
             if req.status_code == 200:
                soup = BeautifulSoup(req.text, 'html.parser')
                print('HTTP Connection Succed')
          else:
             print('Error')
        except requests.exceptions.HTTPError as er:
              print('\nHTTP ERROR\t', err)

        try:
           email = re.findall(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', soup.text)
           email = email[0]
        except Exception as e:
            print(e)
            email = None
            pass

        print(email)

        features['Email'] = email

        self.results.append(features)
        print(self.results)

        return self.results

    def to_csv(self):
        data = pd.DataFrame()
        data['Links'] = pd.Series(self.all_links).values
        data.to_csv('links.csv')

        print('\nemails\t:',self.all_links,'Total Emails:\t',len(self.all_links))
        print('Links Saved to CSV File.')


# main driver
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Yelp)
    process.start()
    #Yelp().to_csv()


    #Yelp.parse_cards(Yelp, '')

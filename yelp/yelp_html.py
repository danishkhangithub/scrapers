from bs4 import BeautifulSoup
from scrapy.selector import Selector
import requests
import csv
import re
import os
import pandas as pd
import json

class EmailScraper:

    filename = './csv_files/contacts31.csv'

    try:
       if (os.path.exists(filename) and os.path.isfile(filename)):
          os.remove(filename)
          print('Files is removed')
       else:
           print('File Not Found.')
    except OSError:
       pass

    def __init__(self):
       self.url = 'https://www.yelp.ca/biz/westminster-motor-corp-toronto-2?hrid=a9t2nd9gcuvVggpOPX2PiA&osq=vehicle+dealerships'
       self.results = []
       self.headers = {
              'USER-AGENT' :  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
                    }




    def fetch(self, url):
         print('HTTP GET request to URL: %s' % url, end='')
         s = requests.Session()
         response = s.get(url, headers=self.headers)
         print('HTTP GET REQUESTS To The URL %s | Status code: %s' % (response.url,response.status_code))

         return response


    def parse(self):


        contents = ''

        #for html in range()
        with open('./yelp_local/yelp.html', 'r') as html_file:
             for line in html_file.read():
                 contents+= line

        response = Selector(text= contents)

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
           req = requests.get(website, headers = self.headers)
           if req.status_code == 200:
              soup = BeautifulSoup(req.text, 'html.parser')
              print('HTTP Connection Succed')
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


    def to_csv(self, results):
        data = pd.DataFrame(results)
        data.to_csv('./csv_files/contacts31.csv')

        print('\nContacts\t:',json.dumps(results,indent = 2))
        print('Contacts Saved to CSV File.')

    def run(self):
       '''
       with open('links.csv', newline='') as csvfile:
          reader = csv.DictReader(csvfile)
          count  = 1
          for row in reader:
              url = row["Links"]
              print(url)
              response = self.fetch(url)
       '''
       #results = self.parse()
       #self.to_csv(results)



if __name__ == '__main__':
    scraper = EmailScraper()
#    scraper.run()
    scraper.parse()

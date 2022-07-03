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



    def fetch(self, url):
         print('HTTP GET request to URL: %s' % url, end='')
         s = requests.Session()
         response = s.get(url, params=self.params, headers=self.headers)
         print('HTTP GET REQUESTS To The URL %s | Status code: %s' % (response.url,response.status_code))

         return response


    def parse(self):
        '''
        contents = ''

        #for html in range()
        with open('./html_files/contacts31.html', 'r') as html_file:
             for line in html_file.read():
                 contents+= line
        '''

    def to_csv(self, results):
        data = pd.DataFrame(results)
        data.to_csv('./csv_files/contacts31.csv')

        print('\nContacts\t:',json.dumps(results,indent = 2),'Total Conatacts:\t',len(results))
        print('Contacts Saved to CSV File.')

    def run(self):
         #response = self.fetch(self.url)
         results = self.parse()
         #self.to_csv(results)



if __name__ == '__main__':
#    scraper = EmailScraper()
#    scraper.run()
    scraper.parse()

from bs4 import BeautifulSoup
from scrapy.selector import Selector
import requests
import csv
import re
import os
import pandas as pd
import json
import time

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
         time.sleep(2)
         print('HTTP GET REQUESTS To The URL %s | Status code: %s' % (response.url,response.status_code))

         return response


    def parse(self):

        '''
        contents = ''

        #for html in range()
        with open('./html_files/contacts31.html', 'r') as html_file:
             for line in html_file.read():
                 contents+= line

        soup = BeautifulSoup(contents, 'lxml')
        for card in soup.select('div.mini-card div.card > div.grid-2'):
           try:
             name = soup.select_one('h1[class="css-11q1g5y"]').text

           except Exception as e:
             print(e)
             name = None
             pass

           try:
             address = soup.find('p',{'class' : 'css-chtywg'}).text

           except Exception as e:
             address = None
             print(e)
             pass


           try:
              phone =  card.select_one('.css-aml4xx+ .css-1h1j0y3').text
           except Exception as e:
              phone = None
              print(e)
              pass


           try:
              website =  card.select_one('').text
           except Exception as e:
              website = None
              print(e)
              pass



           try:
             sector = card.select_one(' div:nth-child(1) > font:nth-child(7) > font').text.split(':')[1]

           except Exception as e:
             print(e)
             sector = None
             pass

           try:

             email =  ','.join([c['href']  for c in card.select_one('a').find_next_siblings("a") ])
             email =  re.findall(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)',email )
             email = email[0]
           except Exception as e:
              email = None
              print(e)
              pass


           features = {
              'Tile' : title,
              'Name' : name,
              'Sector' : sector,
              'Phone' : phone,
              'Email' : email,
              'Address' : address,
              'Website_url': website
           }


           self.results.append(features)
           print('\n\nlength\n',len(address), self.results)



        return self.results
        '''

    def download_html(self, response,count):
            with open('yelp%s.html' %(str(count)), 'w+') as f:
                f.write(response.text)
                time.sleep(2)
                #f.close()
            print('File No %s saved'%str(count))


    def to_csv(self, results):
        data = pd.DataFrame(results)
        data.to_csv('./csv_files/contacts31.csv')

        print('\nContacts\t:',json.dumps(results,indent = 2),'Total Conatacts:\t',len(results))
        print('Contacts Saved to CSV File.')

    def run(self):

       with open('links.csv', newline='') as csvfile:
          reader = csv.DictReader(csvfile)
          count  = 1
          for row in reader:
              url = row["Links"]
              response = self.fetch(url)
              self.download_html(response, count)
              count+=1
              break
       #results = self.parse()
       #self.to_csv(results)



if __name__ == '__main__':
    scraper = EmailScraper()
    scraper.run()
    #scraper.parse()

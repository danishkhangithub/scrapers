# import libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import time
import json
import sys
import csv
import os
import pandas as pd
import mysql.connector

class Scraper:

    url = 'https://www.otcmarkets.com/stock/GZIc/'

    results = []

    def __init__(self):
        self.chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'

        self.chrome_options = Options()
        #self.chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(
                                         executable_path= self.chrome_driver_path,
                                         options=self.chrome_options
             )
        self.mydb_con = mysql.connector.connect(
          host="localhost",
          user="danish-khan",
          password="12345",
          db='otc'
        )

        self.cur = self.mydb_con.cursor()


    def fetch(self, soup, i):
        if i == 'overview':
           self.overview(soup,i)



        elif i == 'quote' :
           self.quote(soup,i)

        elif i == 'news':
           self.news(i)

        elif i == 'disclosure':
            self.disclosure(i)


    def overview(self,soup,i):
        # try to remove the old csv
        file = 'overview.csv'
        try:
           if (os.path.exists(file)) and (os.path.isfile(file)):
              os.remove(file)
           else:
              print('file not found')
        except OSError:
           pass


        features = {}

        DailyHigh = soup.css('div[class= "_2XxiZo8FrF _1zf_cufeWm sc-htpNat dXhXYE sc-bdVaJa iHZvIS"] h2::text').get()

        features['DailyHigh'] = DailyHigh
        features['Change'] = soup.css('div[class= "_2XxiZo8FrF _1zf_cufeWm sc-htpNat dXhXYE sc-bdVaJa iHZvIS"] div[class="_2GSkTrHRjv sc-htpNat pyeRb sc-bdVaJa iHZvIS"] p::text').get()
        features['PercentChange'] = soup.css('div[class= "_2XxiZo8FrF _1zf_cufeWm sc-htpNat dXhXYE sc-bdVaJa iHZvIS"] div[class="_2GSkTrHRjv sc-htpNat pyeRb sc-bdVaJa iHZvIS"] p::text').getall()[1]
        features['BidPrice'] = soup.css('p[class="_2VWvG6yWU0"] strong::text').getall()[0].split('/')[0]
        features['AskPrice'] = soup.css('p[class="_2VWvG6yWU0"] strong::text').getall()[0].split('/')[1]
        features['BidSize'] = soup.css('p[class="_2VWvG6yWU0"] span::text').getall()[0].split('x')[0].replace('(','')
        features['AskSize'] = soup.css('p[class="_2VWvG6yWU0"] span::text').getall()[0].split('x')[1].replace(')','')


        results = []
        results.append(features)

        profile_details = pd.DataFrame(results)


        # store output to JSON file
        with open('overview.jsonl', 'a') as f:
            f.write(json.dumps(features, indent=2) + '\n')
        headers = features.keys()
        with open('overview.csv','a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames = headers)
            writer.writeheader()
            writer.writerows(results)


    def quote(self, soup,i):
        # try to remove the old csv
        file = 'quotes.csv'
        try:
           if (os.path.exists(file)) and (os.path.isfile(file)):
              os.remove(file)
           else:
              print('file not found')
        except OSError:
           pass


        features = {}
        category_list = soup.css('div[class= "_1G7n38q1bb sc-bdVaJa lbvrig"] label::text').getall()

        category_value = soup.css('div[class= "_1G7n38q1bb sc-bdVaJa lbvrig"] p::text').getall()


        for index in range(0, len(category_value)):
            features[category_list[index]] = category_value[index]

        results = []
        results.append(features)

        profile_details = pd.DataFrame(results)

        # store output to JSON file
        with open('quotes.jsonl', 'a') as f:
            f.write(json.dumps(features, indent=2) + '\n')
        headers = features.keys()
        with open('quotes.csv','a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames = headers)
            writer.writeheader()
            writer.writerows(results)

    def news(self,i):
         # try to remove the old csv
        file = 'news.csv'
        try:
           if (os.path.exists(file)) and (os.path.isfile(file)):
              os.remove(file)
           else:
              print('file not found')
        except OSError:
           pass

        results = []
        self.driver.get(self.url + str(i))
        time.sleep(5)
        for i in range(0,5):
             self.driver.execute_script("document.querySelector('._2sFaw3zGf1').click()")
             time.sleep(5)
             response = Selector(text= self.driver.page_source)
        soup = Selector(text = self.driver.page_source)
        news = soup.css('div[class = "sc-bdVaJa dMmFTA"] b::text').getall()
        link = soup.css('div[class = "sc-bdVaJa dMmFTA"] a::attr(href)').getall()
        link = [ 'https://www.otcmarkets.com'+ l for l in link]
        for index in range(0, len(news)):
            results.append({
              'News' : news[index],
              'News_link' : link[index]
            })


        profile_details = pd.DataFrame(results)


        headers = results[0].keys()
        with open('news.csv','a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames = headers)
            writer.writeheader()
            writer.writerows(results)


    def disclosure(self, i):
        # try to remove the old csv
        file = 'disclosure.csv'
        try:
           if (os.path.exists(file)) and (os.path.isfile(file)):
              os.remove(file)
           else:
              print('file not found')
        except OSError:
           pass


        features = {}

        '''
        content = ''
        with open('disclosure.html','r') as html:
           for line in html.read():
               content +=line
        response = Selector(text = content)
        '''
        self.driver.get(self.url + str(i))
        time.sleep(5)
        for i in range(0,5):
             self.driver.execute_script("document.querySelector('._2sFaw3zGf1').click()")
             time.sleep(5)
             response = Selector(text= self.driver.page_source)

        time.sleep(5)
        response = Selector(text = self.driver.page_source)
        table = response.css('div[class = "_15ABW-Db6z"] table')
        table_heads = table.css('thead')
        table_heads = table_heads.css('tr th')
        table_heads = table_heads.css('div[class = "_2X61BpqpLL _1_A2O0SJBN"]::text').getall()

        results = []
        table_body = table.css('tbody')
        date = response.css('._15ABW-Db6z ._3MCbKzRK_6:nth-child(1) span::text').getall()
        title = response.css('._15ABW-Db6z ._3MCbKzRK_6:nth-child(2) span a::text').getall()
        link = response.css('._15ABW-Db6z ._3MCbKzRK_6:nth-child(2) span a::attr(href)').getall()
        period_end_date = response.css('._15ABW-Db6z ._3MCbKzRK_6:nth-child(3) span::text').getall()
        status = response.css('._15ABW-Db6z ._3MCbKzRK_6:nth-child(4) span::text').getall()

        for index in range(0, len(date)):
            results.append({
              'Date' : date[index],
              'Title' : title[index],
               'Link' : link[index],
              'Period_end_date' : period_end_date[index],
              'Status' : status[index]

            })


        headers = results[0].keys()
        with open('disclosure.csv','a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames = headers)
            writer.writeheader()
            writer.writerows(results)
        print('file saved')


    def run(self):

        data_list = ['overview','disclosure','news','quote']
        for i in data_list:
               self.driver.get(self.url + str(i))
               time.sleep(5)

               response = Selector(text= self.driver.page_source)


               self.fetch(response, i)


        self.driver.close()

    def db(self):
         #self.overview_db()
         #news_db()
         self.quotes_db()
         #disclosure_db()
    def news_db(self):

         #create table
         self.cur.execute("""DROP TABLE IF EXISTS otc_news""")
         self.cur.execute(''' CREATE TABLE IF NOT EXISTS otc_news
                       (Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        News varchar(255),
                        News_link VARCHAR(255))

                        ''')


         df = pd.read_csv('news.csv')
         df = pd.DataFrame(df)
         for row in df.itertuples():
                 self.cur.execute('''INSERT INTO otc_news(
                          news,
                          news_link )
                          VALUES("%s", "%s")''',
                          (row.News,row.News_link
                                  ))
         self.mydb_con.commit()

    def overview_db(self):
       #create table
         self.cur.execute("""DROP TABLE IF EXISTS otc_overview""")
         self.cur.execute(''' CREATE TABLE IF NOT EXISTS otc_overview
                       (Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        DailyHigh integer,
                        Change integer),
                        PercentChange Decimal(2,2),
                        BidPrice ,
                        AskPrice,
                        AskSize,
                        BidSize

                        ''')


         df = pd.read_csv('overview.csv')
         df = pd.DataFrame(df)
         for row in df.itertuples():
                 self.cur.execute('''INSERT INTO otc_news(
                          DailyHigh,
                          Change,
                          PercentChange,
                          BidPrice,
                          AskPrice,
                          AskSize,
                          BidSize
                           )
                          VALUES("%s", "%s","%s","%s","%s","%s","%s")''',
                          (row.DailyHigh,
                           row.Change,
                           row.PercentChange,
                           row.BidPrice,
                           row.AskPrice,
                           row.AskSize,
                           row.BidSize
                                  ))
         self.mydb_con.commit()
    def disclosure(self):
       #create table
         self.cur.execute("""DROP TABLE IF EXISTS otc_disclosure""")
         self.cur.execute(''' CREATE TABLE IF NOT EXISTS otc_disclosure
                       (Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        Date integer,
                        Title varchar(20),
                        Link varchar(20) ,
                        Period_end_date,
                        Status varchar(10)
                         )
                        ''')


         df = pd.read_csv('disclosure.csv')
         df = pd.DataFrame(df)
         for row in df.itertuples():
                 self.cur.execute('''INSERT INTO otc_news(
                          Date
                          Title,
                          Link ,
                          Period_end_date,
                          Status
                           )
                          VALUES("%s", "%s","%s","%s","%s")''',
                          (row.Date,
                           row.Title,
                           row.Link,
                           row.Period_end_date,
                           row.Status,

                                  ))
         self.mydb_con.commit()
    def quotes_db(self):
       #create table
         self.cur.execute("""DROP TABLE IF EXISTS otc_quotes""")
         self.cur.execute(''' CREATE TABLE IF NOT EXISTS otc_quotes
                       (Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        open integer,
                        Daily_Range varchar(20),
                        Volume varchar(20),
                        Dividend varchar(20),
                        PreyClose varchar(10),
                        52wk_Range varchar(20),
                        Average_Vo_(3) varchar(20)
                         )
                        ''')


         df = pd.read_csv('disclosure.csv')
         df = pd.DataFrame(df)
         for row in df.itertuples():
                 self.cur.execute('''INSERT INTO otc_news(
                          Date
                          Title,
                          Link ,
                          Period_end_date,
                          Status
                           )
                          VALUES("%s", "%s","%s","%s","%s")''',
                          (row.Date,
                           row.Title,
                           row.Link,
                           row.Period_end_date,
                           row.Status,

                                  ))
         self.mydb_con.commit()


    def __del__(self):
        self.mydb_con.close()
        print('Database connection closed')
        # close the driver
        self.driver.close()




if __name__ == '__main__':
#    scraper = Scraper()
#    scraper.run()
    df = Scraper()
    df.db()

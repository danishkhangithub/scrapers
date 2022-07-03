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

class Scraper:

    url = 'https://www.otcmarkets.com/stock/GZIc/'

    results = []

#    def __init__(self):
#        self.chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'
#
#        self.chrome_options = Options()
#        #self.chrome_options.add_argument('--headless')
#
#        self.driver = webdriver.Chrome(
#                                         executable_path= self.chrome_driver_path,
#                                         options=self.chrome_options
#             )

    def overview(self, soup, i):
        features = {}
        if i == 'overview':
            name = soup.css('div[class= "_2XxiZo8FrF _1zf_cufeWm sc-htpNat dXhXYE sc-bdVaJa iHZvIS"] h2::text').get()

            features['Name'] = name



        elif i == 'quote' :
            category_list = soup.css('div[class= "_1G7n38q1bb sc-bdVaJa lbvrig"] label::text').getall()

            category_value = soup.css('div[class= "_1G7n38q1bb sc-bdVaJa lbvrig"] p::text').getall()


            for index in range(0, len(category_value)):
                features[category_list[index]] = category_value[index]

        elif i == 'news':
           self.driver.get(self.url + str(i))
           time.sleep(5)
#           for i in range(0,5):
#               self.driver.execute_script("document.querySelector('._2sFaw3zGf1').click()")
#               time.sleep(5)
#               response = Selector(text= self.driver.page_source)
           soup = Selector(text = self.driver.page_source)
           news = soup.css('div[class = "sc-bdVaJa dMmFTA"] b::text').getall()

           features['News'] = news


        self.results.append(features)
        #print(self.results)
        return features




    def run(self):

        data_list = ['overview','quote','news', 'disclosure']
        for i in data_list:
               self.driver.get(self.url + str(i))
               time.sleep(5)

               response = Selector(text= self.driver.page_source)


               self.overview(response, i)
        self.driver.close()
        print(self.results)

    def test(self):
        features = {}
        content = ''
        with open('disclosure.html','r') as html:
           for line in html.read():
               content +=line
        response = Selector(text = content)
        table = response.css('div[class = "_15ABW-Db6z"] table')
        table_heads = table.css('thead')
        table_heads = table_heads.css('tr th')
        table_heads = table_heads.css('div[class = "_2X61BpqpLL _1_A2O0SJBN"]::text').getall()
        #print(table_heads)
        results = []
        table_body = table.css('tbody')
        for tr in table_body.css('tr'):
            tbody = [tr.css('td > span *::text ').getall() for tr in table_body.css('tr')]
        for index in range(0, len(tbody)):
            features['Published_date'] = tbody[index][0]
            features['Title'] = tbody[index][1]
            features['Period_Date'] = tbody[index][2]
            features['Status'] = tbody[index][3]
            #print(tbody[index][1])


            print(features)
            results = []
            results.append(features)
            # store output to JSON file
            with open('otc.jsonl', 'a') as f:
                f.write(json.dumps(features, indent=2) + '\n')
            headers = features.keys()
            with open('disclosure.csv','a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames = headers)
                writer.writeheader()
                writer.writerows(results)




if __name__ == '__main__':
    scraper = Scraper()
    #scraper.run()
    scraper.test()

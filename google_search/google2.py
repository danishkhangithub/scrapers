# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
import urllib
import json
import datetime
import time
import sys


base_url = 'https://www.google.com/'

query = 'uk cardiologist'

chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'

chrome_options = Options()
#chrome_options.add_argument('--headless')

driver = webdriver.Chrome(
  executable_path=chrome_driver_path, options=chrome_options
)

driver.get(base_url)

search = driver.find_element_by_css_selector('input[name= "q"]').send_keys(query,Keys.ENTER)
#search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='submit']")))


more_page = driver.find_element_by_xpath('//a[@class="tiS4rf Q2MMlc"]').click()
time.sleep(5)


links = driver.find_elements_by_xpath('//a[@class="C8TUKc rllt__link a-no-hover-decoration"]')
for link in links:
    link.click()
    time.sleep(4)
    res =  Selector(text = driver.page_source)

    details = {
     'Name' : res.xpath('//div[@class="SPZz6b"]/h2/span/text()').get(),
     'Address' : res.xpath('//div[@class="zloOqf PZPZlf"]/span[@class="LrzXr"]/text()').get(),
     'Phone ' : res.xpath('//div[@class="zloOqf PZPZlf"]/span//a/span/text()').get(),
     'Website ' : res.xpath('//div[@class="QqG1Sd"]/a/@href').get()
      }

    print(details)
    #website_url = res.xpath('//div[@class="QqG1Sd"]/a/@href').get()
    #driver.get('https://drboonlim.co.uk/appointment-booking/')

#    res2 = Selector(text = driver.page_source)
#    print(res2)





time.sleep(5)
driver.close()

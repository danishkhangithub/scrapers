from selenium import webdriver
from scrapy.selector import Selector
import time
import sys
import csv
import os



#
#driver = webdriver.Chrome('/home/danish-khan/scrapers/researchgate/chromedriver')
#
#driver.get('https://www.linkedin.com/login')    
#  
#driver.find_element_by_id('username').send_keys('danishkhankd237@gmail.com') 
#
#Enter username of linkedin account here
#
#driver.find_element_by_id('password').send_keys('dankhanish446')  
#
#Enter Password of linkedin account here
#driver.find_element_by_xpath("//button[@type='submit']").click()
#
#
data = ''
with open('linkdn1.html', 'r') as f:
   for line in f.read():
      data += line

results = []
search = Selector(text = data)
#profiles = search.xpath('//span[@class="entity-result__title-text  t-16"]/a/@href').getall()
#profiles = [profile.xpath('@href') for profile in profiles]

#Details = {
#  'Name' : search.xpath('//h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]/text()').get(),
#  'Education' : search.xpath('//h3[@class="pv-entity__school-name t-16 t-black t-bold"]/text()').get(),
#}
#print(Details)

#contact_url = profiles + 'detail/contact-info'
#driver.get(contact_url)
#time.sleep(2)

contact_search = Selector(text = data)

#email = contact_search.xpath('//a[@class = "pv-contact-info__contact-link link-without-visited-state t-14"]/@href')
#print(email)

#for prof in profiles:
#    try: 
#      driver.get(str(prof))
#      time.sleep(2)
#    except Exception as e:
#       print('error:',e)
#    
#driver.close()

url = 'https://www.linkedin.com/in/maira-tanweer-b4550410b?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABupTWUBpxgATilDl8RpgzuL1CXVyZdAZRg'


url = url.split('?')[0]
print(url) 


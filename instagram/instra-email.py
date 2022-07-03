import scrapy 
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib
import re
import json


content = ''
with open('instra1.html', 'r') as f:
  for line in f.read():
      content +=line
response = Selector(text = content)
print(response)
#details = {
#  'Address' : res.xpath('//div[@class="zloOqf PZPZlf"]/span[@class="LrzXr"]/text()').get(),
#  'Phone ' : res.xpath('//div[@class="zloOqf PZPZlf"]/span//a/span/text()').get(),
#  'Website ' : res.xpath('//a[@class="xFAlBc"]/@href').get()
#}
#
#print(details)    
#website =  res.xpath('//div[@class="QqG1Sd"]/a/@href').get()
#
#
#print(website)
  
#print(content)
#em = "pa@drboonlim.co.uk"
#
#email = re.findall('[\w+@\w+\.\w+\.\w+]',em)
#email = ''.join(email)
#email = re.findall('\+@\s+',em)
#
#print(email)



#contacts = response.css('script[type="application/ld+json"]::text').get()
#print(contacts)
#contacts = json.loads(contacts)
#
#contacts = json.dumps(contacts, indent = 2)
#
#concats = contacts['description']
#
#print(concats)
#

# email = re.findall('[\w+@\w+\.\w+\.\w+]',contacts)

email = re.findall('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}',str(content))
#/[\w\.-]+@[\w\.-]+/gm 
#email = ''.join(email)
#email = re.findall('\+@\s+',em)

print(email[0])



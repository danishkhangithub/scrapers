import scrapy 
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib
import re
import json

#content = ''
#with open('res1.html', 'r') as f:
#  for line in f.read():
#      content +=line
#res = Selector(text = content)
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


#details = {
#         'Name' : res.xpath('//div[@class="SPZz6b"]/h2/span/text()').get(),
#         'Address' : res.xpath('//div[@class="zloOqf PZPZlf"]/span[@class="LrzXr"]/text()').get(),
#         'Phone ' : res.xpath('//div[@class="zloOqf PZPZlf"]/span//a/span/text()').get(),
#         'Website ' : res.xpath('//div[@class="QqG1Sd"]/a/@href').get(),
#         'Email' : ''
#                  }
#print(details)
#


params = {
      "tbs": "lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2",
      "tbm": "lcl",
      "sxsrf": "ALeKk01BW86aXeyv0NqmJYfOhvFCjtqsGg:1623217868172",
      "q": "beverages%20in%20atlanta%20georgia",
      "rflfq": "1",
      "num": "10",
      "sa": "X",
      "ved": "2ahUKEwjQkbPj7YnxAhVUgFwKHTUIDQsQjGp6BAgMEE0",
      "biw": "1366",
      "bih": "624",
      "rlst": "hd:;si:;mv:[[33.9412923,-84.25019669999999],[33.6955892,-84.6178867]];",
      'start': 0
    }
for page in range(0,10):
    base_url = urllib.parse.urlencode(params)
    

    params['start'] + page
    params['start'] += 10
    print(params)
    





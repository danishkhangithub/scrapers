# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import os
import json
import datetime
import re

# property scraper class
class ResidentialSale(scrapy.Spider):
    # scraper name
    name = 'therapists'
    base_url = 'https://www.google.com/search?'
    
    params = {
        'tbs': 'lf:1,lf_ui:2',
        'tbm': 'lcl',
        'sxsrf': 'ALeKk03VQw0DRsdOXDInnN69GZXxEq8Uqg:1620538470973',
        'q': 'uk cardiologist',
        'rflfq': 1,
        'num': 10,
        'sa': 'X',
        'ved': '2ahUKEwiQs6Cf8LvwAhWWgVwKHV75CNwQjGp6BAgFEFs',
        'cshid': 1620538493841370,
        'biw': 1366,
        'bih': 566
        }
    
    # headers
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'CGIC=InZ0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIz; HSID=AenmNVZxnoADsXz_x; SSID=AjbLhhwkjh8f3FOM8; APISID=IqkNtUA0V2DXlees/A0tA9iPSadMC2X6dt; SAPISID=8-N4B06I_D5N1mvR/AleccT6Zt0QllrukC; CONSENT=YES+UA.en+; OTZ=5204669_48_48_123900_44_436380; SID=rAd3UAFN_dCIGQ87HqDZZGiNyxdz0dL4dZKy_XquqSr_CHTzqSzfDdNTfLmA2xCMEZOZMA.; ANID=AHWqTUnDWUSHdvWhJiIoPxMAKYXmVtHCQIq7LBMYgiSlZZr3AMGTwY2aVUdjeY7z; NID=193=QImFbOa1vnKpflG8yJytqPXbJYJ9k8fWbIzQMGExsMa4g5oJwdnI56WNjgEVFAyAPJ1SEEOQ-zlW4HAUv-JLj0yAUImTgeT1syDIgFTMWAqxdz10lWRlzFC-3Fmjv6xJcqm2o6RKI50dmb7GetiheNdSAYPkAjng_c0lOHoXZLmtMwFOpkPTrQwVyUW8R2x4o1ux3OW3_kEbR_BREowRV8lVqrsnyo1ffC_Pm40zf81k7aS0cv9esYweGHF6Lxd532z4wA; 1P_JAR=2019-12-06-16; DV=k7BRh0-RaJtZsO9g7sjbrkcKoUjC7RYhxDh5AdfYgQAAAID1UoVsAVkvPgAAAFiry7niUB6qLgAAAGCQehpdCXeKnikKAA; SEARCH_SAMESITE=CgQIvI4B; SIDCC=AN0-TYv-lU3aPGmYLEYXlIiyKMnN1ONMCY6B0h_-owB-csTWTLX4_z2srpvyojjwlrwIi1nLdU4',
        'pragma': 'no-cache',
        'referer': 'https://www.google.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.142 Chrome/75.0.3770.142 Safari/537.36'
        }
    
    try:
       os.remove('abx.csv')
    except OSError:
       pass   
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
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
    def parse(self, res):
       
       content = ''
       with open('res1.html', 'r') as f:
          for line in f.read():
             content +=line
       res = Selector(text=content)
        
#       emails = re.findall('{\w+@\w+\.\w+\w+}', res)    
#       print(emails)
       
       
#       yield response.follow(
#             url = ,
#             headers = self.headers,
#             callback = 
#       )
        '''
        with open('qsranks.csv', 'a') as csv_file:
             writer = csv.DictWriter(csv_file, fieldnames=items.keys())
             writer.writerow(items)

        '''
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ResidentialSale)
    process.start()
    
    #ResidentialSale.parse(ResidentialSale, '')
    

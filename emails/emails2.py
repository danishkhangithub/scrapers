from bs4 import BeautifulSoup
from scrapy.selector import Selector
import requests
import csv
import re
import os
import pandas as pd

class EmailScraper:

    filename = 'emails1.csv'

    try:
       if (os.path.exists(filename) and os.path.isfile(filename)):
          os.remove(filename)
       else:
           print('File Not Found.')
    except OSError:
       pass

    def __init__(self):
       self.url = 'https://www.google.com/search?'
       self.results = []
       self.params = {
            'q': 'ceo o founder e-commerce new york contact email "gmail" site:linkedin.com',
            "sxsrf": "ALiCzsanz1txduedFqXWF5JGtp2ChSNXTQ:1655386219683",
            "ei": "azCrYtuVKc6Xxc8PmfC6mAE",
            "start": 0,
            "sa": "N",
            "ved": "2ahUKEwib99ucirL4AhXOS_EDHRm4DhMQ8NMDegQIARA9"
            }

       # headers
       self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'cookie': 'CGIC=InZ0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIz; HSID=AenmNVZxnoADsXz_x; SSID=AjbLhhwkjh8f3FOM8; APISID=IqkNtUA0V2DXlees/A0tA9iPSadMC2X6dt; SAPISID=8-N4B06I_D5N1mvR/AleccT6Zt0QllrukC; CONSENT=YES+UA.en+; OTZ=5204669_48_48_123900_44_436380; SID=rAd3UAFN_dCIGQ87HqDZZGiNyxdz0dL4dZKy_XquqSr_CHTzqSzfDdNTfLmA2xCMEZOZMA.; ANID=AHWqTUnDWUSHdvWhJiIoPxMAKYXmVtHCQIq7LBMYgiSlZZr3AMGTwY2aVUdjeY7z; NID=193=QImFbOa1vnKpflG8yJytqPXbJYJ9k8fWbIzQMGExsMa4g5oJwdnI56WNjgEVFAyAPJ1SEEOQ-zlW4HAUv-JLj0yAUImTgeT1syDIgFTMWAqxdz10lWRlzFC-3Fmjv6xJcqm2o6RKI50dmb7GetiheNdSAYPkAjng_c0lOHoXZLmtMwFOpkPTrQwVyUW8R2x4o1ux3OW3_kEbR_BREowRV8lVqrsnyo1ffC_Pm40zf81k7aS0cv9esYweGHF6Lxd532z4wA; 1P_JAR=2019-12-06-16; DV=k7BRh0-RaJtZsO9g7sjbrkcKoUjC7RYhxDh5AdfYgQAAAID1UoVsAVkvPgAAAFiry7niUB6qLgAAAGCQehpdCXeKnikKAA; SEARCH_SAMESITE=CgQIvI4B; SIDCC=AN0-TYv-lU3aPGmYLEYXlIiyKMnN1ONMCY6B0h_-owB-csTWTLX4_z2srpvyojjwlrwIi1nLdU4',
            'pragma': 'no-cache',
            'referer': 'https://www.google.com/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.142 Chrome/75.0.3770.142 Safari/537.36'
            }

    def fetch(self, url):
         print('HTTP GET request to URL: %s' % url, end='')
         s = requests.Session()
         response = s.get(url, params=self.params, headers=self.headers)
         #print('HTTP GET REQUESTS To The URL %s | Status code: %s' % (response.url,response.status_code))

         return response


    def parse(self,response):
        contents = ''

        #for html in range()
        with open('emails.html', 'r') as html_file:
             for line in html_file.read():
                 contents+= line

        soup = BeautifulSoup(contents, 'lxml')

        email = ','.join([i.text for i in soup.select('[data-content-feature = "1"]')])

        emails = re.findall(r'[\w+\.-]+@[\w\.-]+',email)

        return emails

    def to_csv(self, results):
        data = pd.DataFrame()
        data['Emails'] = pd.Series(results).values
        data.to_csv('emails1.csv')

        print('\nemails\t:',results,'Total Emails:\t',len(results))
        print('Emails Saved to CSV File.')

    def run(self):
         response = self.fetch(self.url)
         results = self.parse(response)
         self.to_csv(results)



if __name__ == '__main__':
    scraper = EmailScraper()
    scraper.run()
    #scraper.parse()

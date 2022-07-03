# import packages
import scrapy 
from scrapy.selector import Selector 
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import csv
import json
import os

class Speakers(scrapy.Spider):
    name = 'speakers'
    base_url = ''
    headers = { 
          "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    } 
    # csv file 
    file = 'data.csv'
    try:
      if(os.path.exists(file) and os.path.isfile(file)):
         os.remove(file)
         print('file deleted')
      else:      
         print('file not found')
    except OSError:
       pass 
                    
     # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
    }
    
    
    def start_requests(self):
        yield scrapy.Request(
            url = self.base_url,
            headers = self.headers,
            callback = self.parse
                )  

    def parse(self, response):
        content = ''
        with open('res1.html', 'r') as f:
           for line in f.read():
              content +=line
        response = Selector(text = content)
        # beautifulsoup
        content = BeautifulSoup(content, 'lxml')
        #print(content)
         
        # top coordinates
        tops = [int(item.split('top:')[-1].split('px;')[0]) for item in response.css('style::text').get().split('}\n') if 'page_useddemo-gear' in item  and 'top:' in item ]
        
        # map top coordinates in pixels to class names
        coordinates = [
          {
          'class' : item.split('{')[0][1:-1],
          'top' : int(item.split('top:')[-1].split('px;')[0]) 
          } 
          for item in response.css('style::text').get().split('}\n') 
             if 'page_useddemo-gear' in item  and 'top:' in item
         ]
   
        # init raw data list
        data_raw = []
        # loop over raw data_raw
        for top in tops:
            # loop over top coordinates mapped to class names        
            for entry in coordinates:
                # match entries in the order presented in the website
                if entry['top'] == top:
                    #print('\n\n\nentry class',entry['class'],'\n\n\n') 
                    try:
                       try:
                          # append image urls
                          #data_raw.append('http://audioeden.com/' + response.css('img[class="%s"]::attr(src)') %(entry['class']))
                          
                          data_raw.append('http://audioeden.com' + content.find('img', {'class': entry['class']})['src'])
                          #print('\ndata_raw',data_raw,'\n')
                          #print('\nimages','http://audioeden.com' + content.find('img', {'class': entry['class']})['src'])
                       except Exception as e:
                          pass
                          #print('\nerror\t',e)
                       # append descriptions and prices
                       data_raw.append(content.find('div', {'class': entry['class']}).text.strip())
                       #print('\nappend',content.find('div', {'class': entry['class']}).text.strip())   
                    except:
                      pass

        # init output data list
        data = []
        
        # looping over data list
        for index in range(5,len(data_raw)):          
           #pick up description
           if len(data_raw[index]) > 10 and 'http' not in data_raw[index]:            
              # set up index offset in case of image URL
              if 'http' not in data_raw[index + 1]: 
                  offset = 1
              else:
                  offset = 2
              # pick up prices
              if len(data_raw[index + offset]) < 10 and len(data_raw[index + offset + 1]) < 10:               
                try:
                    # map items
                    features = {
                        'description': data_raw[index],
                        'selling_price': data_raw[index + offset],
                        'retail_price': data_raw[index + offset + 1],
                        'image_url': []
                    }
                    print(features) 
                    if 'http' in data_raw[index - 1]:
                        features['image_url'].append(data_raw[index - 1])
                    
                    if 'http' in data_raw[index + 1]:
                        features['image_url'].append(data_raw[index + 1])
                    
                    # append mapped row to data list
                    data.append(features)
                
                except:
                  pass


if __name__ == '__main__':
#   process = CrawlerProcess()
#   process.crawl(Speakers)
#   process.start()
    Speakers.parse(Speakers,'')
   
    

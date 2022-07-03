# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import os
import json
import datetime

# property scraper class
class ResidentialSale(scrapy.Spider):
    # scraper name
    name = 'therapists'
    base_url = 'https://gateway.reddit.com/desktopapi/v1/subreddits/Gold?'
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    
    params = {
      "rtj": "only",
      "redditWebClient": "web2x",
      "app": "web2x-client-production",
      "allow_over18": "",
      "include": "prefsSubreddit",
      "after": "t3_ne1ic2",
      "dist": "8",
      "layout": "card",
      "sort": "hot",
      "geo_filter": "PK"
      }

    
    '''
    try:
       os.remove('abx.csv')
    except OSError:
       pass 
    '''
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

    # general crawler
    def start_requests(self):
       
            # initial HTTP request
            yield scrapy.Request(
                url=self.base_url + urllib.parse.urlencode(self.params),
                headers=self.headers,
                callback=self.parse
                      )
    def parse(self, response):
        json_data = json.loads(response.text)
        
        for post in json_data['posts']:
            post_url = json_data['posts'][post]['permalink']
            
       
       
            yield response.follow(
                 url = post_url,
                 headers = self.headers,
                 callback = self.post
            )
            
            
        self.params['after'] = json_data['token']
        self.params['dist'] = json_data['dist']
        
        # generate Api url
        url = self.base_url + urllib.parse.urlencode(self.params)
        
        # print debug info
        print('Scrolling page... | next URL: %s\n\n' % url)
        
        # make recursive http request to the next infinite scroll page
        yield scrapy.Request(
              url = url,
              callback = self.parse
        )        
        
    def post(self,response):
        post = {
            'Title' : response.css('h1._eYtD2XCVieq6emjKBH3m::text').get(),
            'Description' : response.css('p._1qeIAgB0cPwnLhDF9XSiJM::text').get(),
            'Comments' : response.css('p._1qeIAgB0cPwnLhDF9XSiJM::text').getall()

        }
        print(json.dumps(post, indent = 2))  
        
        with open('posts.jsonl', 'a') as f:
           f.write(json.dumps(post, indent = 2) + '\n')

        
        
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ResidentialSale)
    process.start()
    
    #ResidentialSale.parse(ResidentialSale, '')
    

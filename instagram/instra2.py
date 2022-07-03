# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import os
import json
import datetime
import csv


# property scraper class
class ResidentialSale(scrapy.Spider):
    # scraper name
    name = 'therapists'
    base_url = 'https://www.instagram.com/onaka.vegan/'
    tag = ''
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    try:
       os.remove('instragram1.csv')
    except OSError:
       pass   
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 2
    }

    # general crawler
    def start_requests(self):
            url = self.base_url #+ self.tag
            # initial HTTP request
            yield scrapy.Request(
                url=url,
                headers=self.headers,
               
                callback=self.parse
                      )
    def parse(self, res):
#        content = ''
#        with open('instra2.html', 'r') as f:
#           for line in f.read():
#             content +=line
#        
#        res = Selector(text = content)
    
         

        ''' 
        data = [script for script in res.css('script::text').getall() if 'window._sharedData = ' in script]
        data = [d.split('window._sharedData = ')[-1].replace(' ', '').rstrip(';') for d in data]
        for i in data:
          data = json.loads(i)
          #data = json.dumps(data, indent = 2)
          data = data['entry_data']['ProfilePage']#[0]
          #data = json.dumps(data, indent = 2)
          print('\n\n',json.dumps(data, indent = 2) ,'\n\n')
          for user in data:
              user_data = user['graphql']['user']
              followers = user_data['edge_followed_by']['count']
              following = user_data['edge_follow']['count']
              full_name = user_data['full_name']
              bio = user_data['biography']
              #user_data = json.dumps(bio, indent = 2)
              website = user_data['external_url']
              user_id = user_data['id']
              username = user_data['username']
              profile_pic = user_data['profile_pic_url']
              profile_pic_hd = user_data['profile_pic_url_hd'] 
              business_profile = user_data['is_business_account']
              business_name = user_data['business_category_name']
              private_profile = user_data['is_private']
              verified_profile = user_data['is_verified']
              fb_page = user_data['connected_fb_page']
              email =  user_data['business_email']
              phone_no = user_data['business_phone_number']
              no_of_posts = user_data['edge_owner_to_timeline_media']['count']
              details = {
                 'Name' : full_name,
                 'User_name' : username,
                 'Followers' : followers,
                 'Followings' : following,
                 'Id' : user_id,
                 'Bio' : bio,
                 'Website' : website,
                 'Profile_pic' : profile_pic,
                 'Bussiness_profiles': business_profile,
                 'Bussiness_name' : business_name,
                 'Email' : email,
                 'Phone ': phone_no,
                 'No of posts' : no_of_posts
              }        
              #print(details)
              names = details.keys()
            
        '''
            
            
#       yield response.follow(
#             url = ,
#             headers = self.headers,
#             callback = 
#       )
        
#              with open('instragram1.csv', 'a') as csv_file:
#                writer = csv.DictWriter(csv_file, fieldnames=names)
#                writer.writerow(details)
#        
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ResidentialSale)
    process.start()
    
    #ResidentialSale.parse(ResidentialSale, '')
    

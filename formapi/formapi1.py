import json
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import FormRequest
import urllib
import os
import json
import datetime


class MySpider(scrapy.Spider):
    name = 'myspider'

    #different url

    start_urls = ['https://stackoverflow.com/questions/tagged/web-scraping']
    url = 'https://3ilkbk4xb6-3.algolianet.com/1/indexes/*/objects?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.30.0&x-algolia-application-id=3ILKBK4XB6&x-algolia-api-key=58f07d980dd16d0423322ca96aa03915'

    formdata = {
       "requests":[{"indexName":"prod_products","objectID":"b2842ffa-96b4-4a05-b811-fc9cc76cae36"},{"indexName":"prod_products","objectID":"d196649e-371e-4240-8bae-dfc96f82ba90"},{"indexName":"prod_products","objectID":"96d6ee6e-47aa-4e97-bddd-8b29f2edac06"},{"indexName":"prod_products","objectID":"12b8784b-384c-45d7-93d7-72419bfcc000"},{"indexName":"prod_products","objectID":"f717a363-0ff3-4a8e-9a99-b8c5a4c3db25"},{"indexName":"prod_products","objectID":"96d41557-5b02-4235-94d8-efe8d6f8d73b"},{"indexName":"prod_products","objectID":"13488e32-d268-4f84-8c3a-632ba0b3fe4f"},{"indexName":"prod_products","objectID":"c8925b90-d547-46ff-a617-6bbc81e3c20e"},{"indexName":"prod_products","objectID":"39308bc4-bdb8-463d-bc71-c36517eb8990"},{"indexName":"prod_products","objectID":"46c5cb4f-5292-4dc2-81c8-4248a42349ad"},{"indexName":"prod_products","objectID":"e1f915de-fef2-43b8-a6fe-2d4054f57515"},{"indexName":"prod_products","objectID":"a66be657-18f2-434b-911e-e1e3fd3be78d"},{"indexName":"prod_products","objectID":"7bd79edd-ea30-4472-afb9-d26fcae7a466"},{"indexName":"prod_products","objectID":"a032aa4a-702f-4dbe-bcc7-35aa62192bb8"},{"indexName":"prod_products","objectID":"220ce594-011d-44bc-bc30-935ebc5bcd5f"},{"indexName":"prod_products","objectID":"47a23ce2-19ee-4df3-a337-576bc29abde8"},{"indexName":"prod_products","objectID":"6c106d90-95a2-4e29-b692-829f8b3d81cd"},{"indexName":"prod_products","objectID":"e9f745c4-3298-4af1-b74c-71e170bc051e"},{"indexName":"prod_products","objectID":"391d6f60-843a-4276-a13e-2f5fd28a1d93"},{"indexName":"prod_products","objectID":"72f6e9cc-81cb-4231-bf9e-a0a09bc953b1"},{"indexName":"prod_products","objectID":"8f28dae4-bb78-48bf-b5d7-8efa97e5a89b"},{"indexName":"prod_products","objectID":"94e1423c-4171-471c-a3e5-800a2136b304"},{"indexName":"prod_products","objectID":"9f6528b2-986f-4110-bed3-27a097db98c4"},{"indexName":"prod_products","objectID":"ff6cf963-f71c-4c6c-bb37-09985c8198b8"},{"indexName":"prod_products","objectID":"99e25d4f-dec6-4f60-a24c-52e30cf634df"},{"indexName":"prod_products","objectID":"b79e5a3e-3b70-462d-b1ae-9f1f5e8df2a8"},{"indexName":"prod_products","objectID":"7d12980f-39bc-42ee-bba1-285faaed2725"},{"indexName":"prod_products","objectID":"58e39b11-adfc-4bb2-93f9-b32283d7be91"},{"indexName":"prod_products","objectID":"e8407b4a-41c0-458e-865f-5e3513d08c25"},{"indexName":"prod_products","objectID":"6e2de810-983f-4102-a60d-e4d6bb9b83bd"},{"indexName":"prod_products","objectID":"e1c6156e-264b-4d97-9820-6554bbd63c52"},{"indexName":"prod_products","objectID":"a8aa82b7-52ae-4cd6-88c3-bfbc178ae658"},{"indexName":"prod_products","objectID":"f5e7e53d-218d-43f8-8d46-3716210722a7"},{"indexName":"prod_products","objectID":"24313715-94f3-4071-9bbe-9f4f5980e0c5"},{"indexName":"prod_products","objectID":"1febd14c-4464-4285-90fc-72bafb6eeee7"},{"indexName":"prod_products","objectID":"623590cd-2ba0-43bc-97ca-43dcd6349598"}]
       }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
         #"Content-Type": "application/json"
    }

    def parse(self,response):
        yield scrapy.FormRequest(
                url=self.url,
                method='POST',
                headers=self.headers,
                body=json.dumps(self.formdata),
                callback=self.parse_page,
            )

    def parse_page(self, response):
        data = json.loads(response.text)
        for i in data['results']:
           #features = {
           #       'Category' : i['category']['name'],
           #       'Name' : i['name']
           #}
           print(i)


if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()

    #ResidentialSale.parse(ResidentialSale, '')

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import csv
import os

class Linkedin():
    def getData(self):
        file = 'data.csv'
        try:
          if(os.path.exists(file) and os.path.isfile(file)):
             os.remove(file)
             print('file deleted')
          else:      
             print('file not found')
        except OSError:
           pass   
    
        driver = webdriver.Chrome('/home/danish-khan/scrapers/researchgate/chromedriver')
        driver.get('https://www.linkedin.com/login')
        driver.find_element_by_id('username').send_keys('danishkhankd237@gmail.com') #Enter username of linkedin account here
        driver.find_element_by_id('password').send_keys('dankhanish446')  #Enter Password of linkedin account here
        driver.find_element_by_xpath("//button[@type='submit']").click()

        #*********** Search Result ***************#
        search_key = "data analyst" # Enter your Search key here to find people
        key = search_key.split()
        keyword = ""
        for key1 in key:
            keyword = keyword + str(key1).capitalize() +"%20"
        keyword = keyword.rstrip("%20")
            
        global data
        data = []

        for no in range(1,30):
            start = "&page={}".format(no) 
            search_url = "https://www.linkedin.com/search/results/people/?keywords={}&origin=SUGGESTION{}".format(keyword,start)
            driver.get(search_url)
            driver.maximize_window()
            for scroll in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            search = Selector(text = driver.page_source)
            profiles = search.xpath('//span[@class="entity-result__title-text  t-16"]/a/@href').getall()
            print(profiles)
            print('\nprofiles:',profiles)            
            count = 0
            print("Going to scrape Page {} data".format(no))
            
            for people in profiles:
                    count+=1

                #if count%2==0:

                    driver.get(people)
                    print('\nggg', people)
                    
                    time.sleep(2)
                    
                    # #********** Profile Details **************#
                    
                    page = Selector(text = driver.page_source)
                
                    details = {
                       'Name' : '',
                       'Education' : '',
                       'Email' : ''
                    }
                     
                    try:
                        Name = page.xpath('//h1[@class="text-heading-xlarge inline t-24 v-align-middle break-words"]/text()').get()
                        
                    except:
                        Name = "None"
                    
                    try:
                        Education = page.xpath('//h3[@class="pv-entity__school-name t-16 t-black t-bold"]/text()').get()
                    except:
                        Education = 'None'
                    
                    details['Name'] = Name
                    details['Education'] = Education    
                    
                    

                    #*******  Contact Information **********#
                    time.sleep(2)
                    people = people.split('?')[0]
                    driver.get(people + '/detail/contact-info/')

                    info = Selector(text = driver.page_source)
                    
                    try:
                        linkedin_link = info.xpath('//a[@class = "pv-contact-info__contact-link link-without-visited-state t-14"]/@href').get()
                    except:
                        linkedin_link = 'None'
                   
                    details['Email'] = linkedin_link
                    print(details)
                    
                    with open('data.csv','a') as f:
                      writer = csv.DictWriter(f, fieldnames = details.keys())
                      writer.writerow(details)
                      
                    
                       
        driver.quit()
    
            
    def start(self):
        self.getData()
        
if __name__ == "__main__":
    obJH = Linkedin()
    obJH.start()

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from tkinter import *

class Linkedin():
    def getData(self):
        driver = webdriver.Chrome('/home/danish-khan/scrapers/researchgate/chromedriver')
        driver.get('https://www.linkedin.com/login')
        driver.find_element_by_id('username').send_keys('danishkhankd237@gmail.com') #Enter username of linkedin account here
        driver.find_element_by_id('password').send_keys('dankhanish446')  #Enter Password of linkedin account here
        driver.find_element_by_xpath("//button[@type='submit']").click()

        #*********** Search Result ***************#
        search_key = "data analyst" # Enter your Search key here to find people
        key = search_key.split()
        print('\nkeyword:', key)
        keyword = ""
        for key1 in key:
            keyword = keyword + str(key1).capitalize() +"%20"
        keyword = keyword.rstrip("%20")
        print('\nkeyword2 :', keyword) 
           
        #global data
        data = []
        profile_links = [] 
         
        for no in range(1,3):
            start = "&page={}".format(no) 
            search_url = "https://www.linkedin.com/search/results/people/?keywords={}&origin=SUGGESTION{}".format(keyword,start)
            driver.get(search_url)
#            driver.maximize_window()
            for scroll in range(2):
                  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                  time.sleep(2)
                  links = driver.find_elements_by_xpath('//span[@class="entity-result__title-text  t-16"]/a[@class= "app-aware-link"]')
                
                
                  links = [link.get_attribute('href') for link in links]
                  print('\nlinks:',links)
                
                  profile_links.append(links)
                  print("Going to scrape Page {} data".format(no))
                
                  print('\nprofile_links :', profile_links)
                  lent = 0 
                  for people in profile_links:                     
                      time.sleep(2)
                      driver.get(people)
                      print('\n\npeoples',people)
                      print('\ngetting\n')
                      # #********** Profile Details **************#
                      card = BeautifulSoup(driver.page_source,'lxml')
                      
                      try:
                        Name = card.find('h1', attrs = {'class' : 'text-heading-xlarge inline t-24 v-align-middle break-words'}).text 
                      except:
                        Name = 'None'

                      details = {
                        'Name' :  'hgf', #card.find('h1', attrs = {'class' : 'text-heading-xlarge inline t-24 v-align-middle break-words'}).text,
                        'Location' : '',
                        'Work_at' : '',
                        'Education' : '',
                        'Profile_image' : '',
                        'Website' : '',
                        'Email' : ''
                      }
                      details['Name'] = Name
                      print(details)


                      time.sleep(2)               
                      driver.close()
                
        driver.close()
 
    def start(self):
        self.getData()
 
if __name__ == "__main__":
    obJH = Linkedin()
    obJH.start()

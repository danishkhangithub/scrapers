from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import csv
import os
import wget



login_url = 'https://www.instagram.com/'
base_url = ""
chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'
names = []
chrome_options = Options()
#chrome_options.add_argument('--headless')

webdriver = webdriver.Chrome(
  executable_path=chrome_driver_path, options=chrome_options
)

# default login credential and search query
username = 'danishkhan11'
password = 'danishinstra3.1'
search_query = "Islamia college Peshawar"
results = []

with webdriver as driver:
    # Set timeout time 
    wait = WebDriverWait(driver, 10)

    # retrive url in headless browser
    driver.get(login_url)
    
    # find search box
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
   
    
    username.clear()
    username.send_keys("danishkhankd11")
    password.clear()
    password.send_keys("danishinstra3.1")
    
    # target button
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    
    time.sleep(5)
    alert = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()  
  
    alert2 = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
  
    #driver.get(base_url)
    time.sleep(5)
    
    searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    searchbox.clear()
  
    keyword = "#cat"
    searchbox.send_keys(keyword)
  
    time.sleep(5)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(5)
    
    searchbox.send_keys(Keys.ENTER)
    time.sleep(5)
    
    #scroll down to scrape more images
    driver.execute_script("window.scrollTo(0, 4000);")
    #target all images on the page
    images = driver.find_elements_by_tag_name('img')
    images = [image.get_attribute('src') for image in images]
    images = images[:-2]
    #print('Number of scraped images: ', len(images))
    

    
    path = os.getcwd()
    path = os.path.join(path, keyword[1:] + "s")
        
    #create the directory
    #os.mkdir(path)
    
    counter = 0
    for image in images:
        save_as = os.path.join(path, keyword[1:] + '_' + str(counter))
        wget.download(image, save_as)
        counter +=1
    
    # must close the driver after task finished
    driver.close()

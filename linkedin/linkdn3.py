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
from bs4 import BeautifulSoup


login_url = 'https://www.linkedin.com/checkpoint/rm/sign-in-another-account?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
base_url = ""
chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'
names = []
chrome_options = Options()
#chrome_options.add_argument('--headless')

webdriver = webdriver.Chrome(
  executable_path=chrome_driver_path, options=chrome_options
)

# default login credential and search query
username = 'danishkhankd237@gmail.com'
password = 'dankhanish446'

results = []

with webdriver as driver:
    # Set timeout time 
    wait = WebDriverWait(driver, 10)

    # retrive url in headless browser
    driver.get(login_url)
    
    # find search box
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='session_key']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='session_password']")))
   
    
    username.clear()
    username.send_keys("danishkhankd237@gmail.com")
    password.clear()
    password.send_keys("dankhanish446")
    
    # target button
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    
    time.sleep(5)
    
    searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    searchbox.clear()
    for page in range(7,8):
        base_url = 'https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22101022442%22%5D?keywords=web%20scraping&network=%5B%22F%22%5D&origin=FACETED_SEARCH' + '&page=' + str(page)
        
        driver.get(base_url)
        time.sleep(2)
        
        
#        page = BeautifulSoup(driver.page_source, 'html-parser')
#        page = page.find_all('button', attr = {'class' : '.artdeco-button--secondary'})
#        print(page)
        
        all_buttons = driver.find_elements_by_xpath('//div/button[@class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]')

        #message_buttons = [btn.get_attribute('href') for btn in all_buttons]
        print('\nhh',all_buttons)
        
        
        
        
        time.sleep(2)
        
        
        
    driver.close()

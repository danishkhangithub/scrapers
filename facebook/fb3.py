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



login_url = 'https://web.facebook.com/?stype=lo&jlou=Afe15k5Nm19xKSd_Kw31qahd6Go7Y0CA-8eEVdkIpM9sXrlHWpch4l4BnB7bzEwnaU6vwBJIqzTGYAkCMoXgNYF9GLXu8zUr5aNlT0iSPZThPw&smuh=5576&lh=Ac8eegEPR8H_XISu8-E'
base_url = "https://web.facebook.com/jaleesahmad.qureshi"
chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'
names = []
chrome_options = Options()
chrome_options.add_argument('--headless')

webdriver = webdriver.Chrome(
  executable_path=chrome_driver_path, options=chrome_options
)

# default login credential and search query
username = 'danishkhansf@gmail.com'
password = 'danishkhan785'
search_query = "Islamia college Peshawar"
results = []

with webdriver as driver:
    # Set timeout time 
    wait = WebDriverWait(driver, 10)

    # retrive url in headless browser
    driver.get(login_url)
    
    # find search box
    driver.find_element_by_id("email").send_keys(username)
    driver.find_element_by_id("pass").send_keys(password)
    driver.find_element_by_name("login").click()
    #driver.find_element_by_id("u_0_h_gr").click()
    
    time.sleep(2)
    driver.get(base_url)
    time.sleep(5)
    selector = ''
    names = driver.find_element_by_xpath('//h1[@class="gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl bp9cbjyn j83agx80"]')
    location = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div/div/ul/div[6]/div[2]/div/div/span/a/div/span')
    #location = WebDriverWait(driver, 10).until(
    #     EC.presence_of_all_elements_located((By.XPATH, location))
    #     ) 
   
    print(names.text)
    print(location.text)    
    
    
    driver.close()

#!/usr/bin/env python
# coding: utf-8

import json
from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import time
import xlsxwriter


driver = webdriver.Chrome('/home/danish-khan/scrapers/researchgate/chromedriver')
page= "pageid"   #Enter your page id here
url = 'https://www.instagram.com/{}/'.format(page)
driver.get(url)
driver.maximize_window()
for scroll in range(20):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

page = BeautifulSoup(driver.page_source, 'lxml')
script = page.findAll('script')[8]
print('\nghgh',script)
page_json = script.text.split(' = ', 1)[1].rstrip(';')
data = json.loads(page_json)
#profile = {}
# # ############## Profile Data ###############
#page_data = data['entry_data']['ProfilePage'][0]
#user_details = page_data['graphql']['user']
#followers = user_details['edge_followed_by']['count']
#following = user_details['edge_follow']['count']
#full_name = user_details['full_name']
#bio = user_details['biography']
#Website = user_details['external_url']
#user_id = user_details['id']
#username = user_details['username']
#profile_pic = user_details['profile_pic_url']
#profile_pic_hd = user_details['profile_pic_url_hd'] 
#business_prifile = user_details['is_business_account']
#business_name = user_details['business_category_name']
#private_profile = user_details['is_private']
#verified_profile = user_details['is_verified']
#fb_page = user_details['connected_fb_page']
#insta_channel = user_details['has_channel']
#no_of_posts = user_details['edge_owner_to_timeline_media']['count']
#print("!!!!!!!!Profile details scrapped!!!!!!!")
#
#profile.update({"username":username})
#profile.update({"full_name":full_name})
#profile.update({"followers":followers})
#profile.update({"following":following})
#profile.update({"no_of_posts":no_of_posts})
#profile.update({"profile_pic":profile_pic})
#profile.update({"profile_pic_hd":profile_pic_hd})
#profile.update({"bio":bio})
#profile.update({"Website":Website})
#print("**"*40)
#profile.update({"business_prifile":business_prifile})
#profile.update({"business_name":business_name})
#profile.update({"private_profile":private_profile})
#profile.update({"verified_profile":verified_profile})
#profile.update({"fb_page":fb_page})
#profile.update({"insta_channel":insta_channel})
#
# # ########### POSTS DETAILS ###############
#
#post_data = page.findAll('div', attrs ={'class':'_bz0w'})
#post_details = []
#counting = 0
#for post_link in post_data:
#    posts = {}
#    post_links = post_link.find('a')
#    post_links = post_links['href']
#    post_links = "https://www.instagram.com" + str(post_links)
#     post_urls.append(post_links)
#
#    posts.update({"post_links":post_links})
#    driver.get(post_links)
#    soup = BeautifulSoup(driver.page_source, 'lxml')
#    try:
#        author = soup.find('a', attrs = {'class':'FPmhX notranslate nJAzx'}).text
#    except:
#        author = ''
#    posts.update({"author":author})
#    try:
#        location = soup.find('a', attrs = {'class':'O4GlU'}).text
#    except:
#        location = ''
#    posts.update({"location":location})
#    try:
#        text = soup.find('div', attrs = {'class':'C7I1f X7jCj'}).findAll('span')[0].text
#    except:
#        text = ''
#    try:
#        tags = soup.find('div', attrs = {'class':'C7I1f X7jCj'}).findAll('span')[0].findAll('a').text
#    except:
#        tags = ''
#    caption = text + tags
#   
#    posts.update({"caption":caption})
#    
#    post_media = soup.find('div', attrs = {'class':'ZyFrc'})
#    try:
#        media = post_media.find('video')['src']
#        posts.update({"media_type":'Video'})
#    except:
#        media = post_media.find('div', attrs = {'class': 'KL4Bh'}).find('img')['src']
#        posts.update({"media_type":"Image"})
#    posts.update({"media":media})
#    counting+=1
#    
#    post_details.append(posts)
#print("{} posts scrapped ".format(counting))
#

driver.quit()
    








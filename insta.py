import logging
import threading
import time
import sys
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

homepage = 'https://www.instagram.com/accounts/login/'
LOG_USER_USERNAME = "//input[@class='_2hvTZ pexuQ zyHYP']"
LOG_USER_SIGN_IN = "//button[@class='_0mzm- sqdOP  L3NKy       ']"
LOG_USER_NOT_NOW = "//button[@class='aOOlW   HoLwm ']"
TARGET_FOLOWERS = "//a[@class='-nal3 ']"
TARGET_FOLLOWERS_PEOPLE = "//div[@class='PZuss']"
FOLLOWER_INFO = '/html/body/span/section/main/div/header'
AWAIT_PRESENCE = 15



USERNAME = 'XXXXXXX'
PASSWORD = 'XXXXXXX'
TARGET	 = 'XXXXXXX'
 

  # Logs user on the site
def logUser(usernameStr ,passwordStr,driver):
    print ('Logging user in...')

    driver.get(homepage)

    # Fill in username and password
    try:
        WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.XPATH, LOG_USER_USERNAME)))

        creds = driver.find_elements_by_xpath(LOG_USER_USERNAME)
        username_input = creds[0]
        password_input = creds[1]

        username_input.send_keys(usernameStr)
        password_input.send_keys(passwordStr)

    except TimeoutException:
        print('Username/Password field could not be located!')
        return

     # Hit sign in button
    try:
        password_input.send_keys(Keys.RETURN)
    except:
        print('Sign in button could not be located!')
        return

    time.sleep(3)
# Go to target and view his followers stories
def extractFollowers(driver,target):
    print ('Parsing followers...')
    
    driver.get('https://www.instagram.com/' + target)
    time.sleep(2)
    try: # Go to targets Folowers
        followers_btn = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.XPATH, TARGET_FOLOWERS)))
        followers_btn.click() # Click followers
    except TimeoutException:
        print('Unable to navigate to followers!')
        return
    time.sleep(5)

    follower_window = driver.find_element_by_xpath("//div[@class='PZuss']")

    idx = 0
    followers_file = open('ricci-folowers.txt' ,'w+')
    followers_found = []
    while True:
        print('*Scroll number : ' , idx)
        idx += 1
        if idx % 10 == 1 : time.sleep(10)

         # Try to scroll down
        try:
            lastElement = follower_window.find_elements(By.TAG_NAME ,'li')[-1]

            driver.execute_script("arguments[0].scrollIntoView();", lastElement )
        except:
            time.sleep(0.3)
            all_elements = len(follower_window.find_elements(By.TAG_NAME ,'li'))
            if all_elements >20000 : break
    
        
        time.sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html,features='lxml')

        followers = soup.findAll("div", {"class": 'enpQJ'})
        print ('EXTRACTED A TOTAL OF '  + str(len(followers)) + 'FOLLOWERS')

        
        for follower in followers:
            try:
                name = follower.find('a').text
    
                if name not in followers_found:
                    followers_found.append(name)
                    print (name)
                    followers_file.write(name + '\n')
            except:
                print('Couldnt find/append followers name into list')

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
dirpath = os.getcwd() # Path for current directory
chrdriver_path = dirpath + '/chromedriver'

options = webdriver.ChromeOptions()

options.set_headless(True)
options.add_argument("--headless")
options.add_argument("--disable-gpu")
"""
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
"""
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("user-agent=[Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36]")
driver = webdriver.Chrome(executable_path = chrdriver_path,chrome_options=options)








logUser(USERNAME,PASSWORD,driver)

followers = extractFollowers(driver,TARGET)
driver.get('https://www.instagram.com/')

"""
f = open('names.csv','w')
f.write("Follower_Name \n")

for name in followers:

    f.write(name + '\n') 



try:
    names = open ('names.csv' , 'r')
    follower_list = open ('followers.csv' , 'w+')
    follower_list.write('Follower_Name , Profile_URL , Numof_Posts , Followers , Following , Bio \n')
    for name in names:
        
        url = name
        driver.get(url)
        
        dude_postnumber             = '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span'
        dude_follownumber_private   = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span'
        dude_follownumber_public    = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/span/span'
        dude_follows_private        = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/span/span'
        dude_follows_public         = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span'
        dude_desc                   = '//*[@id="react-root"]/section/main/div/header/section/div[2]'

        dd = WebDriverWait(driver, AWAIT_PRESENCE).until(EC.presence_of_element_located((By.XPATH, dude_postnumber)))

        postnum = driver.find_element_by_xpath(dude_postnumber)

        #TODO ADD VISIBILITY COLUMN1
        try:
            follownum = driver.find_element_by_xpath(dude_follownumber_public)
        except:
            follownum = driver.find_element_by_xpath(dude_follownumber_private)
            print ('He priv')


        try:
            follows = driver.find_element_by_xpath(dude_follows_public)
        except:
            follows = driver.find_element_by_xpath(dude_follows_private)
            print ('He priv')


        bio = driver.find_element_by_xpath(dude_desc)

        print ('==========================')
        print (name.rstrip())
        print ('Number of posts ' + str(postnum.text))
        print ('Number of follows ' + str(follownum.text))
        print ('Number following ' + str(follows.text))    
        namew   = (name).rstrip()
        postnw  = str(postnum.text).rstrip()
        folerw  = str(follownum.text).rstrip()
        folinw  = str(follows.text).rstrip()
        dbionw  = (bio.text.encode("utf-8"))
        dbionw = dbionw.replace('\n','')
        dbionw = dbionw.replace('\t','')
        url     = url.rstrip()

        
        line = namew + ',' + url + ',' + postnw + ',' + folerw + ',' + folinw + ',' + dbionw + '\n'
        follower_list.write(line)


    names.close()
    follower_list.close()
except:
    print ('watafak man')
    driver.quit()
"""

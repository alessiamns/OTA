#!/usr/bin/env python
# coding: utf-8

# In[1]:


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import time
import re
import requests
import urllib.request
import urllib.parse


# In[2]:


driver = webdriver.Chrome('chromedriver.exe')
chrome_options = Options()
driver.get("http://www.tripadvisor.it")
hotels = driver.find_element_by_xpath("//a[@href= '/Hotels']")

actions = ActionChains(driver)
actions.click(hotels) 
actions.send_keys("noto")
actions.perform()
time.sleep(3)
actions.send_keys(Keys.ENTER).perform()

url = driver.current_url
print (url)


# In[60]:


def calendar():
    buttonarrive = driver.find_element_by_xpath("//button[contains(@class, 'button__green')]").click()
    calendnext = driver.find_element_by_xpath("//button[contains(@class, 'calendar__next')]").click() #clicca sulla freccia avanti nel calendario
    calendarweek = driver.find_elements_by_xpath("//div[contains(@class, 'calendar__day-')]") #settimane del calendario
    for i in range(0,(len(calendarweek))):
        calendarweek[i].click()
        time.sleep(1)
        ad = driver.find_elements_by_xpath("//button[contains(@class, 'number-ticker__control')][1]")
        for i in range(0,(len(ad))):
            ad[1].click() 
            time.sleep(2)
            aggiorna = driver.find_element_by_xpath("//button[text()='Aggiorna']").click() #clicca su aggiorna per aggiornare la lista
            time.sleep(5)
            listnames()
            listprices()
            cambiopag()


# In[39]:


def listnames():
    hotelnames = driver.find_elements_by_xpath("//*[@class='listing_title']") #nomi hotel
    structuretype = driver.find_elements_by_xpath("//span[@class='label']")
    infostructure = driver.find_elements_by_xpath("//div[@class='info-col']")
    nonestructure = ("non specificato")
    for i in range(0,(len(hotelnames))):
        #links = driver.find_element_by_link_text(hotelnames[i].text).get_attribute('href')
        print(hotelnames[i].text) #nome struttura
        #print(links)
    for i in range(0,(len(structuretype))):
        print (structuretype[i].text)  #tipologia di struttura


# In[40]:


def listprices():
    hotelprice = driver.find_elements_by_xpath("//*[@class='price-wrap ']/div[position()=last()]") #prezzi
    notes = driver.find_elements_by_xpath("//*[@class='note']") #div delle strutture senza prezzi
    noprice = 0
    textnumber = ""

    if (len(hotelprice)>0):
        for i in range(0,(len(hotelprice))):
            textnumber = hotelprice[i].text
            number = textnumber.strip(" &nbsp;€")
            print(number)
            #separare numero da euro e stampare solo numero(intero) 
            
    elif (len(notes)>0) :
        for i in range(0,(len(notes))):
            print (noprice)


# In[41]:


def cambiopag():
    num_pages = driver.find_elements_by_xpath("//div[@class='pageNumbers']/a")
    last = len(num_pages)-1
    count = int(num_pages[last].get_attribute("data-page-number"))
    for i in range(0,(count-1)):
        page = driver.find_element_by_xpath("//a[@class='nav next taLnk ui_button primary']")
        listnames()
        listprices()
        page.click()
        time.sleep(10)
        
        
cambiopag()        
#calendar()


# In[ ]:





# In[ ]:





import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import time
import re
import mysql.connector
from mysql.connector import Error
import argparse
import sys

options = Options()
options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)


driver.get("http://www.tripadvisor.it/Hotels")
driver.maximize_window()

parser = argparse.ArgumentParser(description='Where to?')

parser.add_argument('-place', type=str, required=True, help='enter with the city name')

args = parser.parse_args()

ahead_input = driver.find_element_by_class_name("typeahead_input").click()

time.sleep(1)

input_search = driver.find_element_by_class_name("typeahead_input")
input_search.send_keys(args.place)
time.sleep(4)
research = driver.find_element_by_xpath("//button[@id='SUBMIT_HOTELS']").click()

time.sleep(3)

#close calendar
view_calendar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "_1HphCM4i")))
element = driver.find_element_by_class_name("_1HphCM4i")
driver.execute_script("arguments[0].style.position = 'initial';", element)


time.sleep(3)




#tabella servizi
def amenities():
    hotel_name = driver.find_element_by_xpath("//h1[contains(@class, 'hotel-review')]").text
    try:
        view_plus = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ssr-init-26f']/*[2]/following-sibling::*[1]")))
        plus = driver.find_element_by_xpath("//div[@class='ssr-init-26f']/*[2]/following-sibling::*[1]").click()
        #gestione servizi in una finestra
        active_amenities = driver.find_elements_by_xpath("//div[contains(@class, 'activeGroup')]//div[contains(@class,'amenity--3fbBj')]")
        time.sleep(3)
        for i in range(0,(len(active_amenities))):
            time.sleep(3)
            amenity_hotel = active_amenities[i].text
            
            insert_table = "INSERT INTO amenities (Name, Amenity) VALUES (%s, %s)"
            records_to_insert = [(hotel_name, amenity_hotel)]
            cursor.executemany(insert_table, records_to_insert)
        close_window = driver.find_element_by_xpath("//div[@role='button']").click()
        
    except:
        active_amenities = driver.find_elements_by_xpath("//div[contains(@class, 'AmenityGroup')][1]//div[contains(@class, 'Amenity')]")
        for i in range(0,(len(active_amenities))):
            amenity_hotel = active_amenities[i].text
    
            insert_table = "INSERT INTO amenities (Name, Amenity) VALUES (%s, %s)"
            records_to_insert = [(hotel_name, amenity_hotel)]
            cursor.executemany(insert_table, records_to_insert)
    #soluzione per eliminare le stringhe vuote dalla tabella: effettuare una query
    cursor.execute("DELETE FROM amenities WHERE Amenity = ''")
    connection.commit()
    print(cursor.rowcount, "Record in amenities")




#connessione al db
try:
        
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="ota"
            )
    cursor = connection.cursor()
    
    cursor.execute("CREATE TABLE amenities (Name VARCHAR(64), Amenity VARCHAR(64)) ")    
    
    
    homepage = driver.window_handles[0]  
    #view_urls = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-clicksource='HotelName']")))
    urls = driver.find_elements_by_xpath("//a[@data-clicksource='HotelName']") #url 
    for i in range(0,(len(urls))):
        urls[i].click()
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        time.sleep(3)
        amenities()
        time.sleep(3)
        driver.close()
        driver.switch_to.window(homepage)
        time.sleep(5)
        
    
except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


#window_before = driver.window_handles[0]
#driver.switch_to.window(window_before)



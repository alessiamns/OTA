import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import time
import re
import configparser
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import argparse
import sys

start = time.time()

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
options.add_argument('headless')
options.add_argument('--lang=it')

driver = webdriver.Chrome(options=options)

config = configparser.ConfigParser()
config_zars = config.read('config.ini')
if not config_zars:
    exit('no config.ini')
else:
    host_zars = config['zarsDB']['host']
    user_zars = config['zarsDB']['user']
    time_zars = config['waiting time']['set_time']
    seconds = int(time_zars)

if not host_zars or not user_zars or not time_zars:
    exit('parametri file config.ini non definiti')

#get url
driver.get("http://www.tripadvisor.it/Hotels")
driver.maximize_window()

parser = argparse.ArgumentParser()
parser.add_argument('-place', type=str, required=True, help='search destination')
parser.add_argument('-pages', type=int, help='enter number pages')
args = parser.parse_args()
ahead_input = driver.find_element_by_class_name("typeahead_input").click()
time.sleep(seconds)
input_search = driver.find_element_by_class_name("typeahead_input")
input_search.send_keys(args.place)
time.sleep(seconds)
research = driver.find_element_by_xpath("//button[@id='SUBMIT_HOTELS']").click()
time.sleep(seconds)

#close calendar
calendar = driver.find_element_by_class_name("_1HphCM4i")
driver.execute_script("arguments[0].style.position = 'initial';", calendar)
time.sleep(seconds)

#function amenities
def amenities():
    hotel_name = driver.find_element_by_xpath("//h1[contains(@class, 'hotel-review')]").text
    city = str(args.place)
    try:
        plus = driver.find_element_by_xpath("//div[@class='ssr-init-26f']/*[2]/following-sibling::*[1]/div")
        time.sleep(seconds)
        plus.click()
        #gestione servizi in una finestra
        active_amenities = driver.find_elements_by_xpath("//div[contains(@class, 'activeGroup')]//div[contains(@class,'amenity--3fbBj')]")
        time.sleep(seconds)
        for i in range(0,(len(active_amenities))):
            time.sleep(seconds)
            amenity_hotel = active_amenities[i].text
            insert_table = "INSERT INTO amenities (Name, City, Amenity) VALUES (%s, %s,  %s)"
            records_to_insert = [(hotel_name, city, amenity_hotel)]
            cursor.executemany(insert_table, records_to_insert)
        close_window = driver.find_element_by_xpath("//div[@role='button']")
        close_window.click()
    except:
        active_amenities = driver.find_elements_by_xpath("//div[contains(@class, 'AmenityGroup')][1]//div[contains(@class, 'Amenity')]")
        for i in range(0,(len(active_amenities))):
            amenity_hotel = active_amenities[i].text
            insert_table = "INSERT INTO amenities (Name, City, Amenity) VALUES (%s, %s, %s)"
            records_to_insert = [(hotel_name, city, amenity_hotel)]
            cursor.executemany(insert_table, records_to_insert)
    #delete empty strings
    cursor.execute("DELETE FROM amenities WHERE Amenity = ''")
    connection.commit()
    print(cursor.rowcount, "record in Amenities")

connection = mysql.connector.connect(
        host=host_zars,
        user=user_zars
        )
cursor = connection.cursor()

#connection
try:    
    db = "zars"
    def create_db(cursor):
        try:
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db))
        except mysql.connector.Error as error:
            print("Failed creating database: {}".format(error))
            exit(1)

    try:
        cursor.execute("USE {}".format(db))
    except mysql.connector.Error as error:
        print("Database {} does not exists.".format(db))
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            create_db(cursor)
            print("Database {} created successfully.".format(db))
            connection.database = db
        else:
            print(error)
            exit(1)
    
    
    cursor.execute("CREATE TABLE IF NOT EXISTS amenities (Name VARCHAR(64) NOT NULL, City VARCHAR(64) NOT NULL, Amenity VARCHAR(64)) ")    
    
    #manage page
    number_pages = driver.find_element_by_xpath("//a[contains(@class, 'pageNum')][position() = last()]").text
    pages = int(number_pages)  #conversion

    if args.pages:
        pages = args.pages

    for j in range(0,pages):
        homepage = driver.window_handles[0]  
        time.sleep(seconds)
        urls = driver.find_elements_by_xpath("//a[@data-clicksource='HotelName']") #url 
        driver.find_element_by_xpath("//div[@class='h1-container']").click()
        time.sleep(seconds)
        if j < (pages-1):
            go_on = driver.find_element_by_xpath("//a[contains(text(),'Avanti')]") #button
            time.sleep(seconds)
            for i in range(0,(len(urls))):
                try:
                    ads = driver.find_element_by_tag_name("iframe")
                    driver.switch_to.frame(ads)
                    time.sleep(seconds)
                    driver.switch_to.default_content()
                    urls[i].click()
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    time.sleep(seconds)
                    amenities() #call the function defined
                    time.sleep(seconds)
                    driver.close()
                    driver.switch_to.window(homepage)
                    time.sleep(seconds)
                except:
                    urls[i].click()
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    time.sleep(seconds)
                    amenities() #call the function defined
                    time.sleep(seconds)
                    driver.close()
                    driver.switch_to.window(homepage)
                    time.sleep(seconds)
            go_on.click()
            time.sleep(seconds)  
        else:
            for i in range(0,(len(urls))):
                try:
                    ads = driver.find_element_by_tag_name("iframe")
                    driver.switch_to.frame(ads)
                    time.sleep(seconds)
                    driver.switch_to.default_content()
                    urls[i].click()
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    time.sleep(seconds)
                    amenities() #call the function defined
                    time.sleep(seconds)
                    driver.close()
                    driver.switch_to.window(homepage)
                    time.sleep(seconds)
                except:
                    urls[i].click()
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    time.sleep(seconds)
                    amenities() #call the function defined
                    time.sleep(seconds)
                    driver.close()
                    driver.switch_to.window(homepage)
                    time.sleep(seconds)
    cursor.execute("SET foreign_key_checks = 0")
    cursor.execute("ALTER TABLE amenities ADD FOREIGN KEY(Name, City) REFERENCES info(Name, City)")
    cursor.execute("SET foreign_key_checks = 1")
    driver.quit()            
    
except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


end = time.time()
#test time
print(end - start)

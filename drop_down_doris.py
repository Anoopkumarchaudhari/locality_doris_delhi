import  pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import  Keys
import time
from twocaptcha import TwoCaptcha
import os

#====================================== Data Base Connectivity ======================================================================
import mysql.connector
conn = mysql.connector.connect(host="localhost", user="atm_user", password="1234", database='anoop',
                              auth_plugin="mysql_native_password")
if conn.is_connected():
    print(' Connection Stablished succesfuuly ... ')
def insert(id1, area):
    try:
        mycursor = conn.cursor()
        mycursor.execute("insert into delhi_locality values(%s,%s)",
                         (id1, area))
        conn.commit()
        print(f'{id1} : {area}')
        print(' ------- SUCCESSFULLY -------')
        id1 += 1
        # return id1
    except Exception as e:
        print(f'{id} : {area} ')
        print(e)
        print('----------------------------------------------')
        # return id1
#===================================================================================================================================



start = time.time()

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

s = Service("D:/PROGRAMMING/Advance_webScraping/chromedriver-win64/chromedriver-win64/chromedriver.exe")
# driver = webdriver.Chrome(service=s, options=options)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://esearch.delhigovt.nic.in/SearchByName1.aspx")
time.sleep(1)
driver.execute_script('window.scrollBy(0,430)')
time.sleep(1)


locality = ''
A_LOC = []
def two_space(text):
    for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        driver.get("https://esearch.delhigovt.nic.in/SearchByName1.aspx")
        time.sleep(1)
        driver.execute_script('window.scrollBy(0,430)')
        time.sleep(1)

        temp = text + char
        element = driver.find_element(by=By.XPATH,value='//*[@id="ctl00_ContentPlaceHolder1_txtSearch"]')
        for c in temp:
            element.send_keys(c)
            time.sleep(0.005)

        # click first party / Second Party
        driver.find_element(by=By.XPATH,value='//*[@id="ctl00_ContentPlaceHolder1_rdbuttun"]/tbody/tr/td[2]/span/label').click()
        time.sleep(0.5)
        driver.execute_script('window.scrollBy(0,430)')
        time.sleep(2)
        locality = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_txtSearch"]').get_attribute("value")

        time.sleep(0.5)
        if temp != locality:
            mycursor = conn.cursor()
            mycursor.execute('select count(*) from anoop.delhi_locality')
            last_id= mycursor.fetchone()
            A_LOC.append(locality)
            print('----'*10)
            print(locality)


def three_space(text):
    for char1 in 'OPQRSTUVWXYZ':
        driver.get("https://esearch.delhigovt.nic.in/SearchByName1.aspx")
        time.sleep(1)
        driver.execute_script('window.scrollBy(0,430)')
        time.sleep(1)

        temp = text + char1

        element = driver.find_element(by=By.XPATH, value='//*[@id="ctl00_ContentPlaceHolder1_txtSearch"]')
        for c in temp:
            element.send_keys(c)
            time.sleep(0.005)

        # click first party / Second Party
        driver.find_element(by=By.XPATH,
                            value='//*[@id="ctl00_ContentPlaceHolder1_rdbuttun"]/tbody/tr/td[2]/span/label').click()
        time.sleep(0.5)
        driver.execute_script('window.scrollBy(0,430)')
        time.sleep(2)
        locality = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_txtSearch"]').get_attribute(
            "value")

        time.sleep(0.5)
        if temp != locality:
            mycursor = conn.cursor()
            mycursor.execute('select count(*) from anoop.delhi_locality')
            all1 = mycursor.fetchone()
            id1 = all1[0] + 1
            insert(id1, locality)

        for char2 in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            driver.get("https://esearch.delhigovt.nic.in/SearchByName1.aspx")
            time.sleep(1)
            driver.execute_script('window.scrollBy(0,430)')
            time.sleep(1)

            temp = text + char1 + char2

            element = driver.find_element(by=By.XPATH, value='//*[@id="ctl00_ContentPlaceHolder1_txtSearch"]')
            for c in temp:
                element.send_keys(c)
                time.sleep(0.005)

            # click first party / Second Party
            driver.find_element(by=By.XPATH,
                                value='//*[@id="ctl00_ContentPlaceHolder1_rdbuttun"]/tbody/tr/td[2]/span/label').click()
            time.sleep(0.5)
            driver.execute_script('window.scrollBy(0,430)')
            time.sleep(2)
            locality = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_txtSearch"]').get_attribute("value")

            time.sleep(0.5)
            if temp != locality:
                mycursor = conn.cursor()
                mycursor.execute('select count(*) from anoop.delhi_locality')
                all1 = mycursor.fetchone()
                id1 = all1[0] + 1
                insert(id1,locality)


text = 'B'
# two_space(text)
three_space(text)
end = time.time()
print('time (s) : ',round(end-start))
print('time (m) : ',round(((end-start)/60),2))
print('len :',len(A_LOC))
print(A_LOC)
# BI






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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from twocaptcha import TwoCaptcha
import os

start = time.time()


options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

s = Service("D:/PROGRAMMING/Advance_webScraping/chromedriver-win64/chromedriver-win64/chromedriver.exe")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

df = pd.read_csv('all_sro_locality_for_b_raj.csv')
name= []
print('--------------- connect successful ---------------')
alpha = input('enter alphabet : ')
for i in df['locality']:
    if i.startswith(alpha):
        name.append(i)


all_html = ""
i = 0

import threading
from selenium.webdriver.common.by import By



# start timer (kill after 8 sec)
count = 1
while i < len(name):
    #search Engine
  try:
    driver.get("https://esearch.delhigovt.nic.in/SearchByName1.aspx")
    time.sleep(2)

    # use for Scrolling
    driver.execute_script('window.scrollBy(0,430)')
    time.sleep(1)

    # Locality search
    driver.find_element(by=By.XPATH,value='//*[@id="ctl00_ContentPlaceHolder1_txtSearch"]').send_keys(name[i].strip())
    time.sleep(1)


    # random click
    driver.find_element(by=By.XPATH,value='//*[@id="aspnetForm"]/div[7]/div[2]/div[2]/div[2]/div[2]/div[1]').click()
    time.sleep(2)
    driver.execute_script('window.scrollBy(0,430)')
    time.sleep(1)

    # click first party / Second Party
    driver.find_element(by=By.XPATH,value='//*[@id="ctl00_ContentPlaceHolder1_rdbuttun"]/tbody/tr/td[2]/span/label').click()
    time.sleep(2)
    driver.execute_script('window.scrollBy(0,430)')
    time.sleep(1)

    # click first party / Second Party ( repeate because of refreshment )
    driver.find_element(by=By.XPATH,value='//*[@id="ctl00_ContentPlaceHolder1_rdbuttun"]/tbody/tr/td[2]/span/label').click()
    time.sleep(2)
    driver.execute_script('window.scrollBy(0,430)')
    time.sleep(1)

    # input in select party
    party = 'baldev raj bhola'
    element = driver.find_element(by=By.XPATH,value='//*[@id="ctl00_ContentPlaceHolder1_txt_Second_sbnm"]')
    for ch in party:
        element.send_keys(ch)
        time.sleep(0.005)
    time.sleep(1)


    # screenshot of capcha
    captcha_img = driver.find_element(by=By.XPATH, value='//*[@id="ctl00_ContentPlaceHolder1_UpdatePanel4"]/div/img')
    time.sleep(1)
    captcha_img.screenshot('captchas/captcha.png')
    time.sleep(1)

    # Api of twocapcha for text extraction

    api_key = os.getenv('APIKEY_2CAPTCHA', 'dbf65fa75150663607b9be3a2e7b1475')

    solver = TwoCaptcha(api_key)

    try:
        result = solver.normal('captchas/captcha.png')

    except Exception as e:
        print(e)

    else:
        code = result['code']
        time.sleep(1)
        # driver.find_element(by=By.XPATH, value='//*[@id="ctl00_ContentPlaceHolder1_txtcaptchsbynm"]').send_keys(code)
        element = driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_txtcaptchsbynm"]')
        for ch in code:
            element.send_keys(ch)
            time.sleep(0.005)
        time.sleep(1)
        # driver.find_element(by=By.XPATH, value='//*[@id="ctl00_ContentPlaceHolder1_btn_searchbyname"]').click()
        WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_btn_searchbyname"]'))
        ).click()
        time.sleep(1)
        all_html += driver.page_source + "\n\n<!-- PAGE BREAK -->\n\n"
        time.sleep(1)
        print('-'*30)
        print(f'{i} : {name[i]}  ,  api capcha :{code}')
        print('='*50)

  except Exception as e:
      print('=' * 30)
      print(i, ' : ', name[i],' ,  Error : Please Enter Valid locality ')
      print('-'*50)
      # print(e)
      time.sleep(1)
  i = i+1
  count += 1
  if count == 15:
      count = 1
      time.sleep(5)
# all_html = ""
# for i in range(4):
#     driver.execute_script('window.scrollBy(0,430)')
#     time.sleep(2)
#     all_html += driver.page_source + "\n\n<!-- PAGE BREAK -->\n\n"
#     # driver.find_element(by=By.XPATH,value='//*[@id="ctl00_ContentPlaceHolder1_GridView1_ctl07_btn_next"]').click()
#     driver.find_element(By.XPATH, '//*[contains(@name, "GridView1") and contains(@name, "btn_next")]').click()
#     time.sleep(3)


end = time.time()
html = driver.page_source
with open(f'{alpha}_baldev_raj_bhola_2.html','w',encoding='utf-8') as f:
    f.write(all_html)

print('time(in second) : ',round((end-start),2))
print('time in minute : ', round((round(end-start)/60),2))
time.sleep(8)
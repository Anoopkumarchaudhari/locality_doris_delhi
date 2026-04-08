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

driver.get("https://esearch.delhigovt.nic.in/Complete_search_without_regyear.aspx")
time.sleep(0.5)
driver.execute_script('window.scrollBy(0,660)')
time.sleep(2)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

data = []

wait = WebDriverWait(driver, 10)

# total SRO count
sro_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddl_sro_s"))
sro_count = len(sro_dropdown.options)
driver.execute_script('window.scrollBy(0,660)')

for i in range(1, sro_count):  # skip "--Select SRO--"

    # re-fetch SRO dropdown (IMPORTANT after reload)
    sro_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddl_sro_s"))
    sro_option = sro_dropdown.options[i]
    driver.execute_script('window.scrollBy(0,660)')
    sro_name = sro_option.text.strip()
    print(f"\nProcessing SRO: {sro_name}")

    # select SRO
    sro_dropdown.select_by_index(i)

    # wait for Locality dropdown to load
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ddl_loc_s"]')))
    driver.execute_script('window.scrollBy(0,660)')
    # get locality dropdown
    locality_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ddl_loc_s"]'))
    driver.execute_script('window.scrollBy(0,660)')
    locality_options = locality_dropdown.options

    for j in range(1, len(locality_options)):  # skip "--Select Locality--"

        locality_name = locality_options[j].text.strip()

        print(f"   -> {locality_name}")

        # store data
        data.append((sro_name, locality_name))

# ✅ Convert to DataFrame
df = pd.DataFrame(data, columns=["SRO Name", "Locality"])

# ✅ Save
df.to_csv("sro_locality.csv", index=False)

print("\n✅ Done! Data saved.")


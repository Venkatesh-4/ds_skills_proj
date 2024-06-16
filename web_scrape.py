# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
import time
import pandas as pd
import os

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

url1 = 'https://www.linkedin.com/jobs/search/?currentJobId=3883384532&distance=25&f_E=2&f_JT=F&f_TPR=r2592000&geoId=105214831&keywords=Data%20Science&location=Bengaluru'

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)
driver.get(url1)

driver.find_element(By.LINK_TEXT, "Sign in").click()
driver.find_element(By.ID, "username").send_keys("venkeyp6@gmail.com")
driver.find_element(By.ID, "password").send_keys("Vaup12#4%")
driver.find_element(By.CSS_SELECTOR, ".btn__primary--large").click()


job_list = driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container').click()
print(job_list)

deets= driver.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__job-insight job-details-jobs-unified-top-card__job-insight--highlight').text
print(deets)







    
    
   
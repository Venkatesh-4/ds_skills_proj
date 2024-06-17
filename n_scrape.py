#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 14:31:52 2024

@author: daz
"""

import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv
import logging
from dotenv import load_dotenv

def create_logfile():
    date_time = datetime.datetime.today().strftime('%d-%b-%y_%H:%M:%S')
    logfile = f"log/{date_time}.log"
    logging.basicConfig(filename=logfile, filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', force=True)
    logging.info(f'Log file {logfile} created')
    return logging

def create_file(file, logging):
    # delete existing file if re-running
    logging.info("Checking if current daily csv exists...")
    if os.path.exists(file):
        os.remove(file)
        logging.info(f"{file} deleted")
    else:
        logging.info(f"{file} ain't exist")
    
    # create file and add header
    logging.info("Creating daily csv file...")
    header = ['date_time', 'search_count', 'job_id', 'job_title', 'company', 'location', 'update_time', 'applicants', 'job_time', 'job_level', 'job_type', 'company_size', 'company_industry', 'job_details']
    with open(file, 'w') as f:
        w = csv.writer(f)
        w.writerow(header)
        logging.info(f"{file} created")

def login(logging):
    url_login = "https://www.linkedin.com/jobs/search/?currentJobId=3912090685&distance=25&f_E=2&f_JT=F&f_TPR=r2592000&f_WT=1&geoId=105214831&keywords=Data%20Science&location=Bengaluru&origin=JOB_SEARCH_PAGE_JOB_FILTER"

    # pulls login information from file called '.env' 
    # this file added to .gitignore so login details not shared
    load_dotenv()
    # .env file is of structure:
    # LINKEDIN_USERNAME=email@gmail.com
    # LINKEDIN_PASSWORD=password

    LINKEDIN_USERNAME = os.getenv('LINKEDIN_USERNAME')
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')

    # # setup chrome to run headless
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1920,1080")

    # login to LinkedIn
    logging.info(f"Logging in to LinkedIn as {LINKEDIN_USERNAME}...")
    wd = webdriver.Chrome()
    wd.maximize_window()
    wd.get(url_login)
    
    wd.find_element(By.LINK_TEXT, "Sign in").click()
    wd.find_element(By.ID, "username").send_keys("alpharomeooo68@gmail.com")
    wd.find_element(By.ID, "password").send_keys("asdfghjklasdfgh@")
    wd.find_element(By.CSS_SELECTOR, ".btn__primary--large").click()

    # # random confirm acount information pop up that may come up
    # try: 
    #     wd.find_element(By.XPATH, "button[@class='primary-action-new']").click()
    # except:
    #     pass
    # logging.info("Log in complete. Scraping data...")

    return wd
#def page_search(wd, search_page, search_count, file, logging):

def page_search(wd, search_page, search_count, file, logging):
    # wait time for events in seconds
    page_wait = 30
    click_wait = 5
    async_wait = 5

    # when retrying, number of attempts
    attempts = 3
    url_search=f"https://www.linkedin.com/jobs/search/?currentJobId=3912090685&distance=25&f_E=2&f_JT=F&f_TPR=r2592000&f_WT=1&geoId=105214831&keywords=Data%20Science&location=Bengaluru&origin=JOB_SEARCH_PAGE_JOB_FILTER&start={search_page}"
    wd.get(url_search)

    # find the number of results 
    height = wd.execute_script("return document.body.scrollHeight")
    scroll_page(wd, height // 200)
    elem = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='jobs-search-results-list__subtitle'] span")))
    search_count = elem.text
    search_count = int(search_count.split()[0])
    print(search_count)
    logging.info(f"Loading page {round(search_page/25) + 1} of {round(search_count/25)} {search_count} results...")

    # get all the job_id's for xpath for current page to click each element
    # running into errors with slow load (11-Aug)
    for attempt in range(attempts):
        try:
            search_results = wd.find_element(By.XPATH,"//ul[@class='scaffold-layout__list-container']").find_elements(By.TAG_NAME, "li")
            result_ids = [result.get_attribute('id') for result in search_results if result.get_attribute('id') != '']
            print(result_ids)
            break
        except:
            time.sleep(click_wait) # wait a few attempts, if not throw an exception and then skip to next page

    # cycle through each job_ids and steal the job data...muhahaha!
    list_jobs = [] #initate a blank list to append each page to
    for id in result_ids:
        try:
            job = wd.find_element(By.ID, id) 
            # print(job)
            job_id = job.get_attribute("data-occludable-job-id").split(":")[-1]
            # print(job_id)
            # select a job and start extracting information
            wd.find_element(By.XPATH, f"//div[@data-job-id='{job_id}']").click()
        except:
            continue
            # exception likely to job deleteing need to go to next id

        for attempt in range(attempts):
            try:
                # from analysis 3 attempts at 5 second waits gets job titles 99.99% of time (11-Aug)
                job_title = wd.find_element(By.XPATH, "//h1[@class='t-24 t-bold inline']") # keep having issues with finding element
                job_title = job_title.text
                # print(job_title)
                break
            except:
                job_title = ''
                time.sleep(click_wait)
        
        # Having issues finding xpath of company (Added 11-Aug)
        for attempt in range(attempts):
            try:
                company = wd.find_element(By.XPATH, "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[1]/div/div/a").text
                location = wd.find_element(By.XPATH, "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[3]/div/span[1]").text
                update_time = wd.find_element(By.XPATH, "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[3]/div/span[3]").text
                applicants = wd.find_element(By.XPATH, "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[3]/div/span[5]").text
                # print(update_time)
                # print(applicants)
                # print(company)
                # print(location)
            
            except:
                company = ''
                location = ''
                update_time = '' # after #attempts leave as blank and move on
                applicants = '' # after #attempts leave as blank and move on
                time.sleep(click_wait)

        # Due to (slow) ASYNCHRONOUS updates, need wait times to get job_info
        job_type = '' # assigning as blanks as not important info and can skip if not obtained below
        job_time = ''
        job_level = ''
        
        for attempt in range(attempts):
            try:
                # 1 - make sure HTML element is loaded
                element = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/ul/li[1]")))
                # 2 - make sure text is loaded
                try:
                    job_info = element.text
                    if job_info != '':
                        # seperate job information on time requirements and position
                        job_info = job_info.split(" · ")
                        if (len(job_info) == 2):
                            job_time = job_info[0]
                            job_level = job_info[1]
                            job_type = ""
                        else: # else condition satisifies the last condition
                            job_type = job_info[0]
                            job_time = job_info[1]
                            job_level = job_info[2]
                        break
                    else:
                        time.sleep(async_wait)
                except:
                    # error means page didn't load so try again
                    time.sleep(async_wait)
            except:
                # error means page didn't load so try again
                time.sleep(async_wait)

        # get company details and seperate on size and industry
        company_size = '' # assigning as blanks as not important info and can skip if not obtained below
        company_industry = ''
        job_details = ''      
        for attempt in range(attempts):
            try:
                company_details = wd.find_element(By.XPATH, "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[4]/ul/li[2]").text
                wd.find_element(By.PARTIAL_LINK_TEXT, "Skills:").click()
                job_details = wd.find_element(By.XPATH, "//a[contains(@class,'job-details-how-you-match__skills-item-subtitle t-14 overflow-hidden')]").text
                print('jd', job_details)
                print(company_details)
                if " · " in company_details:
                    company_size = company_details.split(" · ")[0]
                    company_industry = company_details.split(" · ")[1]
                    # print('cs', company_size)
                    # print('ci', company_industry)
                    # print(job_details)
                else:
                    company_size = company_details
                    company_industry = ''
                
                break
            except:
                time.sleep(click_wait)

        # append (a) line to file
        date_time = datetime.datetime.now().strftime("%d%b%Y-%H:%M:%S")
        # search_keyword = search_keyword.replace("%20", " ")
        list_job = [date_time, search_count, job_id, job_title, company, location, update_time, applicants, job_time, job_level, job_type, company_size, company_industry, job_details]
        list_jobs.append(list_job)

    with open(file, "a") as f:
        w = csv.writer(f)
        w.writerows(list_jobs)
        list_jobs = []
    
    logging.info(f"Page {round(search_page/25) + 1} of {round(search_count/25)} loaded ")
    search_page += 25

    return search_page, search_count

def scroll_page(wd, height):
    for scroll in range(height):
        wd.execute_script("window.scrollTo(0, window.scrollY + 200)")
        time.sleep(0.1)
    
    
# create logging file
logging = create_logfile()

# create daily csv file
date = datetime.date.today().strftime('%d-%b-%y')
file = f"output/{date}.csv"
create_file(file, logging)

# login to linkedin and assign webdriver to variable
wd = login(logging)

# # URL search terms focusing on what type of skills are required for Data Analyst & Data Scientist
# search_keywords = ['Data Analyst', 'Data Scientist', 'Data Engineer']
#     # Titles to remove as search is too long
#     # ['Business Analyst', 'Operations Analyst', 'Marketing Analyst', 'Product Analyst',
#     # 'Analytics Consultant', 'Business Intelligence Analyst', 'Quantitative Analyst',  'Data Architect',
#     # 'Data Engineer', 'Machine Learning Engineer', 'Machine Learning Scientist']
# search_location = "United%20States"
# search_remote = "true" # filter for remote positions
# search_posted = "r86400" # filter for past 24 hours

# Counting Exceptions
exception_first = 0
exception_second = 0

# for search_keyword in search_keywords:
#     search_keyword = search_keyword.lower().replace(" ", "%20")

# Loop through each page and write results to csv
search_page = 0 # start on page 1
search_count = 1 # initiate search count until looks on page
while (search_page < search_count) and (search_page != 1000):
    # Search each page and return location after each completion
    try:
        search_page, search_count = page_search(wd, search_page, search_count, file, logging)
    except Exception as e:
        logging.error(f'(1) FIRST exception on {search_page} of {search_count}, retrying...')
        logging.error(e)
        logging.exception('Traceback ->')
        exception_first += 1
        time.sleep(5) 
        try:
            search_page, search_count= page_search(wd, search_page, search_count, file, logging)
            logging.warning(f'Solved Exception on {search_page} of {search_count}')
        except Exception as e:
            logging.error(f'(2) SECOND exception remains . Skipping to next page...')
            logging.error(e)
            logging.exception('Traceback ->')
            search_page += 25 # skip to next page to avoid entry
            exception_second += 1
            logging.error(f'Skipping to next page on {search_page} of {search_count}...')

wd.quit()


logging.info(f'LinkedIn data scraping complete with {exception_first} first and {exception_second} second exceptions')
logging.info(f'Regard all further alarms...')
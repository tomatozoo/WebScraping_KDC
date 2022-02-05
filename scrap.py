# -*- coding: utf-8 -*-

import json
import os
import re
import pickle
import time
import datetime
from queue import Full
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sys import platform
from tqdm import tqdm
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_opt = webdriver.ChromeOptions()

prefs = {"profile.managed_default_content_settings.images": 2}  # to unable image
chrome_opt.add_experimental_option("prefs", prefs)


print('Current OS : ', platform)
if 'darwin' in platform:
    selen_path = '/chromedriver/chromedriver.exe'
    chrome_opt.add_argument('--kiosk')

elif 'win32' in platform:
    selen_path = os.path.join(os.getcwd(), 'chromedriver', 'chromedriver.exe') 
    chrome_opt.add_argument('--start-maximized')
    chrome_opt.add_experimental_option('excludeSwitches', ['enable-logging'])


# main crawler 
def crawler_D1(keys):
    try:
        # firefox
        Result = {}

        # 로그인
        global driver
        driver.maximize_window()
        driver.get('https://nl.go.kr/')
        time.sleep(1)
        
        # 검색
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main_input-text"]')))
        element.send_keys(keys)
        
        search = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="comSchForm"]/div[1]/div[3]/button')))
        search.send_keys(Keys.ENTER)
        
        # 정보 추출
        author = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sub_content"]/div[1]/div/div[1]/div[3]/div/div/div[3]/div[2]/div[1]/div[2]/div[3]/span[4]')))
        
        company = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sub_content"]/div[1]/div/div[1]/div[3]/div/div/div[3]/div[2]/div[1]/div[2]/div[3]/span[5]')))
        
        year = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sub_content"]/div[1]/div/div[1]/div[3]/div/div/div[3]/div[2]/div[1]/div[2]/div[3]/span[6]')))
        
        sname = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sub_content"]/div[1]/div/div[1]/div[3]/div/div/div[3]/div[2]/div[1]/div[2]/div[3]/span[8]')))
        sname = sname.split(':')[1]
        
        return [keys, author.text, company.text, year.text, sname.text]
        
        # //*[@id="divSeoji"]/div[1]/p[7]/a[2]
    except:
        pass


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=selen_path,
                              chrome_options=chrome_opt)
    result = pd.DataFrame(columns=['도서명', '저자', '출판사','출판년도','청구기호'])
    df = pd.read_excel('2018 교육학과 도서목록 정리 통합본(1130).xlsx', sheet_name='단순통합')
    df = df['도서명']
    for i in df:
    
        print(i)
        i = i.split(':')[0]
        i = i.split('(')[0]
        i = i.split('[')[0]
        RS1 = crawler_D1(i)
        result.append(RS1)
        
    df.to_excel('초안.xlsx')
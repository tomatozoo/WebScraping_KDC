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
    print(keys)
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
        print(author.text)
        
        company = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sub_content"]/div[1]/div/div[1]/div[3]/div/div/div[3]/div[2]/div[1]/div[2]/div[3]/span[5]')))
        print(company.text) 
        
        year = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sub_content"]/div[1]/div/div[1]/div[3]/div/div/div[3]/div[2]/div[1]/div[2]/div[3]/span[6]')))
        print(year.text) 
        
        sname = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sub_content"]/div[1]/div/div[1]/div[3]/div/div/div[3]/div[2]/div[1]/div[2]/div[3]/span[8]')))
        sname = sname.split(':')[1]
        print(sname.text)     
    except:
        pass


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=selen_path,
                              chrome_options=chrome_opt)
    
    for i in ['TED처럼 말하라 : 세계 최고 프레젠테이션의 25가지 비밀','마음의 작동법 : 무엇이 당신을 움직이는가','일의 미래 : 10년 후, 나는 어디서 누구와 어떤 일을 하고 있을까','마음의 사회학','권력이동','사회적 자본과 민주주의: 이탈리아의 지방자치와 시민적 전통','사회주의 재발명','살라미나의 병사들 : 하비에르 세르카스 장편소설','미국의 송어낚시']:
        RS1 = crawler_D1(i)
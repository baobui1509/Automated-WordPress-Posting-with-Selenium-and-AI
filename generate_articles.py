from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException, NoSuchElementException
import time
from selenium.webdriver.common.action_chains import ActionChains
import csv
from datetime import datetime
import pytz
import uuid
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.model_selection import train_test_split
from difflib import SequenceMatcher
import threading
import subprocess
import sys
import os
from webdriver_manager.chrome import ChromeDriverManager

gemini_API_key = 'AIzaSyC5SA3F6-ylQ155KMPI1r7uUNsE91VyDGg'


username = 'buithienbaoo2@gmail.com'
password = 'Utcung 1509@'

google_results_number = 3
excel_start = 1
excel_end = 3

def get_prompts(keyword, google_result_urls):
    prompts = [
        f'Truy cập vào link [{google_result_urls[0]}] để lấy những thông tin quan trọng của cá nhân đang được nhắc đến. Liệt kê những thông tin đó.',
        f'Tiếp tục truy cập link [{google_result_urls[1]} để lấy thêm thông tin chưa có. Viết thành 1 bài văn biểu cảm về nhân vật được nhắc đến.]',
        f'Sửa lại cách dùng từ, từ ngữ sao cho biểu cảm hơn',
        f'Hoàn thiện bài văn trên sao cho không giống với bài viết của 1 AI'
    ]
    return prompts

def get_keywords(path):
    with open(path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file] if excel_end != 0 else [line.strip() for line in file][excel_start - 1:excel_end - 1]

def openChromeDriver(google_url, chatGPT_url):
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(google_url)
    time.sleep(5)
    driver.execute_script(f"window.open('{chatGPT_url}', '_blank');")
    return driver

# def openChromeDriver(google_url, chatGPT_url):
#     options = Options()
    
#     # Loại bỏ logging của Chrome
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
#     # Các tùy chọn để cải thiện hiệu suất
#     options.add_argument("start-maximized")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
    
#     # Đường dẫn tới profile Chrome của bạn
#     profile_path = "/Users/baobui1509/Library/Application Support/Google/Chrome"  # Thay thế đường dẫn chính xác
#     options.add_argument(f"user-data-dir={profile_path}")  # Đường dẫn thư mục profile
#     options.add_argument("profile-directory=Default")  # Chỉ định profile sử dụng (Default hoặc Profile 1)

#     # Thêm remote debugging để tránh lỗi khởi động
#     options.add_argument("--remote-debugging-port=9222")

#     # Khởi tạo ChromeDriver
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
    
#     # Truy cập Google và mở ChatGPT
#     driver.get(google_url)
    
#     # Đợi trang Google tải
#     time.sleep(5)  # Có thể thay thế bằng WebDriverWait
    
#     # Mở ChatGPT trong tab mới
#     driver.execute_script(f"window.open('{chatGPT_url}', '_blank');")
    
#     return driver

def click_captcha_google(driver):
    try:
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
        checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#recaptcha-anchor")))
        checkbox.click()
        driver.switch_to.default_content()
        print('PASS CAPTCHA GOOGLE!')
    except Exception:
        print('NO CAPTCHA')

def get_google_result_urls(driver, keyword):
    google_result_urls = []
    tabs = driver.window_handles
    driver.switch_to.window(tabs[0])
    time.sleep(1)  
    textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#APjFqb")))
    textarea.clear()
    textarea.send_keys(keyword)
    textarea.send_keys(Keys.ENTER)
    click_captcha_google(driver)

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MjjYud")))
    articles = driver.find_elements(By.CSS_SELECTOR, ".MjjYud:not(:has(.Wt5Tfe))")
    for article in articles:
        try:
            link = article.find_element(By.CSS_SELECTOR, 'a[jsname="UWckNb"]').get_attribute("href")
            if len(google_result_urls) >= google_results_number:
                break
            print(link)
            print('----------------------------------------------------------------------------')
            google_result_urls.append(link)
        except Exception:
            pass
    return google_result_urls

def get_article(driver, keyword, google_result_urls):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])
    prompts = get_prompts(keyword, google_result_urls)
    for prompt in prompts:
        textarea = driver.find_element(By.CSS_SELECTOR, "#prompt-textarea")
        textarea.clear()
        textarea.send_keys(prompt)
        textarea.send_keys(Keys.ENTER)
        time.sleep(5)

if __name__ == '__main__':
    keywords = get_keywords('keywords.csv')
    google_url = 'https://www.google.com/'
    chatGPT_url = 'https://chatgpt.com/'
    driver = openChromeDriver(google_url, chatGPT_url)
    time.sleep(1)
    for keyword in keywords:
        google_result_urls = get_google_result_urls(driver, keyword)
        get_article(driver, keyword, google_result_urls)
    time.sleep(100000000)

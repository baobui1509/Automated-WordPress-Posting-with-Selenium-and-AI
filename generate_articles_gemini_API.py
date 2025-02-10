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
import google.generativeai as genai
import json
import re
import platform
import concurrent.futures



gemini_API_key = 'AIzaSyC5SA3F6-ylQ155KMPI1r7uUNsE91VyDGg'
SAVE_FILE_PATH = "saved_content.json"

with open(SAVE_FILE_PATH, "r", encoding="utf-8") as f:
        content = json.load(f)
        category = content.get("category", "")
        image_number = content.get("image", 0)
        google_results_number = content.get("number", 1)
        prompt1 = content.get("prompt1", "")
        prompt2 = content.get("prompt2", "")
        prompt3 = content.get("prompt3", "")
        prompt4 = content.get("prompt4", "")
        get_image = content.get("get_image")
        publish = content.get("publish")
        

genai.configure(api_key=gemini_API_key)
MAX_THREADS = 2
excel_start = 1
excel_end = 3
keywords = []
current_keyword = ''
prompts = []
USERNAME = "admin1"
PASSWORD = "11111111"

def switch_tab(driver, number):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[number])

def insert_image_h2(driver):
    try:
        h2_tags = driver.find_elements(By.CSS_SELECTOR, "h2")
        h2_tags = [h2 for h2 in h2_tags if "Intro" not in h2.text]
        if (len(h2_tags) == 0):
            return
        smaller_number = min(len(h2_tags), image_number)
        h2_tags = h2_tags[:smaller_number]
        # index = 0
        for tag in h2_tags:
            h2_text = tag.text
            switch_tab(driver, 2)
            textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#APjFqb")))
            textarea.clear()
            textarea.send_keys(h2_text)
            textarea.send_keys(Keys.ENTER)
            time.sleep(1)
            img_src = driver.find_element(By.CSS_SELECTOR, '[jscontroller="XW992c"] img.YQ4gaf').get_attribute("src")
            # html = f'<figure class="wp-block-image size-large"><img src="{img_src}" alt=""/></figure>'
            # html = f'<figure tabindex="0" class="block-editor-block-list__block wp-block size-full wp-block-image" id="block-ffc33aa0-e396-4a11-854e-f7049ca23f57" role="document" aria-label="Block: Image" data-block="ffc33aa0-e396-4a11-854e-f7049ca23f57" data-type="core/image" data-title="Image"><div class="components-resizable-box__container" style="position: relative; user-select: auto; display: block; width: auto; height: auto; max-width: 1450px; max-height: 966.667px; min-width: 30px; min-height: 20px; box-sizing: border-box; flex-shrink: 0;"><img src="{img_src}" alt="This image has an empty alt attribute; its file name is 19.jpg"><div><div class="components-resizable-box__handle components-resizable-box__side-handle components-resizable-box__handle-right" style="position: absolute; user-select: none; cursor: col-resize;"></div><div class="components-resizable-box__handle components-resizable-box__side-handle components-resizable-box__handle-bottom" style="position: absolute; user-select: none; cursor: row-resize;"></div></div></div><div class="components-drop-zone" data-is-drop-zone="true"></div></figure>'
            
            html =f'<figure class="wp-block-image size-large is-resized"><img src="{img_src}" alt="" style="width: 745px; height: auto; display: block; margin: auto;"/> </figure>'
            switch_tab(driver, 1)
            driver.execute_script("""
                var range = document.createRange();
                var sel = window.getSelection();
                var h2 = arguments[0];
                range.selectNodeContents(h2);
                range.collapse(false);
                sel.removeAllRanges();
                sel.addRange(range);
            """, tag)
            tag.send_keys(Keys.ENTER)
            add_button = driver.find_element(By.CSS_SELECTOR, ".components-button.editor-document-tools__inserter-toggle.is-primary.has-icon")
            add_button.click() 
            print("CLICK add_button")
            time.sleep(0.5)
            image_button = driver.find_element(By.CSS_SELECTOR, ".components-button.block-editor-block-types-list__item.editor-block-list-item-image")
            image_button.click() 
            print("CLICK image_button")

            time.sleep(1)
            more_button = driver.find_element(By.CSS_SELECTOR, ".components-dropdown.components-dropdown-menu.block-editor-block-settings-menu")
            more_button.click() 
            print("CLICK more_button")

            time.sleep(1)
            edit_html_button = driver.find_elements(By.CSS_SELECTOR, ".components-button.components-menu-item__button")[11] 
            edit_html_button.click() 
            print("CLICK edit_html_button")

            time.sleep(0.5) 
            textarea = driver.find_element(By.CLASS_NAME, "block-editor-block-list__block-html-textarea")
            textarea.clear()
            textarea.click()
            if platform.system() == "Darwin":  # macOS
                textarea.send_keys(Keys.COMMAND + "a")
            else:  # Windows/Linux
                textarea.send_keys(Keys.CONTROL + "a")
            textarea.send_keys(Keys.DELETE)
            textarea.send_keys(html)
            print("SEND KEYS")
    except Exception as e:
        print(f'Error in Insert_image:\n', {e})
        driver.get("https://www.i-inc-usa.com/wp-admin/post-new.php")




def add_new_post(driver, post):
    try:
        switch_tab(driver, 1)
        categories = driver.find_elements(By.CSS_SELECTOR, ".components-flex.components-h-stack.css-1et9n8m.e19lxcc00")
        for element in categories:
            print('element.text: ', element.text)
            if element.text == category:
                box = element.find_element(By.CSS_SELECTOR, ".components-checkbox-control__label")
                driver.execute_script("arguments[0].click();", box)
                break
        # # Tìm title
        # title_match = re.search(r"Meta Title:\n(.+)", post)
        # title = title_match.group(1).strip() if title_match else ""

        # # Loại bỏ title và description để lấy phần nội dung còn lại
        # content_start = re.search(r"Meta Description:\n(.+?)\n\n", post, re.DOTALL)
        # if content_start:
        #     content = post[content_start.end():].strip()
        # else:``
        #     content = post
        # Tìm Meta Title
        title_match = re.search(r"## Meta Title:\s*(.+)", post)
        title = title_match.group(1).strip() if title_match else ""

        # Loại bỏ Meta Title và Meta Description để lấy nội dung còn lại
        content_start = re.search(r"## Meta Description:\s*(.+?)\n\n", post, re.DOTALL)
        if content_start:
            content = post[content_start.end():].strip()
        else:
            content = post
        title_area = driver.find_element(By.CSS_SELECTOR, "#editor > div.editor-editor-interface.edit-post-layout.is-mode-visual.has-metaboxes.interface-interface-skeleton.has-footer > div.interface-interface-skeleton__editor > div.interface-interface-skeleton__body > div.interface-navigable-region.interface-interface-skeleton__content > div.editor-visual-editor.edit-post-visual-editor > div > div:nth-child(1) > div.editor-styles-wrapper.block-editor-writing-flow > div.editor-visual-editor__post-title-wrapper.edit-post-visual-editor__post-title-wrapper > h1")
        title_area.send_keys(title)
        content_area = driver.find_element(By.CSS_SELECTOR, "#editor > div.editor-editor-interface.edit-post-layout.is-mode-visual.has-metaboxes.interface-interface-skeleton.has-footer > div.interface-interface-skeleton__editor > div.interface-interface-skeleton__body > div.interface-navigable-region.interface-interface-skeleton__content > div.editor-visual-editor.edit-post-visual-editor > div > div:nth-child(1) > div.editor-styles-wrapper.block-editor-writing-flow > div.is-root-container.is-desktop-preview.is-layout-flow.wp-block-post-content.block-editor-block-list__layout > div > div > p")
        content_area.send_keys(content)
        if (get_image):
            insert_image_h2(driver)
        if (publish):
            publish_button = driver.find_element(By.CSS_SELECTOR, "#editor > div.editor-editor-interface.edit-post-layout.is-mode-visual.has-metaboxes.interface-interface-skeleton.has-footer > div.interface-interface-skeleton__editor > div.interface-navigable-region.interface-interface-skeleton__header > div > div.editor-header__settings > button.components-button.editor-post-publish-panel__toggle.editor-post-publish-button__button.is-primary.is-compact")
            publish_button.click()
            time.sleep(1)
            confirm = driver.find_element(By.CSS_SELECTOR, "#editor > div.editor-editor-interface.edit-post-layout.is-mode-visual.has-metaboxes.interface-interface-skeleton.has-footer > div.interface-interface-skeleton__editor > div.interface-interface-skeleton__body > div.interface-navigable-region.interface-interface-skeleton__actions > div:nth-child(2) > div > div > div.editor-post-publish-panel__header > div.editor-post-publish-panel__header-publish-button > button")
            confirm.click()
            time.sleep(1)
            driver.get("https://www.i-inc-usa.com/wp-admin/post-new.php")
        else:
            save_draft = driver.find_element(By.CSS_SELECTOR, "#editor > div.editor-editor-interface.edit-post-layout.is-mode-visual.has-metaboxes.interface-interface-skeleton.has-footer > div.interface-interface-skeleton__editor > div.interface-navigable-region.interface-interface-skeleton__header > div > div.editor-header__settings > button.components-button.editor-post-save-draft.is-compact.is-tertiary")
            save_draft.click()
            time.sleep(1)
            driver.get("https://www.i-inc-usa.com/wp-admin/post-new.php")
    except Exception as e:
        print("ERROR IN add_new_post:\n", e)


def login_wordpress(driver):
    switch_tab(driver, 1)
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user_login")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#user_pass"))) 
    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#wp-submit"))) 
    login_button.click() 
    time.sleep(2) 
    posts = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#menu-posts > a > div.wp-menu-name"))) 
    posts.click()
    add_new_post = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#menu-posts > ul > li:nth-child(3) > a"))) 
    driver.execute_script("arguments[0].click();", add_new_post)

    
def get_prompts(keyword, google_result_urls):

    prompts = [
        prompt1.replace('$KEYWORD', keyword),
        prompt2.replace('$KEYWORD', keyword),
        prompt3.replace('$KEYWORD', keyword),
        prompt4.replace('$KEYWORD', keyword)
    ]
    updated_prompts = []
    for prompt in prompts:
        # Tìm kiếm tất cả các chuỗi '$URL' theo sau bởi một số (ví dụ: $URL1, $URL2)
        matches = re.findall(r'\$URL(\d)', prompt)  # Sử dụng regex để tìm số sau $URL

        for match in matches:
            url_number = int(match) - 1  # Chuyển đổi số từ chuỗi thành integer
            # Thay thế $URL số với google_result_urls[số]
            prompt = prompt.replace(f"$URL{match}", str(google_result_urls[url_number]))
        updated_prompts.append(prompt)
    # print('updated_prompts: ', updated_prompts)
    return updated_prompts

def get_keywords(path):
    with open(path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file] if excel_end != 0 else [line.strip() for line in file][excel_start - 1:excel_end - 1]

def openChromeDriver(google_url, wordpress_url):
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(google_url)
    driver.execute_script("window.open(arguments[0], '_blank');", wordpress_url)
    time.sleep(1)
    switch_tab(driver, 1)
    driver.execute_script("window.open(arguments[0], '_blank');", "https://www.google.com/search?sca_esv=aac09e88d3bc5d88&sxsrf=AHTn8zoplQL__lTeFEKEorwxP9P4zY5Mtw:1739011471698&q=car&udm=2&fbs=ABzOT_AfCikcO6SgGMxZXxAG9tmS8rx53CbgOCSVg3O9Xo5xAK_RXi3VFy8QcDJV9F46BNVgXPVSNLh3EC8UATXqoQIBSA6FFNIPLMxYHHFRyE7wcmKutmRnya8dFuXrMKlslaMSg0PSD-RHrzxr5jD2xk4gJqbKjg8cuQm7NyLR-ch9tdhKN8ZBfmspljZBXQB0nbaLomPI1io-dTHEkKhfDGCJW_9usXtO9NhVLan8usNbMVE7ayw&sa=X&ved=2ahUKEwjBr5_I8rOLAxVej68BHahUAMoQtKgLegQIGhAB&cshid=1739011499279199&biw=1728&bih=1080&dpr=2")
    time.sleep(1)
    switch_tab(driver, 2)
    login_wordpress(driver)
    return driver

def click_captcha_google(driver):
    try:
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
        checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#recaptcha-anchor")))
        checkbox.click()
        time.sleep(4)
        driver.switch_to.default_content()
        print('PASS CAPTCHA GOOGLE!')
    except Exception:
        print('NO CAPTCHA')

def get_google_result_urls(driver, keyword, google_results_number):
    try:
        switch_tab(driver, 0)
        google_result_urls = []
        time.sleep(1)  
        textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#APjFqb")))
        textarea.clear()
        textarea.send_keys(keyword)
        textarea.send_keys(Keys.ENTER)
        click_captcha_google(driver)
        time.sleep(1)

        # elements = driver.find_elements(By.CSS_SELECTOR,'.TzHB6b.j8lBAb.p7kDMc.cLjAic:not:has([jsname="N760b"]))')
        elements = driver.find_elements(By.CSS_SELECTOR, '[jscontroller="gOTY1"]')

        for element in elements:
            try:
                data_id = element.get_attribute("data-id")
                if len(google_result_urls) >= google_results_number:
                    break
                if data_id and "https://" in data_id:
                    url = re.findall(r"https://\S+", data_id)
                    print(url)
                    print('----------------------------------------------------------------------------')
                    google_result_urls.append(url)
            except Exception:
                pass

        # search_results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc a")

        # # Lấy URL của 3 kết quả đầu tiên
        # google_result_urls = [result.get_attribute("href") for result in search_results[:3]]
        # print('google_result_urls: ', google_result_urls)

        return google_result_urls
    except Exception as e:
        print("ERROR IN get_google_result_urls:\n", e)

def chat_with_gemini(user_input, conversation_history):
    context = "\n".join(conversation_history)
    prompt = f"{context}\nUser: {user_input}\nAI:"
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    conversation_history.append(f"User: {user_input}")
    conversation_history.append(f"AI: {response.text}")
    
    # print(response.text)
    with open('results.txt', "a", encoding="utf-8") as f:
        f.write('')
        f.write(response.text + "\n")
    return response.text

def get_article(driver, keyword, google_result_urls):
    try:
        prompts = get_prompts(keyword, google_result_urls)
        conversation_history = []
        k = 1
        response = ''
        for prompt in prompts:
            print(f'----------------------------------------------------------------------------PROMPT {k}------------------------------------------------------------------------------')
            with open('results.txt', "a", encoding="utf-8") as f:
                f.write(f'----------------------------------------------------------------------------PROMPT {k}------------------------------------------------------------------------------' + "\n")
            response = chat_with_gemini(prompt, conversation_history)
            time.sleep(1)
            k += 1
        print('post: ', response)
        return response
        # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        # print(conversation_history)
    except Exception as e:
        print("ERROR IN get_article:\n", e)

def process_keyword(driver, keyword):
    try:
        print("Processing keyword:", keyword)
        google_result_urls = get_google_result_urls(driver, keyword, google_results_number)
        print('len(google_result_urls):', len(google_result_urls))

        article = get_article(driver, keyword, google_result_urls)
        add_new_post(driver, article)
    except Exception as e:
        print(f"Error with keyword {keyword}: {e}")

def worker(driver, keywords):
    print("keywords in worker: ", keywords)
    for keyword in keywords:
        print()
        process_keyword(driver, keyword)
    driver.quit()

def main():
    google_url = 'https://www.google.com/'
    wordpress_url = 'https://www.i-inc-usa.com/wp-admin/'
    keyword_groups = [keywords[i::MAX_THREADS] for i in range(MAX_THREADS)]

    # Chạy đa luồng
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        drivers = [openChromeDriver(google_url, wordpress_url) for _ in range(MAX_THREADS)]
        executor.map(worker, drivers, keyword_groups)


    # for keyword in keywords:
    #     try:
    #         print("keyword:", keyword) 
    #         google_result_urls = get_google_result_urls(driver, keyword, google_results_number)
    #         print()
    #         print('len(google_result_urls): ', len(google_result_urls))

    #         article = get_article(driver, keyword, google_result_urls)
    #         add_new_post(driver, article)
    #     except Exception as e:
    #         print('ERROR IN MAIN:\n', e)
    # driver.quit()

# if __name__ == '__main__':
#     keywords = get_keywords('keywords.csv')
#     google_url = 'https://www.google.com/'
#     driver = openChromeDriver(google_url)
#     time.sleep(1)
#     for keyword in keywords:
#         google_result_urls = get_google_result_urls(driver, keyword)
#         get_article(driver, keyword, google_result_urls)
    
#     time.sleep(100000000)

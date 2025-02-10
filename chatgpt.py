import time
from bs4 import BeautifulSoup
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import random
import html
import re


gmail = 'timtruyentranh.com@gmail.com'
passw = '/9Ck2U8Ep6stRA8'

folder_save_folder = [
            r'C:\Users\Admin\AppData\Local\Google\Chrome\User Data\chrome_smodin01',
            #r'C:\Users\Admin\AppData\Local\Google\Chrome\User Data\chrome_smodin02', 
            #r'C:\Users\Admin\AppData\Local\Google\Chrome\User Data\chrome_smodin03',
            #r'C:\Users\Admin\AppData\Local\Google\Chrome\User Data\chrome_smodin04',
            #r'C:\Users\Admin\AppData\Local\Google\Chrome\User Data\chrome_smodin05'
        ]


def _remove_all_attrs(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all(True): 
        tag.attrs = {}
    return soup 

def _remove_all_attrs_except_href(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all(True): 
        if tag.name == 'a':  # Kiểm tra nếu là thẻ <a>
            continue  # Bỏ qua việc loại bỏ thuộc tính của thẻ <a>
        else:
            tag.attrs = {}
    return soup


#hàm replace chừa lại h2 đầu tiên

def replace_all_except_first_occurrence(text, search_str, replace_str):
    first_occurrence_index = text.find(search_str)  # Tìm chỉ mục của lần xuất hiện đầu tiên
    new_text = text.replace(search_str, replace_str)  # Thay thế tất cả các lần xuất hiện
    
    # Thay thế lại lần xuất hiện đầu tiên
    if first_occurrence_index >= 0:
        new_text = new_text[:first_occurrence_index] + search_str + new_text[first_occurrence_index + len(replace_str):]
    
    return new_text





# Lấy ouline
def automation_promt1(list_url, keyword, domain_name, brand_name, folder_save_folder):

    # Nhập dữ liệu mà không lấy
    try:
        chrome_options = uc.ChromeOptions()
        
        chrome_options.add_argument(f'--user-data-dir={random.choice(folder_save_folder)}')
        #chrome_options.add_argument("--max-connections=1")

        driver = uc.Chrome(driver_executable_path='chromedriver.exe', options=chrome_options)

        # driver = webdriver.Chrome(options=chrome_options)

        # Navigate to the link
        driver.get("https://chat.openai.com/chat")
        # driver.get("https://www.google.com/")
        driver.implicitly_wait(10)
        time.sleep(5)
        # đợi cho đến khi được nhập câu hỏi
        WebDriverWait(driver,60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="prompt-textarea"]')))
        time.sleep(1)
        res = driver.page_source
        soup = BeautifulSoup(res, "html.parser")
    except Exception as e:
        soup = ""
        print('Bước tạo chrome AI lỗi: %s' % e, '')


    if soup != "":

        print("Nhập promt 0")

        # Search query nhập câu hỏi
        try:
            time.sleep(2)
            tao_value = f'''
                - Browser Internet, Please, start by reading these links:                 
                {list_url}.
                '''
            # Xoá xuống dòng
            try:
                xoa_xuong_dong_script = " ".join([s for s in tao_value.splitlines()])
                xoa_xuong_dong_script = xoa_xuong_dong_script.replace('"', '')
                xoa_xuong_dong_script = xoa_xuong_dong_script.replace("'", "'")
            except Exception as e:
                print('Bước xoá xuống dòng lỗi: %s' % e, '')


            input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
            input_field.send_keys(f"""{xoa_xuong_dong_script}""")



            time.sleep(5)

            # nhấn click
            def skip_info2():
                actions2 = ActionChains(driver)
                actions2.send_keys(Keys.ENTER)
                actions2.perform()

            # Calling a function
            skip_info2()

            time.sleep(1)

        except Exception as e:
            print('Bước nhập câu hỏi lỗi nhập lại câu hỏi lần 2: %s' % e, '')


        # Đợi 150s
        try:
            time.sleep(5)
            buttons = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.justify-start:last-of-type button.rounded-lg:last-of-type')))

            # if buttons:
            #     # Chọn phần tử cuối cùng

            #     button_element = WebDriverWait(driver, 50).until(
            #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.justify-start:last-of-type button.rounded-lg:last-of-type')))

            time.sleep(10)

        except Exception as e:
            print('Bước đợi 150s lỗi, nhập lại lần 2: %s' % e, '')

        


        ############################################################################
        # Nhập promt 2
        # Search query nhập câu hỏi
        print("Nhập promt 1")
        try:
            time.sleep(2)
            tao_value = f'''
                List 20 latent semantic keywords associated, 20 EVA's (Entity, Attribute, Values), 20 ERE (Entity, Relation, Entity), 20 Semantic triple (Subject, Predicate, Object) with primary keyword: [{keyword}] from additional information and chatgpt. Search Intent: Develop content with the user's search intent in mind. Anticipate the keywords users might use when searching and address those in the article.
                '''
            # Xoá xuống dòng
            try:
                xoa_xuong_dong_script = " ".join([s for s in tao_value.splitlines()])
                xoa_xuong_dong_script = xoa_xuong_dong_script.replace('"', '')
                xoa_xuong_dong_script = xoa_xuong_dong_script.replace("'", "'")
            except Exception as e:
                print('Bước xoá xuống dòng lỗi: %s' % e, '')


            input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
            input_field.send_keys(f"""{xoa_xuong_dong_script}""")



            time.sleep(5)

            # nhấn click
            def skip_info2():
                actions2 = ActionChains(driver)
                actions2.send_keys(Keys.ENTER)
                actions2.perform()

            # Calling a function
            skip_info2()

            time.sleep(1)

        except Exception as e:
            print('Bước nhập câu hỏi lỗi nhập lại câu hỏi lần 2: %s' % e, '')


        try:
            time.sleep(5)
            buttons = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.justify-start:last-of-type button.rounded-lg:last-of-type')))

            # if buttons:
            #     button_element = WebDriverWait(driver, 50).until(
            #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.justify-start:last-of-type button.rounded-lg:last-of-type')))

            time.sleep(20)

        except Exception as e:
            print('Bước đợi 150s lỗi, nhập lại lần 2: %s' % e, '')



        ############################################################################
        print("Nhập promt 2")
        try:
            time.sleep(2)
            tao_value = f'''
                Based on the information above. I'm the assigned writer for {domain_name}, serving as the representative of the '{brand_name}' brand in the financial sector. My mission is to create informative and engaging content suitable for readers curious about famous people's finances. My goal is to provide readers with in-depth, up-to-date analysis of celebrities' latest net worth and the latest information surrounding their daily lives.

                Write an article like a human with a low amount of perplexity and a high amount of burstiness. Including all semantic keywords, all EVA, all ERE, all Semantic triple, adding linking words between sentences and paragraphs in this article is natural as well. Writing Style: Conversational. Tone: Informal. 100% SEO readability. 

                Search Intent: Develop content with the user's search intent in mind. Anticipate the keywords users might use when searching and address those in the article. With outline below, exclude conclusion:
                
                '{keyword} Quick Facts include Real Name, Popular Name, Gender, Date of birth, Age, Zodiac sign, Parents, Siblings, Birthplace, Nationality, Ethnicity, Education, Marital Status, Sexual Orientation, Wife/Spouse, Children, Dating, Net Worth, Source of Wealth, Height, Weight in pounds, Hair colour, Eye colour. (Table format with 2 columns FACT and DETAIL, Write N/A if there is no information).

                What is the Net Worth Of {keyword} in 2024? (100 words+, give the specific number data from net worth, compare with A, B, C)

                Full Overview and Wiki (500 words+) include sub-heading (please focusing on his career journey, which has increased his net worth over time)
                '''
            # Xoá xuống dòng
            try:
                xoa_xuong_dong_script = " ".join([s for s in tao_value.splitlines()])
                xoa_xuong_dong_script = xoa_xuong_dong_script.replace('"', '')
                xoa_xuong_dong_script = xoa_xuong_dong_script.replace("'", "'")
            except Exception as e:
                print('Bước xoá xuống dòng lỗi: %s' % e, '')


            input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
            input_field.send_keys(f"""{xoa_xuong_dong_script}""")



            time.sleep(5)

            # nhấn click
            def skip_info2():
                actions2 = ActionChains(driver)
                actions2.send_keys(Keys.ENTER)
                actions2.perform()

            # Calling a function
            skip_info2()

            time.sleep(1)

        except Exception as e:
            print('Bước nhập câu hỏi lỗi nhập lại câu hỏi lần 2: %s' % e, '')


        try:
            time.sleep(5)
            buttons = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.justify-start:last-of-type button.rounded-lg:last-of-type')))

            time.sleep(20)

        except Exception as e:
            print('Bước đợi 150s lỗi, nhập lại lần 2: %s' % e, '')


        # bước lấy câu trả lời
        try:
            res2 = driver.page_source
            soup2 = BeautifulSoup(res2, "html.parser")
            cau_tra_loi = soup2.find_all("div", class_="markdown")[-1]
            cau_tra_loi = html.unescape(str(cau_tra_loi))
            if cau_tra_loi == None:
                cau_tra_loi = ''
            cau_tra_loi = str(cau_tra_loi).replace('Title: ', '')
            cau_tra_loi = cau_tra_loi.replace('<button><svg><path></path><rect></rect></svg>Copy code</button>', '')
            cau_tra_loi = str(cau_tra_loi).replace('''<button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button>''', '')

            cau_tra_loi = cau_tra_loi.replace("h1", "h2")
            cau_tra_loi = _remove_all_attrs(str(cau_tra_loi))
            cau_tra_loi_content = str(cau_tra_loi)

            # print('cau_tra_loi_content', cau_tra_loi_content)

        except Exception as e:
            print('Bước lấy cau_tra_loi_content lỗi: %s' % e, '')
            cau_tra_loi_content = ''




        if len(cau_tra_loi_content) > 100:


            ############################################################################
            print("Nhập promt 3 lấy paa")
            try:
                time.sleep(2)
                tao_value = f'''
                    10 FAQs about {keyword}: 10 QA. Following the readers' search intent when they search {keyword} on Google. Write like a human with a low amount of perplexity and a high amount of burstiness. Writing Style: Conversational. Tone: Informal. 100% SEO readability.
                    '''
                # Xoá xuống dòng
                try:
                    xoa_xuong_dong_script = " ".join([s for s in tao_value.splitlines()])
                    xoa_xuong_dong_script = xoa_xuong_dong_script.replace('"', '')
                    xoa_xuong_dong_script = xoa_xuong_dong_script.replace("'", "'")
                except Exception as e:
                    print('Bước xoá xuống dòng lỗi: %s' % e, '')


                input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
                input_field.send_keys(f"""{xoa_xuong_dong_script}""")



                time.sleep(5)

                # nhấn click
                def skip_info2():
                    actions2 = ActionChains(driver)
                    actions2.send_keys(Keys.ENTER)
                    actions2.perform()

                # Calling a function
                skip_info2()

                time.sleep(1)

            except Exception as e:
                print('Bước nhập câu hỏi lỗi nhập lại câu hỏi lần 2: %s' % e, '')


            try:
                time.sleep(5)
                buttons = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.justify-start:last-of-type button.rounded-lg:last-of-type')))

                time.sleep(20)

            except Exception as e:
                print('Bước đợi 150s lỗi, nhập lại lần 2: %s' % e, '')


            # bước lấy câu trả lời
            try:
                res2 = driver.page_source
                soup2 = BeautifulSoup(res2, "html.parser")
                cau_tra_loi = soup2.find_all("div", class_="markdown")[-1]
                cau_tra_loi = html.unescape(str(cau_tra_loi))
                if cau_tra_loi == None:
                    cau_tra_loi = ''
                cau_tra_loi = str(cau_tra_loi).replace('Title: ', '')
                cau_tra_loi = cau_tra_loi.replace('<button><svg><path></path><rect></rect></svg>Copy code</button>', '')
                cau_tra_loi = str(cau_tra_loi).replace('''<button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button>''', '')

                cau_tra_loi = cau_tra_loi.replace("h1", "h2")
                cau_tra_loi = _remove_all_attrs(str(cau_tra_loi))
                cau_tra_loi_paa = str(cau_tra_loi)

                # print('cau_tra_loi_paa', cau_tra_loi_paa)

            except Exception as e:
                print('Bước lấy cau_tra_loi_paa lỗi: %s' % e, '')
                cau_tra_loi_paa = ''


            


            ############################################################################
            print("Nhập promt 4 lấy link social")
            try:
                time.sleep(2)
                tao_value = f'''
                    List all social media accounts of {keyword} including links by bullet points format. (give the latest number of followers)
                    '''
                # Xoá xuống dòng
                try:
                    xoa_xuong_dong_script = " ".join([s for s in tao_value.splitlines()])
                    xoa_xuong_dong_script = xoa_xuong_dong_script.replace('"', '')
                    xoa_xuong_dong_script = xoa_xuong_dong_script.replace("'", "'")
                except Exception as e:
                    print('Bước xoá xuống dòng lỗi: %s' % e, '')


                input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
                input_field.send_keys(f"""{xoa_xuong_dong_script}""")



                time.sleep(5)

                # nhấn click
                def skip_info2():
                    actions2 = ActionChains(driver)
                    actions2.send_keys(Keys.ENTER)
                    actions2.perform()

                # Calling a function
                skip_info2()

                time.sleep(1)

            except Exception as e:
                print('Bước nhập câu hỏi lỗi nhập lại câu hỏi lần 2: %s' % e, '')


            try:
                time.sleep(2)
                buttons = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.justify-start:last-of-type button.rounded-lg:last-of-type')))

                time.sleep(10)

            except Exception as e:
                print('Bước đợi 150s lỗi, nhập lại lần 2: %s' % e, '')


            # bước lấy câu trả lời
            try:
                res2 = driver.page_source
                soup2 = BeautifulSoup(res2, "html.parser")
                cau_tra_loi = soup2.find_all("div", class_="markdown")[-1]
                cau_tra_loi = html.unescape(str(cau_tra_loi))
                if cau_tra_loi == None:
                    cau_tra_loi = ''
                cau_tra_loi = str(cau_tra_loi).replace('Title: ', '')
                cau_tra_loi = cau_tra_loi.replace('<button><svg><path></path><rect></rect></svg>Copy code</button>', '')
                cau_tra_loi = str(cau_tra_loi).replace('''<button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button>''', '')

                cau_tra_loi = cau_tra_loi.replace("h1", "h2")
                cau_tra_loi = _remove_all_attrs_except_href(str(cau_tra_loi))
                cau_tra_loi_social = str(cau_tra_loi)

                # print('cau_tra_loi_social', cau_tra_loi_social)

            except Exception as e:
                print('Bước lấy câu trả lời cau_tra_loi_social lỗi: %s' % e, '')
                cau_tra_loi_social = ''



            
            ############################################################################
            print("Nhập promt 5 lấy link meta")
            try:
                time.sleep(2)
                tao_value = f'''
                    As an SEO expert specializing in keyword research, your objective is to create a well-rounded content plan for a specific target keyword. This task involves the creation of a comprehensive and strategic content plan drawn from your expertise in SEO and compliance with recent Google Quality guidelines and Google E-A-T rules.

                    Your content plan should encompass the following components:

                    Under the header “Meta Title”, you’re required to write a 60 to 70 characters meta title involving the main keyword. Be sure to implement attention-grabbing, click-through-rate (CTR) driven titles. Refrain from using quotation marks around the content. The main purpose of the title is to be featured on Google Discovery and top Google search results
                    Under “Meta Description”, craft a 150 to 160 characters CTR-driven meta description for this page based on the provided data. Create a description that draws attention and encourages a click. Please do not add quotation marks around the content.

                    Under Introduction, write an Introduction around 50 words with primary keyword

                    Under Conclusion, write an Conclusion around 50 words 

                    Bear in mind, the end reader will find the content beneficial, instantly valuable, and easy to read. Your plan should lure clicks and promptly answer the searcher’s intent. Retain your creativity and attention to detail while adhering to all specified guidelines and requirements.
                    Target keyword: [{keyword}]".
                    '''
                # Xoá xuống dòng
                try:
                    xoa_xuong_dong_script = " ".join([s for s in tao_value.splitlines()])
                    xoa_xuong_dong_script = xoa_xuong_dong_script.replace('"', '')
                    xoa_xuong_dong_script = xoa_xuong_dong_script.replace("'", "'")
                except Exception as e:
                    print('Bước xoá xuống dòng lỗi: %s' % e, '')


                input_field = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
                input_field.send_keys(f"""{xoa_xuong_dong_script}""")



                time.sleep(5)

                # nhấn click
                def skip_info2():
                    actions2 = ActionChains(driver)
                    actions2.send_keys(Keys.ENTER)
                    actions2.perform()

                # Calling a function
                skip_info2()

                time.sleep(1)

            except Exception as e:
                print('Bước nhập câu hỏi lỗi nhập lại câu hỏi lần 2: %s' % e, '')


            try:
                time.sleep(2)
                buttons = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.justify-start:last-of-type button.rounded-lg:last-of-type')))

                time.sleep(10)

            except Exception as e:
                print('Bước đợi 150s lỗi, nhập lại lần 2: %s' % e, '')


            # bước lấy câu trả lời
            try:
                res2 = driver.page_source
                soup2 = BeautifulSoup(res2, "html.parser")
                cau_tra_loi = soup2.find_all("div", class_="markdown")[-1]
                cau_tra_loi = html.unescape(str(cau_tra_loi))
                if cau_tra_loi == None:
                    cau_tra_loi = ''
                cau_tra_loi = str(cau_tra_loi).replace('Title: ', '')
                cau_tra_loi = cau_tra_loi.replace('<button><svg><path></path><rect></rect></svg>Copy code</button>', '')
                cau_tra_loi = str(cau_tra_loi).replace('''<button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button>''', '')

                cau_tra_loi = cau_tra_loi.replace("h1", "h2")
                # cau_tra_loi = _remove_all_attrs(str(cau_tra_loi))
                cau_tra_loi_meta = str(cau_tra_loi)

                

                # print('cau_tra_loi_meta', cau_tra_loi_meta)

            except Exception as e:
                print('Bước lấy câu trả lời cau_tra_loi_meta lỗi: %s' % e, '')
                cau_tra_loi_meta = ''


            if cau_tra_loi_meta:
                try:
                    cau_tra_loi_meta_soup = BeautifulSoup(cau_tra_loi_meta, "html.parser")

                    paragraphs_tag = cau_tra_loi_meta_soup.find_all('p')

                    if len(paragraphs_tag) == 4:

                        Meta_Title = paragraphs_tag[0].get_text()
                        Meta_Title = str(Meta_Title).replace("Meta Title:", "")
                        Meta_Description = paragraphs_tag[1].get_text()
                        Meta_Description = str(Meta_Description).replace("Meta Description:", "")
                        Meta_Introduction = paragraphs_tag[2].get_text()
                        Meta_Introduction = str(Meta_Introduction).replace("Introduction:", "")
                        Meta_Conclusion = paragraphs_tag[3].get_text()
                        Meta_Conclusion = str(Meta_Conclusion).replace("Conclusion:", "")

                    else:
                        Meta_Title = paragraphs_tag[0].get_text()
                        Meta_Title = str(Meta_Title).replace("Meta Title:", "")

                    
                except Exception as e:
                    print('Bước lấy Meta_Title lỗi: %s'%e,'')
                    Meta_Title = ''
                    Meta_Description = ''
                    Meta_Introduction = ''
                    Meta_Conclusion = ''



        else:
            cau_tra_loi_content = ''
            cau_tra_loi_paa = ''
            cau_tra_loi_social = ''
            Meta_Title = ''
            Meta_Description = ''
            Meta_Introduction = ''
            Meta_Conclusion = ''
            pass


    else:
        cau_tra_loi_content = ''
        cau_tra_loi_paa = ''
        cau_tra_loi_social = ''
        Meta_Title = ''
        Meta_Description = ''
        Meta_Introduction = ''
        Meta_Conclusion = ''
        pass


    time.sleep(5)
    driver.quit()

    return cau_tra_loi_content, cau_tra_loi_paa, cau_tra_loi_social, Meta_Title, Meta_Description, Meta_Introduction, Meta_Conclusion













if __name__ == '__main__':


    list_tklquan = ["seo", 'kiếm tiền online']
    list_url = 'https://www.celebritynetworth.com/richest-celebrities/actors/dann-florek-net-worth/, https://www.justjared.com/2024/01/25/richest-law-order-svu-cast-members-ranked-lowest-to-highest-by-estimated-net-worth-1-is-worth-100-million/6/, https://en.wikipedia.org/wiki/Dann_Florek, https://www.sarkariexam.com/danny-pino-net-worth-details-about-gf-career-film-age-cars-earnings/452848, https://www.nbc.com/nbc-insider/why-dann-florek-cragen-left-svu, https://www.celebritynetworth.com/richest-celebrities/actors/dann-florek-net-worth/, https://www.justjared.com/2024/01/25/richest-law-order-svu-cast-members-ranked-lowest-to-highest-by-estimated-net-worth-1-is-worth-100-million/6/, https://en.wikipedia.org/wiki/Dann_Florek, https://www.sarkariexam.com/danny-pino-net-worth-details-about-gf-career-film-age-cars-earnings/452848, https://www.nbc.com/nbc-insider/why-dann-florek-cragen-left-svu'

    language = 'vietnam'
    keyword = 'Dann Florek Net Worth'
    domain_name = 'vansonnguyen.com'
    brand_name = 'Vansonnguyen.com'

    cau_tra_loi_content, cau_tra_loi_paa, cau_tra_loi_social, Meta_Title, Meta_Description, Meta_Introduction, Meta_Conclusion = automation_promt1(list_url, keyword, domain_name, brand_name, folder_save_folder)
    
    print("cau_tra_loi_content", cau_tra_loi_content)
    print("cau_tra_loi_paa", cau_tra_loi_paa)
    print("cau_tra_loi_social", cau_tra_loi_social)
    print("Meta_Title", Meta_Title)
    print("Meta_Description", Meta_Description)
    print("Meta_Introduction", Meta_Introduction)
    print("Meta_Conclusion", Meta_Conclusion)


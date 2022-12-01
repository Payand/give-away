from requests import options
from giveaway import db
from flask_login import current_user
from giveaway.models import Post
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium .webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from giveaway.config import USERNAME, PASSWORD
import time






class Lottory:

    @classmethod
    def log_in(cls):
        options = Options()
        options.headless = True
        print('Opening designated Link...')
        cls.browser = webdriver.Chrome(options=options)
        cls.browser.get("http://www.instagram.com")     
        # cls.browser.maximize_window()
        print('login in progress')
        username =WebDriverWait(cls.browser, 10).until(EC.element_to_be_clickable
                                                             ((By.CSS_SELECTOR,"input[name='username']")))
        password =WebDriverWait(cls.browser, 10).until(EC.element_to_be_clickable
                                                             ((By.CSS_SELECTOR,"input[name='password']")))
        
        username.clear()
        password.clear()

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)    
        
        #Pressing login button
        log_in_btn = WebDriverWait(cls.browser,20).until(EC.element_to_be_clickable
                                                               ((By.CSS_SELECTOR,"button[type='submit']")))
        log_in_btn.click()     
        # To press not now 
        not_now_one = WebDriverWait(cls.browser,20).until(EC.element_to_be_clickable
                                                                ((By.XPATH,"//button[contains(text(),'Not Now')]")))
        not_now_one.click()
        #To press not now button Notification, disabeled for headless mode
        """
            not_now_two = WebDriverWait(cls.browser,20).until(EC.element_to_be_clickable
                                                                    ((By.XPATH,"//button[contains(text(),'Not Now')]")))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
            not_now_two.click()
        """
        time.sleep(5)
        print('Login Successful ...')
    
    @classmethod
    def get_followers(cls,url):
        print('Get page link...')
        cls.browser.get(url)
        time.sleep(3)
        followers_count = cls.browser.find_element(By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div/span').text
        print('Get the followers count...')
        return followers_count

    
    @classmethod
    def countinue_on_followers(cls,url):
        
        
        cls.browser.get(url)
        followers_count = cls.browser.find_element(By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div/span').text
        if 'K' in followers_count:
            first_refinery_k = followers_count.split('k')
            second_refinery_k= round(float(first_refinery_k[0]))
            int_to_string_k = str(second_refinery_k) + '000'
            final_followers_count = int_to_string_k
        elif 'M' in followers_count:
            first_refinery_m = followers_count.split('k')
            second_refinery_m = round(float(first_refinery_m[0]))
            int_to_string_m= str(second_refinery_m) + '000000'
            final_followers_count = int_to_string_m
        else:
            final_followers_count = followers_count  
        
        print('Followers count is : {}'.format(final_followers_count))
        time.sleep(3)
        cls.browser.find_element(By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div').click()
        time.sleep(4)
        print('Please wait ,Scraping in progross...')
        followers_list_scroll = cls.browser.find_element(By.XPATH,'/html/body/div[5]/div/div/div/div[2]')
        scroll_count = round(int(final_followers_count) // 12)
        followers_final_set = set()
        for _ in range (0,scroll_count+1):
            time.sleep(2)
            cls.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_list_scroll)
            time.sleep(3)
            followers_lists = followers_list_scroll.find_elements(By.TAG_NAME,'li')
            for follower in followers_lists:
                follower_name = follower.find_element(By.TAG_NAME,'a')
                if follower_name.get_attribute('href'):
                    followers_extract_href = follower_name.get_attribute('href')
                    follower_extract_link = followers_extract_href.replace("https://www.instagram.com/", "")
                    follower_extract_char = follower_extract_link.replace("/","")
                    followers_final_set.add(follower_extract_char)
       
        print('Scraping was successful...')
        followers_names_list = list(followers_final_set)
        time.sleep(10)
        # cls.browser.close()
        print('progress has been completed!')
        return followers_names_list
        
    @classmethod
    def get_likers(cls,url):
        cls.browser.get(url)
        likes_count = cls.browser.find_element(By.XPATH, 
                                                '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span').text
        return likes_count
    
    @classmethod
    def countinue_on_likers(cls,url):
        cls.browser.get(url)
        print('Get post link ...')
        cls.browser.get(url)
        time.sleep(5)
        likes_count = cls.browser.find_element(By.XPATH, 
                                                '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span')
        raw_extracted_num =likes_count.text
        time.sleep(2)
        if "," in raw_extracted_num:
            pure_one = raw_extracted_num.split(',')
            raw_extracted_num = pure_one[0]+pure_one[1]
        
        print('liks count is : {}'.format(raw_extracted_num))
        WebDriverWait(cls.browser,10).until(EC.element_to_be_clickable
                                                ((By.XPATH,'//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a'))).click()
        time.sleep(5)
        counts = round(int(raw_extracted_num) // 12)
        likers_ul = cls.browser.find_element(By.XPATH,'/html/body/div[5]/div/div/div[2]/div')
        first_one = likers_ul.find_element(By.CLASS_NAME,'notranslate')
        time.sleep(3)
        final_likers_set = set()
        final_likers_set.add(first_one.text)
        print('Please wait ,Scraping in progross...')
        for _ in range(0,counts+1):
            time.sleep(2)
            cls.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", likers_ul)
            time.sleep(8)
            likers_name = likers_ul.find_elements(By.TAG_NAME,'a')
            for like in likers_name:
                if like.get_attribute("href"):       
                    names_link = like.get_attribute("href")
                    name_without_link=names_link.replace('https://www.instagram.com/','')
                    name_without_char = name_without_link.replace('/','')
                    final_likers_set.add(name_without_char)
        print("likes count is {}".format(len(final_likers_set)))
        print('Scraping was successful...')
        likers_name_list =list(final_likers_set)
        time.sleep(10)
        # cls.browser.close()
        print('Progress has been completed!')
        return likers_name_list
       
    @classmethod
    def comment_section_scroller(cls,url):
        all_comment_section = []
        cls.browser.get(url)
        print('Get post link ...')
        time.sleep(5)
        owner_element = cls.browser.find_element(By.XPATH,
                                                  "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/div/span/a")
        def expand_comments_section():
            comment_section_elements = cls.browser.find_elements(By.CSS_SELECTOR,"svg[aria-label = 'Load more comments']")
            time.sleep(3)        
            for btn in comment_section_elements:
                if btn:
                    time.sleep(3)
                    btn.click()
                    time.sleep(3)
                    expand_comments_section()
                else: 
                    break
        expand_comments_section()
        print('Page name is :' + owner_element.text)
        comments_name = cls.browser.find_elements(By.CLASS_NAME,"C4VMK")
        time.sleep(5)
        for comment in comments_name:
            if owner_element.text not in comment.text:
                all_comment_section.append(comment.text)
        return all_comment_section     
            
    @classmethod
    def get_comments_tags(cls,url,type):
        comments_split = []
        taggers_commenters_list = []
        purified_final_dict={}
        all_comment_section_comments=cls.comment_section_scroller(url)
        time.sleep(4)
        if type == 'comments_plan':
            for commenters in all_comment_section_comments:
                if "@" not in commenters:
                    comments_split.append(commenters.split('\n'))
        if type == 'tags_plan':
            for commenters in all_comment_section_comments:
                if "@" in commenters:
                    comments_split.append(commenters.split('\n'))
        for comment in comments_split:
            purified_final_dict.setdefault(comment[0],[]).append(comment[1])
        for key,value in purified_final_dict.items():
            no_double = set(value)
            value = list(no_double)
            cls.insert_data(key,type,value)    
            taggers_commenters_list.append(key)          
        print('Scraping was successful...')
        time.sleep(10)
        print('progress has been completed!')
        return taggers_commenters_list
    
    @classmethod
    def get_combine(cls,url):
        likers = cls.countinue_on_likers(url)
        comments = cls.get_comments_tags(url,'comments_plan')
        tags = cls.get_comments_tags(url,'tags_plan')
        owner_element = cls.browser.find_element(By.XPATH,
                                                  "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/div/span/a")
        print(owner_element.text)
        followers = cls.countinue_on_followers('https://www.instagram.com/'+ owner_element.text)
        time.sleep(2)
        create_combine_list = [*likers,*comments,*tags,*followers]
        time.sleep(3)
        return create_combine_list
    
    @classmethod
    def close_window(cls,second):
        time.sleep(second)
        cls.browser.close()
    
    @classmethod
    def insert_data(cls,owner,type,data):
        list_to_string = ",".join(map(str,data))
        set_data_to_tabel = Post(user_username=owner, 
                                 type=type, 
                                 tag_mention_followers_urls=list_to_string,
                                 counts=len(data),
                                 author=current_user)
        db.session.add(set_data_to_tabel) 
        db.session.commit()     
    






   
        
        
        
        
        
        
        
        
        
        
        
    
    

















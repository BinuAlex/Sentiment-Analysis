from selenium import webdriver
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from time import sleep
import sqlite3 as sql
import sqlite3

option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument('--ignore-certificate-errors')
browser = webdriver.Chrome(executable_path='C:/Users/Admin/Downloads/chromedriver.exe', options= option)
url =  "https://www.etsy.com/in-en/listing/784884891/star-hoops-huggie-hoop-earrings-mini?ref=search_srv-5"
browser.get(url)
time.sleep(2)
user_agent={'User-Agent':'Chrome'}
response = requests.get(url, headers = user_agent)
soup = BeautifulSoup(response.text, 'html.parser')
review_scraped = {'review':[]}

for i in range(1,12):
    try:
        for r in range(4):  
            h= browser.find_element_by_xpath('//*[@id="review-preview-toggle-' +str(r)+'"]').text
            review_scraped['review'].append(h)  
    except:
        pass
    get_review = browser.find_element_by_xpath('//*[@id="reviews"]/div[2]/nav/ul/li[position() = last()]/a')
    get_review.click()
    sleep(4)

reviews = pd.DataFrame(review_scraped)
reviews.to_csv('reviews_scraped.csv', index=False) 


conn = sql.connect('etsy_product_review.db')

reviews.to_sql('reviews', conn, index =  False)


#load the database table back to dataframe
conn = sql.connect('etsy_product_review.db')
new_df = pd.read_sql('SELECT * FROM reviews ',conn)
new_df.to_csv('etsy_product_review.csv', index=False) 
print(new_df.sample(5))  



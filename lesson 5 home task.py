import time
from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo_ru']
goods_db = db['results']

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

url = "https://www.mvideo.ru/"

driver.get(url)

#todo: я попадаю на капчу, планировал добавить куки, чтобы не вылетало, но еще не разобрался как их добыть целиком а не построчно. пока убирал руками.
#driver.add_cookie({"VID": "24_sRS2_g42400000V0-D4o4:::0-0-0-628efb2:CAASENA_-b6FYTxAol5tgLjq7bAaYEFhJ-H-vyKcV7tg3fhYomKHXQGh_74M9kwoTWAGc2XejIbPC1p4-ejaw2bEEFUfiQJ9cdpu0DruD1cOtkiG5-JTo9M_AgsAE9hQ22jrIAATwB7_7lqVBk111RtRTRfpqg",})

time.sleep(1)

#driver.find_element_by_class_name('geolocation__action-approve-city').click()

#todo: найти блок в котором лежат товары. через xpath текст
#наверное можно сделать проще, новинки лежат в списке у которого есть атрибут: ul data-init-param= {} "title":"Новинки", но я не нашел пока как зацепиться за элемент словаря атрибута.
#anchor_element = driver.find_element_by_xpath('//ul[contains(., "title"]') - неудачно
new_products_block = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/ancestor::div[3]")

#todo: в этом блоке ищем стрелку в право, цикл идет пока у стрелки вправо не появится класс disabled, next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right disabled
button_next = new_products_block.find_element_by_xpath("//a[contains(@class, 'next-btn')]")

while True:
#    if driver.find_element_by_css_selector("a[class='next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right disabled']")\
    if new_products_block.find_element_by_xpath("//a[contains(@class, 'next-btn') and contains(@class, 'disabled') ]"):
        break
    else:
        try:
            time.sleep(2)
            button_next = new_products_block.find_element_by_xpath("//a[contains(@class, 'next-btn')]")
            button_next.click()
        except Exception as e:
            print(e)
            break

#todo: собираем товары которые лежат в этом же блоке gallery-list-item начиная с rel="0" до rel="0"
goods_raw = new_products_block.find_elements_by_xpath("//li[contains(@class, 'gallery-list-item')]")
goods = []

for good in goods_raw:
    single_product = {}
    target_element = good.find_element_by_xpath("//a[contains(@class, 'fl-product-tile-picture__link')]")
    single_product.update(target_element.get_attribute('data-product-info'))
#    single_product.update(good.find_element_by_xpath("//a[contains(@class, 'fl-product-tile-picture__link')]").get_attribute('data-product-info'))
    single_product['link'] = f'{url}{"/".join(target_element.get_attribute("href")[0].split("/")[1:])}'
    goods.append(single_product)

for good in goods:
    goods_db.update_one(
                {'link':good['link']},
                {'$set':good},
                upsert=True)
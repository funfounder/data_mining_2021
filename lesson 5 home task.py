import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get("https://www.mvideo.ru/")

#todo: я попадаю на капчу, планировал добавить куки, чтобы не вылетало, но еще не разобрался как их добыть целиком а не построчно. пока убирал руками.
#driver.add_cookie({"VID": "24_sRS2_g42400000V0-D4o4:::0-0-0-628efb2:CAASENA_-b6FYTxAol5tgLjq7bAaYEFhJ-H-vyKcV7tg3fhYomKHXQGh_74M9kwoTWAGc2XejIbPC1p4-ejaw2bEEFUfiQJ9cdpu0DruD1cOtkiG5-JTo9M_AgsAE9hQ22jrIAATwB7_7lqVBk111RtRTRfpqg",})

time.sleep(1)

button_geo = driver.find_element_by_class_name('geolocation__action-approve-city')
button_geo.click()

#todo: найти блок в котором лежат товары. через xpath текст


#todo: в этом блоке ищем стрелку в право, цикл идет пока у стрелки вправо не появится класс disabled, next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right disabled

#можно сделать проще: ul data-init-param= {} "title":"Новинки"

#driver.findElement(By.xpath('//*[@data-init-param='title":"Новинки"']))

while True:
    if driver.find_element_by_css_selector("a[class='next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right disabled']"):
        break
    else:
        try:
            driver_wait = WebDriverWait(driver, 10)
            right_button = driver_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right']")))
            right_button.click()
        except Exception as e:
            print(e)
            break

#todo: собираем товары которые лежат в этом же блоке gallery-list-item начиная с rel="0" до rel="0"

right_scroll = True

#//*[text() = 'Новинки']

#if driver.find_element_by_xpath("//input[@id='passwd-id']"):
#    driver.findElement(By.xpath("//*[text()='Get started free']"));
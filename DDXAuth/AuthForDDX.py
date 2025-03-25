import os
from time import sleep

import pickle
# сохранение куков в файл
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.page_load_strategy = "eager"
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 5, poll_frequency=0.5)

url = "https://www.freeconferencecall.com/global/fr/login"
driver.get(url)

email_field = driver.find_element("xpath", "//*[@id='login_email']")
email_field.send_keys("autocheck@ya.ru")

password_field = driver.find_element("xpath", "//*[@id='password']")
password_field.send_keys("123")

CHECKBOX_LOCATOR = ("xpath", "//*[@id='gdpr_checkbox']")
driver.find_element(*CHECKBOX_LOCATOR).click()

login_button = driver.find_element("xpath", "(//*[@id='loginformsubmit'])[1]")
login_button.click()

#Сохранение куки в текущую директорию
pickle.dump(driver.get_cookies(), open(os.getcwd()+"/cookies.pkl", "wb"))

driver.close()

#СОЗДАËМ НОВУЮ СЕССИЮ
user_cookies = webdriver.Chrome(options=options)

user_cookies.get(url)
user_cookies.delete_all_cookies()

cookies = pickle.load(open(os.getcwd()+ "/cookies.pkl", "rb"))
#ЦИКЛ ДЛЯ ПОДСТАНОВКИ КУКОВ:
for cookie in cookies:
    try:
        user_cookies.add_cookie(cookie) #будем добавлять по одной куке
    except Exception as e:
        print(f"Ошибка при добавлении cookie: {e}")
        
#Проверяем куки рефрешем
sleep(3)
user_cookies.refresh()
sleep(5)

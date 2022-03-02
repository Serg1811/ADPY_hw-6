import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from tokens import login_yandex, password_yandex

driver = webdriver.Firefox()
driver.get('https://passport.yandex.ru/auth/')
elem = driver.find_element(by=By.NAME, value='login')
time.sleep(1)
elem.send_keys(login_yandex)
time.sleep(1)
elem.send_keys(Keys.RETURN)
time.sleep(1)
print(driver.page_source)
assert 'no result found.' not in driver.page_source
elem = driver.find_element(by=By.NAME, value='passwd')
elem.send_keys(password_yandex)
time.sleep(1)
elem.send_keys(Keys.RETURN)
print(driver.page_source)
assert 'no result found.' not in driver.page_source
time.sleep(3)
driver.close()
driver.quit()

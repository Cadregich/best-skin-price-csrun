from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


def check_majority(driver):
    switch_label = driver.find_element(By.CSS_SELECTOR, 'label.agree-switcher')
    switch_label.click()


def set_needed_price(driver, min_price, max_price):

    min_price_input = driver.find_elements(By.ID, 'market-filter-minPrice')[0]
    max_price_input = driver.find_elements(By.ID, 'market-filter-minPrice')[1]
    min_price_input.clear()
    max_price_input.clear()
    min_price_input.send_keys(min_price)
    max_price_input.send_keys(max_price)


def load_all_items(driver):
    while True:
        try:
            load_more_btn = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.load-more')))
            load_more_btn.click()
            time.sleep(1)
        except:
            break


min_price = input("Минимальная сумма: ")
max_price = input("Максимальная сумма: ")

chrome_driver_path = './chromedriver.exe'
os.environ['PATH'] += ';' + os.path.dirname(os.path.abspath(chrome_driver_path))

driver = webdriver.Chrome()

driver.get('https://csgo3.run/market/')

wait = WebDriverWait(driver, 3)

check_majority(driver)

set_needed_price(driver, min_price, max_price)

load_all_items(driver)

# driver.implicitly_wait(3)

drop_preview_elements = driver.find_elements(By.CLASS_NAME, 'drop-preview')

print("Количество товаров:", len(drop_preview_elements))
print('\n', '_______________________')

items = []

for card in drop_preview_elements:
    price_el = card.find_element(By.CLASS_NAME, 'drop-preview__price')
    title_el = card.find_element(By.CLASS_NAME, 'drop-preview__subtitle')
    desc_el = card.find_element(By.CLASS_NAME, 'drop-preview__desc')

    item_data = {
        "price": price_el.text,
        "title": title_el.text,
        "wear": desc_el.text
    }

    items.append(item_data)

    print("Цена:", item_data["price"])
    print("Название:", item_data["title"])
    print("Износ:", item_data["wear"])
    print('_______________________')

driver.quit()

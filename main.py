from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import os
import time
import requests


class SteamMarketScraper:
    def __init__(self):
        self.top_prices = {
            'csgo': [],
            'dota': [],
            'rust': []
        }
        self.total_iterations = 0
        self.items_total_count = 0
        self.items_game = ''

    def init(self, min_price, max_price):
        chrome_driver_path = './chromedriver.exe'
        os.environ['PATH'] += ';' + os.path.dirname(os.path.abspath(chrome_driver_path))

        driver = webdriver.Chrome()
        driver.get('https://csgo3.run/market/')
        # wait = WebDriverWait(driver, 3)
        self.check_majority(driver)
        self.set_needed_price(driver, min_price, max_price)

        time.sleep(1)
        log_delimiter = '____________________________'

        print("\nПолучаем предметы с рана...")

        self.load_all_items(driver)

        drop_preview_elements = driver.find_elements(By.CLASS_NAME, 'drop-preview')

        self.items_total_count = len(drop_preview_elements)

        print("\nКоличество предметов:", self.items_total_count, '\n', log_delimiter)
        print("\nПредметы успешно полученны, обрабатываем их... \n", log_delimiter)

        items = self.process_csrun_items(drop_preview_elements, log_delimiter)

        print("\nВсе предметы успешно обработаны \n", log_delimiter)

        driver.quit()

        csgo_items = []
        rust_items = []
        dota_items = []

        for item in items:
            if item['title'] != '' and item['subtitle'] == '' and item['wear'] != '':
                dota_items.append(item)
            elif item['title'] != '' and item['subtitle'] == '' and item['wear'] == '':
                if item['title'] == 'Engineer SMG':
                    rust_items.append(item)
            else:
                csgo_items.append(item)

        print('Найденно вещей из csgo: ', len(csgo_items), '\n', log_delimiter)
        print('Найденно вещей dota 2: ', len(dota_items), '\n', log_delimiter)
        print('Найденно вещей rust: ', len(rust_items), '\n', log_delimiter)

        print('\nПриступаем к получению цен... \n', log_delimiter, '\n')

        self.start_looking_items_in_steam_market(csgo_items, 'csgo')
        self.start_looking_items_in_steam_market(dota_items, 'dota')

    def process_csrun_items(self, drop_preview_elements, log_delimiter):
        items = []
        for card in drop_preview_elements:
            price_el = card.find_element(By.CLASS_NAME, 'drop-preview__price')
            title_el = card.find_element(By.CLASS_NAME, 'drop-preview__title')
            subtitle_el = card.find_element(By.CLASS_NAME, 'drop-preview__subtitle')
            desc_el = card.find_element(By.CLASS_NAME, 'drop-preview__desc')

            item_data = {
                "price": price_el.text,
                "title": title_el.text,
                "subtitle": subtitle_el.text,
                "wear": desc_el.text
            }

            items.append(item_data)

            print("Цена:", item_data["price"])
            print("Название:", item_data["title"])
            print("Износ:", item_data["wear"])
            print(log_delimiter)

        return items

    def check_majority(self, driver):
        switch_label = driver.find_element(By.CSS_SELECTOR, 'label.agree-switcher')
        switch_label.click()

    def set_needed_price(self, driver, min_price, max_price):
        min_price_input = driver.find_elements(By.ID, 'market-filter-minPrice')[0]
        max_price_input = driver.find_elements(By.ID, 'market-filter-minPrice')[1]
        min_price_input.clear()
        max_price_input.clear()
        min_price_input.send_keys(min_price)
        max_price_input.send_keys(max_price)

    def load_all_items(self, driver):
        while True:
            try:
                load_more_btn = WebDriverWait(driver, 1).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, '.load-more')))
                load_more_btn.click()
                time.sleep(1)
            except:
                break

    def update_top_prices(self, top_price_item_data, wears):
        self.top_prices[self.items_game].append(top_price_item_data)
        if len(self.top_prices[self.items_game]) > 20:
            self.top_prices[self.items_game].sort(key=lambda x: x['difference_in_percents'], reverse=True)
            self.top_prices[self.items_game].pop()

        self.top_prices[self.items_game].sort(key=lambda x: x['difference_in_percents'], reverse=True)
        self.setTopPrices(wears)

    def setTopPrices(self, wears):

        with open("result.txt", "w", encoding='utf-8') as file:
            file.write('Предметы из CS:GO:\n')
            self.write_top_prices_in_file(file, 'csgo', wears)
            file.write('\nПредметы из Dota 2:\n')
            self.write_top_prices_in_file(file, 'dota', wears)
            file.write('\nПредметы из Rust:\n')
            self.write_top_prices_in_file(file, 'rust', wears)

    def write_top_prices_in_file(self, file, game, wears):
        for skin_data in self.top_prices[game]:
            file.write(f"{skin_data['name']} ")
            file.write(
                f"({skin_data['wear']}) "
                if skin_data['wear'] in wears else ''
            )
            file.write(
                f"=> {skin_data['difference_in_percents']}%\n"
                f"Цены: {skin_data['run_price']}$ => {skin_data['steam_price']}$"
                f"\n________________________\n"
            )

    def start_looking_items_in_steam_market(self, items, items_game):
        self.items_game = items_game
        wears = self.getWears()
        english_wears = self.getWearsOnEnglish()

        for item in items:
            attempts_to_get_item_data = 0
            url = self.getItemUrl(item, items_game, wears ,english_wears)
            while True:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()

                    try:
                        run_price = float(item['price'].replace('$', ''))
                        steam_price = float(data['lowest_price'].replace('$', ''))
                        difference_in_percents = round(((steam_price - run_price) / run_price) * 100, 1)
                        price_info = f'Цены: {run_price} $ => {steam_price} $ | {difference_in_percents}%'

                        self.logChekingSuccess(item, items_game, price_info, wears)

                        result_item_key = self.getResoultItemKey(item)

                        self.update_top_prices({
                            'name': result_item_key,
                            'difference_in_percents': difference_in_percents,
                            'run_price': run_price,
                            'steam_price': steam_price,
                            'wear': item['wear']
                        }, wears)

                        break
                    except Exception:
                        print('Не удалось получить минимальную цену для', url, '\n')
                        if attempts_to_get_item_data < 2 and item['title'] != 'Sticker':
                            print('Возможно предмет незагрузился, попробуем ещё раз')
                            time.sleep(2)
                            attempts_to_get_item_data += 1
                        else:
                            break
                elif response.status_code == 429:
                    self.logCheckingError429(response.status_code, url)
                    time.sleep(60)
                else:
                    print(f"Ошибка запроса: {response.status_code} для предмета: \n {url}")
                    if item['title'] == 'Sticker':
                        print('Вероятнее всего существует несколько его версий \n')
                    break

            self.total_iterations += 1
            print(f"Предметов обработанно: {self.total_iterations} / {self.items_total_count} \n")

    def getItemUrl(self, item, items_game, wears, englishWears):
        url = ''
        if items_game == 'csgo':
            if item['wear'] in wears:
                url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={item['title']} | " \
                      f"{item['subtitle']} ({englishWears[item['wear']]})"
            else:
                url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={item['title']} | " \
                      f"{item['subtitle']}"
        elif items_game == 'dota':
            url = 'https://steamcommunity.com/market/priceoverview/?appid=570&currency=1' \
                  f"&market_hash_name={item['title']}"
        return url

    def logChekingSuccess(self, item, items_game, price, wears):
        if items_game == 'dota':
            print(item['title'])
            print(price, '\n')

        elif items_game == 'csgo':
            print(item['title'], '|', item['subtitle'],
                  f'({item["wear"]})' if item['wear'] in wears else '')
            print(price, '\n')

    def logCheckingError429(self, status_code, url):
        print(f"Ошибка запроса: {status_code} \n {url}")
        print("Получен код ошибки 429. Ждём минутку и продолжаем кошмарить сервер ^) \n")

    def getResoultItemKey(self, item):
        key = f"{item['title']}"
        key += f"{' | ' + item['subtitle'] if item['subtitle'] != '' else ''}"
        return key

    def getWears(self):
        return {
            'Прямо с завода',
            'Немного поношенное',
            'После полевых',
            'Поношенное',
            'Закалённое в боях'
        }

    def getWearsOnEnglish(self):
        return {
            'Прямо с завода': 'Factory New',
            'Немного поношенное': 'Minimal Wear',
            'После полевых': 'Field-Tested',
            'Поношенное': 'Well-Worn',
            'Закалённое в боях': 'Battle-Scarred'
        }


min_price = input("Минимальная сумма: ")
max_price = input("Максимальная сумма: ")

steamScrapper = SteamMarketScraper()

steamScrapper.init(min_price, max_price)

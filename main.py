from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

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
        self.items_total_count = {
            'csgo': 0,
            'dota': 0,
            'rust': 0
        }
        self.items_game = ''

        self.wears = {
            'FN',
            'MW',
            'FT',
            'WW',
            'BS'
        }

        self.wears_full_name = {
            'FN': 'Factory New',
            'MW': 'Minimal Wear',
            'FT': 'Field-Tested',
            'WW': 'Well-Worn',
            'BS': 'Battle-Scarred'
        }

    def init(self, max_price, min_price):
        min_price = float(min_price)
        log_delimiter = '____________________________'
        chrome_driver_path = './browserdriver.exe'
        os.environ['PATH'] += ';' + os.path.dirname(os.path.abspath(chrome_driver_path))

        driver = webdriver.Chrome()
        driver.get('https://csgo5.run/profile/inventory')
        self.set_needed_price(driver, max_price)
        time.sleep(1)

        games_block = driver.find_element(By.CSS_SELECTOR, '#market > div.contents.w-full.shrink-0.flex-col.pt-1.lg\:flex.lg\:h-full.lg\:w-67\.5.lg\:pb-5 > div.order-2.flex.gap-1\.5.lg\:flex-col')
        dota_btn = games_block.find_element(By.XPATH, './*')
        rust_btn = games_block.find_element(By.XPATH, './child::*[3]')
        market_name = driver.find_element(By.CSS_SELECTOR, '#market > div.group.relative.order-5.-mx-2\.5.flex.flex-col.overflow-hidden.lg\:-mr-5.lg\:ml-0.lg\:rounded-br-3xl > div.place-content-top.grid.grid-cols-3.gap-1\.5.overflow-auto.overscroll-contain.px-2\.5.py-3.scrollbar-mb-3.scrollbar-mt-3.sm\:grid-fill-28.lg\:mr-2\.25.lg\:grid-cols-6.lg\:pb-5.lg\:pl-0.lg\:pr-2\.75.lg\:scrollbar-mb-5')

        csgo_items = self.get_all_game_items(driver, market_name, 'csgo', min_price, log_delimiter)
        dota_btn.click()
        time.sleep(1)
        dota_items = self.get_all_game_items(driver, market_name, 'dota', min_price, log_delimiter)
        rust_btn.click()
        time.sleep(1)
        rust_items = self.get_all_game_items(driver, market_name, 'rust', min_price, log_delimiter)

        driver.quit()

        print('Найдено вещей из csgo: ', len(csgo_items), '\n', log_delimiter)
        print('Найдено вещей dota 2: ', len(dota_items), '\n', log_delimiter)
        print('Найдено вещей rust: ', len(rust_items), '\n', log_delimiter)

        print('\nПриступаем к получению цен... \n', log_delimiter, '\n')

        self.start_looking_items_in_steam_market(csgo_items, 'csgo')
        self.start_looking_items_in_steam_market(dota_items, 'dota')
        self.start_looking_items_in_steam_market(rust_items, 'rust')

    def get_all_game_items(self, driver, market_block, game, min_price, log_delimiter):
        print(f"\nПолучаем {game} предметы с маркета csgorun...")

        self.load_all_items(driver, market_block, min_price)

        print(f"\nПредметы из {game} успешно получены, обрабатываем их... \n", log_delimiter)

        try:
            drop_preview_elements = market_block.find_elements(By.TAG_NAME, 'button')
        except:
            print(f'\nНе нашли предметов из {game} :( \n', log_delimiter)
            return []

        result_items = []

        for item in drop_preview_elements:
            process_result = self.process_csrun_item(item, min_price, log_delimiter)
            if process_result != 'done':
                result_items.append(self.process_csrun_item(item, min_price, log_delimiter))

        print(f"\nВсе предметы из {game} успешно обработаны \n", log_delimiter)

        self.items_total_count[game] = len(result_items)

        return result_items

    def process_csrun_item(self, card, min_price, log_delimiter):
        item_data = self.get_item_data(card)
        if item_data["price"] is not None:
            price = float(item_data["price"].replace('$', '').strip())

            if price < min_price:
                return 'done'

        print("Цена:", item_data["price"])
        print("Название:", self.get_full_item_title(item_data))
        print("Износ:", item_data["wear"])
        print(log_delimiter)

        return item_data

    def get_item_data(self, card):
        def find_element_or_empty(card, locator):
            try:
                element = card.find_element(*locator)
                return element.text
            except NoSuchElementException:
                return ""

        title_locator = (By.CSS_SELECTOR,
                         'div.absolute.inset-x-2\.5.bottom-3.leading-tight.lg\:inset-x-4\.5.lg\:bottom-4 > div:nth-child(1)')
        subtitle_locator = (By.CSS_SELECTOR,
                            'div.absolute.inset-x-2\.5.bottom-3.leading-tight.lg\:inset-x-4\.5.lg\:bottom-4 > div:nth-child(2)')
        wear_locator = (By.CLASS_NAME, 'rounded-sm')
        price_locator = (By.CLASS_NAME, 'font-bold')

        title = find_element_or_empty(card, title_locator)
        subtitle = find_element_or_empty(card, subtitle_locator)
        wear = find_element_or_empty(card, wear_locator)
        price = find_element_or_empty(card, price_locator)

        return {
            "price": price,
            "title": title,
            "subtitle": subtitle,
            "wear": wear
        }

    def set_needed_price(self, driver, max_price):
        max_price_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Макс. цена"]')
        max_price_input.clear()
        max_price_input.send_keys(max_price)

    def load_all_items(self, driver, block, min_price):
        while True:
            try:
                old_height = block.get_attribute("scrollHeight")

                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", block)

                time.sleep(1)

                new_height = block.get_attribute("scrollHeight")

                if new_height == old_height:
                    break

                last_item = block.find_elements(By.TAG_NAME, 'button')[-1]
                item_data = self.get_item_data(last_item)
                if item_data["price"] is not None:
                    price = float(item_data["price"].replace('$', '').strip())
                    if price < min_price:
                        break
            except:
                break

    def update_top_prices(self, top_price_item_data):
        self.top_prices[self.items_game].append(top_price_item_data)
        if len(self.top_prices[self.items_game]) > 20:
            self.top_prices[self.items_game].sort(key=lambda x: x['difference_in_percents'], reverse=True)
            self.top_prices[self.items_game].pop()

        self.top_prices[self.items_game].sort(key=lambda x: x['difference_in_percents'], reverse=True)
        self.set_top_prices()

    def set_top_prices(self):
        with open("result.txt", "w", encoding='utf-8') as file:
            file.write('Предметы из CS:GO:\n')
            self.write_top_prices_in_file(file, 'csgo')
            file.write('\nПредметы из Dota 2:\n')
            self.write_top_prices_in_file(file, 'dota')
            file.write('\nПредметы из Rust:\n')
            self.write_top_prices_in_file(file, 'rust')

    def write_top_prices_in_file(self, file, game):
        for skin_data in self.top_prices[game]:
            file.write(f"{skin_data['name']} ")
            file.write(
                f"({skin_data['wear']}) "
                if skin_data['wear'] in self.wears else ''
            )
            file.write(
                f"=> {skin_data['difference_in_percents']}%\n"
                f"Цены: {skin_data['run_price']}$ => {skin_data['steam_price']}$"
                f"\n________________________\n"
            )

    def start_looking_items_in_steam_market(self, items, items_game):
        self.items_game = items_game

        for item in items:
            attempts_to_get_item_data = 0
            url = self.get_item_url(item, items_game)
            while True:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    try:
                        run_price = float(item['price'].replace('$', ''))
                        steam_price = float(data['lowest_price'].replace('$', ''))
                        difference_in_percents = round(((steam_price - run_price) / run_price) * 100, 1)
                        price_info = f'Цены: {run_price} $ => {steam_price} $ | {difference_in_percents}%'

                        self.log_checking_success(item, items_game, price_info)

                        result_item_key = self.get_full_item_title(item)

                        self.update_top_prices({
                            'name': result_item_key,
                            'difference_in_percents': difference_in_percents,
                            'run_price': run_price,
                            'steam_price': steam_price,
                            'wear': item['wear']
                        })

                        break
                    except Exception:
                        print('Не удалось получить минимальную цену для', url, '\n')
                        if attempts_to_get_item_data < 2 and item['title'] != 'Sticker':
                            print('Возможно предмет не загрузился, попробуем ещё раз')
                            time.sleep(2)
                            attempts_to_get_item_data += 1
                        else:
                            break
                elif response.status_code == 429:
                    self.log_checking_error_429(response.status_code, url)
                    time.sleep(60)
                else:
                    print(f"Ошибка запроса: {response.status_code} для предмета: \n {url}")
                    if item['title'] == 'Sticker':
                        print('Вероятнее всего существует несколько его версий \n')
                    break

            self.total_iterations += 1
            print(f"Предметов обработано из {items_game}: {self.total_iterations} / {self.items_total_count[items_game]} \n")

    def get_item_url(self, item, items_game):
        url = ''
        if items_game == 'csgo':
            if item['wear'] in self.wears:
                url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={item['title']} | " \
                      f"{item['subtitle']} ({self.wears_full_name[item['wear']]})"
            else:
                url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={item['title']} | " \
                      f"{item['subtitle']}"
        elif items_game == 'dota':
            url = 'https://steamcommunity.com/market/priceoverview/?appid=570&currency=1' \
                  f"&market_hash_name={item['title']}"
        return url

    def log_checking_success(self, item, items_game, price):
        if items_game == 'dota':
            print(item['title'])
            print(price, '\n')

        elif items_game == 'csgo':
            print(item['title'], '|', item['subtitle'],
                  f'({item["wear"]})' if item['wear'] in self.wears else '')
            print(price, '\n')

    def log_checking_error_429(self, status_code, url):
        print(f"Ошибка запроса: {status_code} \n {url}")
        print("Получен код ошибки 429. Ждём минутку и продолжаем кошмарить сервер ^) \n")

    def get_full_item_title(self, item):
        key = f"{item['title']}"
        key += f"{' | ' + item['subtitle'] if item['subtitle'] != '' else ''}"
        return key


max_price = input("Максимальная сумма: ")
min_price = input("Минимальная сумма: ")

steamScrapper = SteamMarketScraper()

steamScrapper.init(max_price, min_price)

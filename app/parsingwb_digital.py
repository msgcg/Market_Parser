import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
try:
    from .parsing import init_webdriver, save_cookies, load_cookies
    from .telegram_debugger import send_debug
except:
    from parsing import init_webdriver, save_cookies, load_cookies
    from telegram_debugger import send_debug
def parse_wildberries_category(category_url,cookies_f,req_ses):
    product_data = []
    processed_ids = set()

    # Use webdriver_manager to handle ChromeDriver installation/updates
    try:
        driver = init_webdriver()
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        send_debug(f"Error initializing WB WebDriver: {e}")
        return []

    try:
        driver.get(category_url)
        print(f"Страница цифровых товаров вб {category_url} скачана успешно")
        send_debug(f"Страница цифровых товаров вб {category_url} скачана успешно")
        load_cookies(driver,cookies_f)
        driver.refresh()
        WebDriverWait(driver, 1.3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.offer-card-new__title"))
        )  # Wait for at least one product to load

        # --- Scrolling Logic ---
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1.7,2))  # Give the page time to load (adjust as needed)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # No more content loaded
            last_height = new_height
        save_cookies(driver,cookies_f)
        # --- Extract Product Links ---
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        offer_links = [link.get('href') for link in soup.find_all('a', class_='offer-card-new__title') if link.get('href')]
        offer_links = list(set(offer_links)) #remove dublicates
        print(f"найдено {len(offer_links)} ссылок для цифрового вб")
        send_debug(f"найдено {len(offer_links)} ссылок для цифрового вб")

        retry_count = 0  # Счётчик неудачных попыток
        max_delay = 600  # 10 минут в секундах
        base_delay = 3   # Начальная задержка
        max_wait_reached_count = 0  # Счётчик случаев, когда достигли максимальной задержки

        # --- Process Each Product Link (same as before, but with Selenium-gathered links) ---
        for link in offer_links:
            try:
                offer_id = link.split('/')[-1]
                if not offer_id.isdigit():
                    print(f"Skipping invalid offer link: {link}")
                    continue
                if offer_id in processed_ids:
                    continue
                processed_ids.add(offer_id)

                api_url = f"https://digital.wildberries.ru/api/v1/offers/{offer_id}"

                while True:
                    try:
                        load_cookies(req_ses, cookies_f)
                        api_response = req_ses.get(api_url)
                        api_response.raise_for_status()
                        product_json = api_response.json()
                        save_cookies(req_ses, cookies_f)

                        # --- Extract relevant data (adapt to your needs) ---
                        try:
                            product = {
                                'id': product_json.get('id'),
                                'name': product_json.get('title'),
                                'price': product_json.get('priceb', {}).get('regular_price'),
                                'salePriceU': product_json.get('priceb', {}).get('discount_price'),
                                'cashback': None,
                                'sale': None,
                                'brand': product_json.get('author', {}).get('nickname'),
                                'rating': product_json.get('rating'),
                                'supplier': product_json.get('author', {}).get('nickname'),
                                'supplierRating': product_json.get('author', {}).get('rating'),
                                'feedbacks': product_json.get('feedback_count'),
                                'reviewRating': product_json.get('rating'),
                                'promoTextCard': None,
                                'promoTextCat': None,
                                'update': datetime.datetime.now().strftime("%Y-%m-%d"),
                                'link': urljoin(category_url, link),
                            }
                            product_data.append(product)

                            # Если запрос успешный, сбрасываем счетчики задержек
                            retry_count = 0
                            max_wait_reached_count = 0
                            print(f"Успешный парсинг карточки {product['name']}")
                            break  # Успешный парсинг — переходим к следующему offer_id

                        except AttributeError as e:
                            print(f"Error extracting data for product {offer_id}: {e}. JSON: {product_json}")
                            break

                    except req_ses.exceptions.RequestException as e:
                        if api_response.status_code == 429:
                            retry_count += 1
                            delay = min(base_delay * 2**retry_count, max_delay)  # Экспоненциальное увеличение задержки
                            delay += random.uniform(-delay * 0.2, delay * 0.2)  # Добавляем случайный разброс (±20%)

                            print(f"Страница {offer_id} вернула 429. Ждём {int(delay)} сек. Попытка #{retry_count}")
                            time.sleep(delay)

                            if delay >= max_delay:
                                max_wait_reached_count += 1
                                if max_wait_reached_count >= 2:
                                    print("Достигнуто два 10-минутных ожидания без результатов. Пропускаем оставшиеся ссылки.")
                                    break  # Выходим из цикла обработки offer_links

                        else:
                            print(f"Error processing offer {link}: {e}")
                            break  # Если ошибка не 429, прекращаем попытки

            except (json.JSONDecodeError, AttributeError) as e:
                print(f"Error processing offer {link}: {e}")
                continue


    except Exception as e:
        print(f"An error occurred: {e}")
        send_debug(f"An error WB DIGITAL PARSING occurred: {e}")
        return []
    finally:
        driver.quit()  # Always quit the driver, even if errors occur

    return product_data

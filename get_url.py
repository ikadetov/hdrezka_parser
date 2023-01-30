# Imports
from selenium.webdriver.common.by import By
import re

from driver import create_driver


def find_season_tabs(driver):
    try:
        driver.find_element(By.XPATH, '//*[@id="simple-seasons-tabs"]')  # Try to get season bar
        return True
    except:
        return False


def check_series_url(url):
    while True:
        s = re.search(r"#t:(\d{1,4})-s:(\d{1,4})-e:(\d{1,4})$", url)
        if s:
            t = s.group(1)  # Get series code
            break
        else:
            print("Похоже вы ввели не полный url. Пожалуйста выберите любую серию и скопируйте полный url!")
            url = input("URL: ")

    return url, t


def get_url():
    while True:  # Endless loop for missing in url

        url = input("URL: ")
        if url.startswith("https://rezka.ag/") and ".html" in url and url.count('/') >= 4:  # Check url
            print("Проверяем url...")
        else:
            print("Неверный url. Используйте сайт https://rezka.ag")
            continue

        driver = create_driver(5)  # Creating driver

        try:
            driver.get(url)
        except Exception as e:
            pass
        finally:
            title = driver.title
            if title == "404 Not Found":  # Check existing of WebPage
                print("Неверный url!")
                continue
            is_series = find_season_tabs(driver)  # Try to find season bar (existing only in series)
            if is_series:
                url, t = check_series_url(url)  # Find series code
                break
            else:
                t = False  # If film code = False
                break
    return url, t, title

from account_usage import *
from configureproxy import load_proxy_list
from browser import create_firefox_browser

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException
from captcha_solver import solve_captcha
import tempfile
import base64
import requests
import random
import secrets
import string
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import base64
from PIL import Image
from io import BytesIO
from transliterate import transliterate
import io
import shutil
import os
import logging
import zipfile
from dotenv import load_dotenv
import os
from browser import create_firefox_browser 
import sys
import io
import requests 
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def get_external_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        ip = response.json()["ip"]
        return ip
    except requests.RequestException as e:
        logging.error(f"Error getting external IP: {e}")
        return None


load_dotenv()
capmonster_api_key = os.getenv("CAPMONSTER_API_KEY")

from concurrent.futures import ThreadPoolExecutor
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def save_full_profile(source_dir, target_dir):
    """Копирует и сжимает профиль Firefox из исходной директории в целевую."""
    zip_target = target_dir + '.zip'
    if os.path.exists(zip_target):
        os.remove(zip_target)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    shutil.copytree(source_dir, target_dir, ignore=shutil.ignore_patterns('parent.lock', '*.lock'))
    # Сжатие копированного профиля в архив ZIP
    with zipfile.ZipFile(zip_target, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(target_dir, '..')))
    shutil.rmtree(target_dir) 


def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def save_account_details(username, password):
    with open("accounts.txt", "a") as file:
        file.write(f"{username}:{password}\n")

def check_phone_request(driver):
    try:
        # Попытка найти элемент с сообщением о запросе номера телефона
        phone_error = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[4]/div[4]/div/div/div/div/form/div[18]/div/div/div[3]/small")
        if phone_error.is_displayed():
            logging.error(f"Phone number requested: {phone_error.text}")
            return True
    except NoSuchElementException:
        # Элемент не найден, значит запроса номера телефона нет
        return False


def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.2))

def generate_password(length=12):
    while True:
        characters = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = ''.join(secrets.choice(characters) for i in range(length))
        
        # Проверка на простые последовательности и популярные пароли
        if not (any(char.isdigit() for char in password) and
                any(char.isupper() for char in password) and
                any(char.islower() for char in password) and
                any(char in "!@#$%^&*()" for char in password) and
                password not in ['123456', 'qwerty', 'password']):
            continue
        
        return password





def register_and_save_account(name, surname, year):
    try:
        driver = create_firefox_browser()
        if register_account(driver, capmonster_api_key, name, surname, year):
            logging.info(f"Registration and profile saving completed for {name} {surname}")
        else:
            logging.info(f"Registration failed for {name} {surname}, profile not saved.")
    except Exception as e:
        logging.error(f"Error occurred for {name} {surname}: {str(e)}")
    finally:
        driver.quit()


def register_account(driver, capmonster_api_key, name, surname, year):
    try:
        wait = WebDriverWait(driver, 10)
        driver.get("https://account.mail.ru/signup")
        time.sleep(5)

        # Заполнение формы регистрации
        first_name = driver.find_element(By.ID, "fname")
        human_type(first_name, name)
        last_name = driver.find_element(By.ID, "lname")
        human_type(last_name, surname)
        select_date(driver, random.randint(1, 28))
        select_month(driver, random.choice(['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']))
        select_year(driver, year)
        select_sex(driver, "Мужской")

        # Генерация и ввод логина
        base_username = transliterate(f"{name}.{surname}{random.randint(1, 9999)}")
        max_length = 30
        if len(base_username) > max_length:
            base_username = base_username[:max_length]
        username = base_username.lower()
        username_field = driver.find_element(By.ID, "aaa__input")
        human_type(username_field, username)

        domain = select_domain(driver)
        # Генерация и ввод пароля
        password = generate_password()
        password_field = driver.find_element(By.ID, "password")
        human_type(password_field, password)
        repeat_password_field = driver.find_element(By.ID, "repeatPassword")
        human_type(repeat_password_field, password)

        # Отправка формы
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)

        # Обработка капчи
        captcha_solution = solve_captcha(driver, capmonster_api_key)
        if captcha_solution:
            captcha_input_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Код"]')))
            human_type(captcha_input_field, captcha_solution)
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", submit_button)
            time.sleep(5)

        # Проверка наличия запроса номера телефона
        if check_phone_request(driver):
            logging.error("Phone number request detected, registration aborted.")
            return False

        # Проверка попадания на страницу с входящей почтой
        inbox_xpath = "//a[contains(@href, '/inbox/')]"
        if wait.until(EC.presence_of_element_located((By.XPATH, inbox_xpath))):
            # Сохранение деталей учётной записи
            save_account_details(f"{username}@{domain}", password)
            profile_dir = driver.capabilities['moz:profile']
            target_dir = f'full_profiles/{name}_{surname}'
            save_full_profile(profile_dir, target_dir)

            logging.info(f"Account successfully registered for {name} {surname}")
            return True
        else:
            logging.error("Did not reach inbox page, registration aborted.")
            return False

    except Exception as e:
        logging.error(f"An error occurred during registration for {name} {surname}: {e}")
        return False
    finally:
        driver.quit()
    

def register_and_save_account(name, surname, year, proxy=None):
    try:
        driver = create_firefox_browser(proxy)
        if register_account(driver, capmonster_api_key, name, surname, year):
            logging.info(f"Registration and profile saving completed for {name} {surname}")
        else:
            logging.info(f"Registration failed for {name} {surname}, profile not saved.")
    except Exception as e:
        logging.error(f"Error occurred for {name} {surname}: {str(e)}")
    finally:
        driver.quit()

def main():
    names_surnames = []
    with open("names_surnames.txt", "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                name, surname = line.strip().split()
                names_surnames.append((name, surname))

    proxies = load_proxy_list("proxies.txt")
    if proxies:
        logging.info(f"Loaded {len(proxies)} proxies from file.")
    else:
        logging.warning("No proxies loaded from file.")

    external_ip = get_external_ip()
    if external_ip:
        logging.info(f"Your external IP is: {external_ip}")
    else:
        logging.warning("Could not determine external IP.")

    random.shuffle(names_surnames)

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        for i, (name, surname) in enumerate(names_surnames):
            proxy = proxies[i % len(proxies)] if proxies else None
            futures.append(executor.submit(register_and_save_account, name, surname, random.randint(1970, 2002), proxy))
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
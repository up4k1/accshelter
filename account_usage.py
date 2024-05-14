import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import random


def select_date(driver, day):
    wait = WebDriverWait(driver, 10)
    day_dropdown_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Select__control")))
    day_dropdown_button.click()
    time.sleep(2)
    xpath_string = f"//div[@data-test-id='select-option-wrapper']//div[@data-test-id='select-value:{day}']//span[text()='{day}']"
    day_to_select = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_string)))
    day_to_select.click()


def select_month(driver, month):
    wait = WebDriverWait(driver, 10)
    month_dropdown_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Месяц')]")))
    month_dropdown_button.click()
    time.sleep(2)
    month_xpath = f"//div[@data-test-id='select-option-wrapper']//span[text()='{month}']"
    month_to_select = wait.until(EC.element_to_be_clickable((By.XPATH, month_xpath)))
    month_to_select.click()


def select_year(driver, year):
    wait = WebDriverWait(driver, 10)
    year_dropdown_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Год')]")))
    year_dropdown_button.click()
    time.sleep(2)
    year_xpath = f"//div[@data-test-id='select-option-wrapper']//span[text()='{year}']"
    year_to_select = wait.until(EC.element_to_be_clickable((By.XPATH, year_xpath)))
    year_to_select.click()

def select_sex(driver, sex):
    wait = WebDriverWait(driver, 10)
    sex_xpath = f"//span[contains(text(), '{sex}')]"
    sex_option = wait.until(EC.element_to_be_clickable((By.XPATH, sex_xpath)))
    sex_option.click()


def select_domain(driver):
    wait = WebDriverWait(driver, 10)
    domains = ["mail.ru", "internet.ru", "bk.ru", "inbox.ru", "list.ru"]
    random.shuffle(domains)
    # Нажимаем на кнопку, чтобы открыть список доменов
    domain_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div/div[4]/div[4]/div/div/div/div/form/div[12]/div/div[2]/div[1]/div/div/div[3]/div/div/div")))
    domain_button.click()
    time.sleep(2)
    for domain in domains:
        try:
            domain_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@data-test-id='select-option-wrapper']//span[text()='@{domain}']")))
            domain_option.click()
            return domain
        except NoSuchElementException:
            continue
    raise Exception("No available domains found.")
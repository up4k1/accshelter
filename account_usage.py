import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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
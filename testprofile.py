from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def load_saved_profile(profile_path):
    # Установка настроек для Firefox
    options = Options()
    options.profile = profile_path
    # Включение профиля с сохранённой сессией
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    # Открытие браузера с загруженным профилем
    driver.get("https://www.google.com")  # Можешь изменить URL на нужный тебе
    return driver

def main():
    profile_path = 'full_profiles/Степан_Гончаров.zip'  # Укажи правильный путь к профилю
    driver = load_saved_profile(profile_path)
    input("Press Enter to close the browser...")  # Пауза перед закрытием браузера
    driver.quit()

if __name__ == "__main__":
    main()

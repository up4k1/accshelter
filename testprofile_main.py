from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import os
import zipfile

def extract_and_load_profile(zip_profile_path, extract_to_dir):
    """Распаковывает ZIP-архив профиля и загружает его в Firefox."""
    # Убедимся, что папка для распаковки существует или создадим её
    if not os.path.exists(extract_to_dir):
        os.makedirs(extract_to_dir)

    # Распаковываем ZIP
    with zipfile.ZipFile(zip_profile_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_dir)

    # Получаем путь к распакованной папке профиля
    profile_dir = os.path.join(extract_to_dir, os.listdir(extract_to_dir)[0])

    # Загружаем профиль в браузер
    options = Options()
    options.profile = profile_dir
    service = Service(executable_path='./geckodriver-0.34.0/geckodriver-0.34.0/')  # Указываем путь к geckodriver
    driver = webdriver.Firefox(options=options, service=service)
    return driver

def main():
    profile_zip = './full_profiles/Глеб_Левин.zip'  # Путь к ZIP-архиву с профилем
    extract_to = './full_profiles/extracted'  # Папка для распаковки
    driver = extract_and_load_profile(profile_zip, extract_to)
    try:
        driver.get("https://www.google.com")  # Открываем страницу для проверки
        input("Press Enter to close the browser...")  # Ждём нажатия Enter для закрытия
    finally:
        driver.quit()  # Закрываем браузер

if __name__ == "__main__":
    main()

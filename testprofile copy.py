from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import os
import zipfile

def extract_profile(profile_zip_path, extract_to_path):
    """Распаковывает профиль из ZIP-архива."""
    with zipfile.ZipFile(profile_zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)
    return os.path.join(extract_to_path, os.listdir(extract_to_path)[0])  # Возвращает путь к распакованной папке

def load_saved_profile(profile_path):
    """Загружает профиль Firefox."""
    options = Options()
    # Указываем путь к профилю
    options.add_argument(f"-profile {profile_path}")
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.google.com")
    return driver

def main():
    profile_zip = './full_profiles/Дмитрий_Панов.zip'  # Абсолютный путь к архиву профиля
    extract_to = './full_profiles/extracted'  # Путь, куда будет распакован профиль
    profile_path = extract_profile(profile_zip, extract_to)  # Распаковываем и получаем путь к профилю
    driver = load_saved_profile(profile_path)  # Загружаем профиль в браузер
    input("Press Enter to close the browser...")
    driver.quit()

if __name__ == "__main__":
    main()

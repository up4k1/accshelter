# browser.py
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from fake_useragent import UserAgent

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def create_firefox_browser():
    path_to_geckodriver = './geckodriver-0.34.0/geckodriver-0.34.0/'  # Укажите путь к geckodriver
    service = Service(executable_path=path_to_geckodriver)
    options = Options()
    options.set_preference("media.peerconnection.enabled", False)
    options.set_preference("media.navigator.permission.disabled", True)
    options.set_preference("media.navigator.streams.fake", True)
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.socks", "192.168.3.238")
    options.set_preference("network.proxy.socks_port", 3066)
    options.set_preference("network.proxy.socks_version", 5)
    options.set_preference("network.proxy.socks_remote_dns", True)
    user_agent = get_random_user_agent()
    options.set_preference("general.useragent.override", user_agent)
    driver = webdriver.Firefox(service=service, options=options)
    driver.set_window_size(1920, 1080)
    return driver

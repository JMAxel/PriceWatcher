from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver(headless: bool = True):
    options = Options()
    if headless:
        options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--lang=pt-BR')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    return driver

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading


class DriverPool:
    _driver = None
    _lock = threading.Lock()

    @classmethod
    def get_driver(cls):
        with cls._lock:
            if cls._driver is None:
                chrome_options = Options()
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--window-size=1920,1080")
                chrome_options.add_argument("--disable-dev-shm-usage")
                user_agent = (
                    "user-agent=Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0 Safari/537.36"
                )
                chrome_options.add_argument(user_agent)

                cls._driver = webdriver.Chrome(options=chrome_options)
            return cls._driver

    @classmethod
    def shutdown(cls):
        with cls._lock:
            if cls._driver:
                cls._driver.quit()
                cls._driver = None

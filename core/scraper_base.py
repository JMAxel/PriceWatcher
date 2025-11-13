from core.selenium_driver import get_driver
import time
from abc import ABC, abstractmethod


class ScraperBase(ABC):
    def __init__(
        self, url: str, use_selenium: bool = True, wait_time: int = 3
    ):
        self.url = url
        self.use_selenium = use_selenium
        self.wait_time = wait_time

    def get_price(self) -> float:
        if self.use_selenium:
            return self._get_price_with_selenium()
        else:
            raise NotImplementedError("Not yet implemented.")

    def _get_price_with_selenium(self) -> float:
        driver = get_driver(headless=True)
        try:
            driver.get(self.url)
            time.sleep(self.wait_time)
            return self._extract_price(driver)
        finally:
            driver.quit()

    @abstractmethod
    def _extract_price(self, driver) -> float:
        pass

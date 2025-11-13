from core.scraper_base import ScraperBase
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class AmazonScraper(ScraperBase):
    def _extract_price(self, driver):
        selectors = [
            (By.ID, "priceblock_ourprice"),
            (By.ID, "priceblock_dealprice"),
            (By.CSS_SELECTOR, ".a-price .a-offscreen"),
        ]

        for by, selector in selectors:
            try:
                elem = driver.find_element(by, selector)
                price_text = elem.text.strip()
                price = (
                    price_text.replace("R$", "")
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
                )
                return float(price)
            except NoSuchElementException:
                continue
        raise ValueError("Preço não encontrado na Amazon.")

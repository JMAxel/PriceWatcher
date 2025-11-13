from scrapers.amazon_scraper import AmazonScraper
from bs4 import BeautifulSoup


def test_extract_price_from_html():
    html = '<span id="priceblock_ourprice">R$ 249,90</span>'
    soup = BeautifulSoup(html, "html.parser")
    scraper = AmazonScraper("https://fakeurl.com")
    price = scraper.extract_price(soup)
    assert price == 249.90

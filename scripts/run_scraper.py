from core.database import Database
from scrapers.amazon_scraper import AmazonScraper


def main():
    db = Database()

    products = db.get_products()
    for product in products:
        print(f"Consultando {product['name']} ({product['store']})...")
        if "amazon" in product["url"]:
            scraper = AmazonScraper(product["url"])
            try:
                new_price = scraper.get_price()
                db.update_price(product["id"], new_price)
                db.insert_price_history(product["id"], new_price)
                print(f"Novo preço: R$ {new_price:.2f}")
            except Exception as e:
                print(f"Erro ao consultar preço: {e}")

    db.close()


if __name__ == "__main__":
    main()

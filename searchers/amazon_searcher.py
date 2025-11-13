from core.selenium_driver import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time


class AmazonSearcher:
    def __init__(
        self,
        base_url: str = "https://www.amazon.com.br",
        wait_time: int = 3
    ):
        self.base_url = base_url
        self.wait_time = wait_time

    def _extract_name_and_url(self, item):
        """Tenta extrair nome e URL com múltiplos seletores."""
        link_selectors = [
            "a.a-link-normal.s-line-clamp-4",
            "a.a-link-normal.s-line-clamp-3",
            "a.a-link-normal.s-line-clamp-2",
            "h2 a",
            "a.a-link-normal.a-text-normal",
        ]

        for selector in link_selectors:
            try:
                link = item.find_element(By.CSS_SELECTOR, selector)
                url = link.get_attribute("href")

                # Tentar pegar o nome de diferentes formas
                name = None
                name_selectors = ["h2 span", "span.a-text-normal", "h2"]

                for name_sel in name_selectors:
                    try:
                        name_elem = link.find_element(
                            By.CSS_SELECTOR, name_sel
                        )
                        name = name_elem.text.strip()
                        if name:
                            return name, url
                    except NoSuchElementException:
                        continue

                # Se encontrou o link mas não o nome, tenta direto do link
                name = link.text.strip()
                if name:
                    return name, url

            except NoSuchElementException:
                continue

        return None, None

    def _extract_price(self, item):
        """Tenta extrair preço com múltiplos seletores."""
        price_selectors = [
            (
                "span.a-price[data-a-color='base'] span.a-offscreen",
                "textContent",
            ),
            ("span.a-price span.a-offscreen", "text"),
            ("span.a-price-whole", "text"),
            (".a-price .a-offscreen", "text"),
        ]

        for selector, method in price_selectors:
            try:
                price_elem = item.find_element(By.CSS_SELECTOR, selector)

                if method == "textContent":
                    price_text = (
                        price_elem.get_attribute("textContent").strip()
                    )
                else:
                    price_text = price_elem.text.strip()

                if price_text:
                    # Limpar e converter
                    price_clean = (
                        price_text.replace("R$", "")
                        .replace("\u00a0", "")
                        .replace(".", "")
                        .replace(",", ".")
                        .strip()
                    )
                    return float(price_clean)

            except (NoSuchElementException, ValueError, AttributeError):
                continue

        return None

    def search(self, query: str):
        print(f"Iniciando busca: {query}")
        driver = get_driver(headless=True)
        results = []

        try:
            print(f"Acessando: {self.base_url}")
            driver.get(self.base_url)
            time.sleep(self.wait_time)

            print(f"Título da página: {driver.title}")

            search_box = driver.find_element(By.ID, "twotabsearchtextbox")
            print("Caixa de busca encontrada")

            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            print("Busca enviada")

            time.sleep(self.wait_time)

            print(f"URL após busca: {driver.current_url}")

            items = driver.find_elements(
                By.CSS_SELECTOR,
                "div[data-component-type='s-search-result']"
            )
            print(f"Número de items encontrados: {len(items)}")

            for idx, item in enumerate(items[:5], 1):
                print(f"\nProcessando item {idx}")
                try:
                    # Extrair nome e URL
                    name, url = self._extract_name_and_url(item)

                    if not name or not url:
                        print("  Nome ou URL não encontrado, pulando item")
                        continue

                    print(f"  Nome: {name[:50]}...")
                    print(f"  URL: {url[:80]}...")

                    # Extrair preço
                    price = self._extract_price(item)

                    if price is None:
                        print("  Preço não encontrado, pulando item")
                        continue

                    print(f"  Preço: R$ {price:.2f}")

                    results.append({"name": name, "url": url, "price": price})

                except Exception as e:
                    print(f"  Erro ao processar item: {e}")
                    continue

            print(f"\nProdutos encontrados: {len(results)}")
            return results

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Erro ao realizar a busca na Amazon: {e}")
            import traceback
            traceback.print_exc()
            return []

        finally:
            driver.quit()

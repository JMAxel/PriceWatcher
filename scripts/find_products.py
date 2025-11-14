from searchers.amazon_searcher import AmazonSearcher
from core.selenium_driver import DriverPool
import sys


if __name__ == "__main__":
    # Verificar argumento da linha de comando
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "SSD Kingston NV2 1TB"

    print(f"Buscando por: {query}\n")

    searcher = AmazonSearcher()
    results = searcher.search(query)

    if not results:
        print("Nenhum produto encontrado!")
    else:
        for i, r in enumerate(results, start=1):
            preco = (f"R$ {r['price']:.2f}" if r["price"]
                     else "Preço indisponível")
            print(f"{i}. {r['name']} - {preco}")
            print(f"   {r['url']}\n")

    # Importante: Encerrar o driver somente aqui, após todas as buscas.
    DriverPool.shutdown()

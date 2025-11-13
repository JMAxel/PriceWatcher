from searchers.amazon_searcher import AmazonSearcher
import sys


if __name__ == "__main__":
    # Verificar se foi passado um argumento
    if len(sys.argv) > 1:
        # Juntar todos os argumentos em uma única query
        query = " ".join(sys.argv[1:])
    else:
        # Query padrão se nenhum argumento for passado
        query = "SSD Kingston NV2 1TB"
    
    print(f"Buscando por: {query}\n")
    
    searcher = AmazonSearcher()
    results = searcher.search(query)

    if not results:
        print("Nenhum produto encontrado!")
    else:
        for i, r in enumerate(results, start=1):
            print(f"{i}. {r['name']} - R$ {r['price']:.2f}")
            print(f"   {r['url']}\n")

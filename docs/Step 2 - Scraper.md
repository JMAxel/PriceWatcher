# 📘 Etapa 2 — Implementação do Scraper da Amazon

## 💡 Contexto Geral
Nesta etapa, o projeto ganha **capacidade de buscar produtos reais** na Amazon Brasil.  
Até aqui, tínhamos apenas o banco de dados preparado, mas sem forma de coletar informações de produtos.  
Agora, passamos a extrair dados reais (nome, preço e URL) diretamente da Amazon, criando a base para o monitoramento automático de preços.

---

## 🧩 O que foi construído
Implementamos um módulo chamado **`searchers/amazon_searcher.py`**, responsável por buscar produtos na Amazon usando **Selenium WebDriver** para automação de navegador.

Esse módulo:
- Acessa automaticamente a Amazon Brasil e realiza buscas por produtos.  
- Extrai informações estruturadas: nome, URL e preço atual.  
- Utiliza **múltiplos seletores CSS** como fallback para lidar com diferentes layouts de produtos.  
- Suporta diferentes categorias de produtos (eletrônicos, móveis, acessórios, etc.).  
- Oferece logs detalhados para debugging e análise de erros.

Em resumo: ele é o **"coletor de dados"** do sistema.

---

## 🧱 Estrutura do Scraper

### 🔍 Classe `AmazonSearcher`
Responsável por toda a lógica de busca e extração de dados.

#### Métodos Principais

| Método | Descrição |
|--------|-----------|
| `__init__()` | Inicializa o scraper com URL base e tempo de espera |
| `search(query)` | Realiza busca por produtos e retorna lista de resultados |
| `_extract_name_and_url(item)` | Extrai nome e URL com múltiplos seletores de fallback |
| `_extract_price(item)` | Extrai preço com diferentes estratégias de parsing |

#### Estrutura de Retorno
```python
{
    "name": "SSD Kingston NV2 1TB",
    "url": "https://www.amazon.com.br/...",
    "price": 450.99
}
```

---

## ⚙️ Como funciona na prática

### 1️⃣ **Inicialização**
```python
searcher = AmazonSearcher()
# Define URL base e tempo de espera padrão
```

### 2️⃣ **Busca de Produtos**
```python
results = searcher.search("SSD Kingston NV2 1TB")
# Retorna lista com até 5 produtos encontrados
```

### 3️⃣ **Extração Robusta**
O scraper tenta múltiplos seletores CSS em ordem de prioridade:

**Para Nome e URL:**
- `a.a-link-normal.s-line-clamp-4`
- `a.a-link-normal.s-line-clamp-3`
- `a.a-link-normal.s-line-clamp-2`
- `h2 a`
- `a.a-link-normal.a-text-normal`

**Para Preço:**
- `span.a-price[data-a-color='base'] span.a-offscreen`
- `span.a-price span.a-offscreen`
- `span.a-price-whole`
- `.a-price .a-offscreen`

### 4️⃣ **Tratamento de Preços**
O sistema limpa automaticamente:
- Símbolos monetários (`R$`)
- Espaços não-quebráveis (`\u00a0`)
- Separadores de milhares (`.`)
- Converte vírgula decimal (`,`) para ponto (`.`)

---

## 🛠️ Integração com o Projeto

### Script de Busca
Criamos **`scripts/find_products.py`** para testar o scraper:

```python
python -m scripts.find_products "Mesa Kuadra 180cm"
```

### Makefile Target
Adicionamos comando facilitado:

```bash
make search QUERY="Notebook Lenovo"
```

---

## 🧠 Desafios Resolvidos

### 1️⃣ **Diferentes Layouts de Produtos**
**Problema:** Notebooks têm HTML diferente de mesas ou eletrônicos.  
**Solução:** Implementamos múltiplos seletores com fallback automático.

### 2️⃣ **Produtos Sem Preço Visível**
**Problema:** Alguns produtos não exibem preço diretamente.  
**Solução:** Sistema pula produtos sem preço e continua processando.

### 3️⃣ **Espaços Não-Quebráveis**
**Problema:** Preços como `R$ 241,08` contêm caracteres especiais Unicode.  
**Solução:** Limpeza robusta com `replace("\u00a0", "")`.

### 4️⃣ **ChromeDriver Dependencies**
**Problema:** ChromeDriver falhava com exit code 127 no Linux.  
**Solução:** Documentação para instalar dependências corretas.

---

## 📊 Exemplo de Uso Completo

```python
from searchers.amazon_searcher import AmazonSearcher

# Inicializar scraper
searcher = AmazonSearcher()

# Buscar produtos
results = searcher.search("Mouse Gamer")

# Processar resultados
for product in results:
    print(f"{product['name']}")
    print(f"R$ {product['price']:.2f}")
    print(f"{product['url']}\n")
```

**Saída:**
```
Mouse Gamer Logitech G502 Hero
R$ 249.90
https://www.amazon.com.br/...

Mouse Gamer Razer DeathAdder V2
R$ 279.99
https://www.amazon.com.br/...
```

---

## 🧪 Testes e Validação

### Categorias Testadas
- ✅ Eletrônicos (notebooks, SSDs, mouses)
- ✅ Móveis (mesas, cadeiras)
- ✅ Periféricos (teclados, headsets)
- ✅ Produtos patrocinados vs orgânicos

### Logs de Debug
O sistema gera logs detalhados:
```
Iniciando busca: Mesa Kuadra 180cm
Título da página: Amazon.com.br
Caixa de busca encontrada
Busca enviada
Número de items encontrados: 16

Processando item 1
  Nome: Mesa Kuadra Office 180cm Preta
  URL: https://www.amazon.com.br/...
  Preço: R$ 899.90

Produtos encontrados: 5
```

---

## 🔄 Próximos Passos

Esta etapa preparou o terreno para:
1. **Integração com o banco de dados** — salvar produtos encontrados automaticamente.
2. **Monitoramento periódico** — executar buscas em intervalos regulares.
3. **Sistema de alertas** — notificar quando preços caírem abaixo do target.
4. **Múltiplas lojas** — expandir para Mercado Livre, Magazine Luiza, etc.

---

## ✅ O que você tem agora

- Um **scraper funcional da Amazon Brasil**.
- Extração robusta de **nome, preço e URL**.
- Sistema que funciona com **diferentes categorias de produtos**.
- **Múltiplos seletores de fallback** para maior confiabilidade.
- **Logs detalhados** para debugging.
- **Interface via terminal** com Makefile.

---

## 🚨 Boas Práticas para Manutenção

### Para desenvolvedores:
- **Respeite os robots.txt** da Amazon — não faça scraping agressivo.
- **Use headless mode** em produção para economizar recursos.
- **Implemente rate limiting** — adicione delays entre requisições.
- **Mantenha seletores atualizados** — a Amazon muda seu HTML frequentemente.
- **Salve screenshots em caso de erro** — facilita debugging.

### Rate Limiting Recomendado:
```python
import time

class AmazonSearcher:
    def __init__(self, wait_time=5):  # Aumentar para 5 segundos
        self.wait_time = wait_time
    
    def search(self, query):
        # ...busca...
        time.sleep(self.wait_time)  # Respeitar delay
```

### User-Agent Recomendado:
```python
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
```

---

## 📚 Recursos Adicionais

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [CSS Selectors Reference](https://www.w3schools.com/cssref/css_selectors.php)
- [Amazon Robots.txt](https://www.amazon.com.br/robots.txt)
- [Conventional Commits](https://www.conventionalcommits.org/)

---
# PriceWatcher --- Roadmap do Projeto

Sistema extensível de monitoramento de preços com scraping, notificações
em múltiplos canais e análise histórica.

## 0. Preparação Inicial

### Objetivos

-   Criar ambiente de desenvolvimento.
-   Definir estrutura de diretórios.
-   Instalar dependências mínimas.
-   Criar arquivo `.env.example`.

### Estrutura recomendada

    pricewatcher/
    ├── core/
    ├── scrapers/
    ├── notifiers/
    ├── services/
    ├── bot/
    ├── web/
    ├── tests/
    ├── scripts/
    ├── .env.example
    ├── requirements.txt
    └── README.md

### Dependências iniciais

-   requests\
-   beautifulsoup4\
-   python-telegram-bot\
-   schedule\
-   python-dotenv

### Critério de Aceitação

-   Projeto instala sem erros.
-   Variáveis `.env` são carregadas corretamente.

## 1. Banco de Dados (SQLite)

### Objetivos

-   Criar base sólida para armazenar produtos e histórico.
-   Preparar funções CRUD independentes.

### Estrutura de tabelas

    products(
      id, name, url, store, canonical_name,
      sku, target_price, last_price,
      active, margin_percent
    )

    price_history(
      id, product_id, price, date
    )

### Funcionalidades mínimas

-   Inserir produto.
-   Listar produtos.
-   Ativar/desativar produto.
-   Registrar nova medição de preço.
-   Consultar histórico por ID.

### Critério de Aceitação

-   Inserções, consultas e histórico funcionando via testes.

## 2. Scraping Básico (HTML Estático)

### Objetivos

-   Implementar o primeiro scraper funcional.
-   Definir interface padrão para scrapers.

### Componentes

-   BaseScraper\
-   example_store_scraper.py

### Critério de Aceitação

-   Scraper retorna nome e preço corretamente usando fixture HTML.

## 3. Monitoramento de Preços (Single Run)

### Objetivos

-   Criar mecanismo que:
    1.  Carrega produtos do DB
    2.  Obtém preços via scraper
    3.  Atualiza histórico
    4.  Retorna lista de mudanças

### Critério de Aceitação

-   Rodar um "check" atualiza o DB e grava o histórico corretamente.

## 4. Notificações via Telegram

### Objetivos

-   Integrar bot para envio de alertas.
-   Enviar alerta quando preço \<= target_price.

### Componentes

-   TelegramNotifier
-   Serviço de alerta com regra básica.

### Critério de Aceitação

-   Mensagens chegam no Telegram do admin após detecção de promoção.

## 5. Scheduler (Execução Automática)

### Objetivos

-   Permitir execução periódica (ex.: a cada X horas).

### Ferramentas

-   schedule
-   Script dedicado: run_scheduler.py

### Critério de Aceitação

-   Sistema executa "checks" periódicos sem travar.

## 6. Bot Administrativo (Telegram)

### Objetivos

-   Controlar produtos via bot.

### Comandos sugeridos

-   /listar
-   /adicionar `<url>`{=html} `<preco>`{=html}
-   /remover `<id>`{=html}
-   /alterar `<id>`{=html} `<preco>`{=html}
-   /pausar `<id>`{=html}
-   /reativar `<id>`{=html}
-   /media `<id>`{=html} \[N\]

### Critério de Aceitação

-   Comandos funcionam apenas para o ADMIN_CHAT_ID.

## 7. Múltiplos Canais: Discord e WhatsApp

### Objetivos

-   Tornar sistema extensível a vários canais.

### Componentes

-   DiscordNotifier (webhook)
-   WhatsAppNotifier (API externa)
-   Registro dinâmico de notifiers no serviço de alertas

### Critério de Aceitação

-   Mensagens chegam nos outros canais quando habilitados.

## 8. Normalização de Produtos (Cross-Store)

### Objetivos

-   Permitir cálculo de médias entre lojas diferentes.

### Implementação

-   Campo canonical_name
-   Campo opcional sku
-   Função de normalização automática

### Critério de Aceitação

-   Produtos iguais em lojas diferentes são agrupados corretamente.

## 9. Cálculo de Médias (Histórico e Entre Lojas)

### Objetivos

-   Implementar duas médias:
    -   Média histórica por produto
    -   Média entre lojas do mesmo item (canonical_name)

### Critério de Aceitação

-   Funções retornam os valores esperados em testes unitários.

## 10. Alertas Baseados em Média

### Objetivos

-   Enviar alerta quando preço atual estiver abaixo:
    -   da média histórica
    -   da média entre lojas
    -   menos a margem configurável

### Critério de Aceitação

-   Bot envia alertas diferenciando "abaixo do target" e "abaixo da
    média".

## 11. Painel Web (Opcional)

### Objetivos

-   Criar interface simples (Flask) para visualizar:
    -   Lista de produtos
    -   Histórico de preços (gráficos)

### Critério de Aceitação

-   Painel acessível localmente e apresentando dados reais.

## 12. Scrapers com Playwright (Conteúdo Dinâmico)

### Objetivos

-   Suportar lojas com JavaScript.

### Critério de Aceitação

-   Scraper com Playwright retorna preço corretamente.

## 13. Robustez e Respeito a Limites

### Objetivos

-   Melhorar estabilidade:
    -   Retry com backoff
    -   Headers dinâmicos
    -   Esperas aleatórias
    -   Consulta a robots.txt

### Critério de Aceitação

-   Sistema lida com erros de rede e tempo de resposta sem falhar.

## 14. Logs, Testes e CI

### Objetivos

-   Tornar projeto confiável.

### Itens

-   Logging estruturado
-   Testes unitários
-   GitHub Actions rodando pytest

### Critério de Aceitação

-   Pipeline passa e logs mostram cada etapa da execução.

## 15. Deploy Gratuito

### Opções

-   Render
-   Railway
-   Replit
-   PythonAnywhere

### Critério de Aceitação

-   Scheduler roda em produção com variáveis `.env` configuradas.

## 16. Extensões Futuras

-   Relatórios semanais
-   Gráficos enviados pelo Telegram
-   Interface multiusuário
-   Recomendação por machine learning
-   Suporte automático a novas lojas

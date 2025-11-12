# 📘 Etapa 1 — Introdução ao Banco de Dados do Projeto

## 💡 Contexto Geral
Nesta etapa, o projeto ganha **sua primeira estrutura técnica real**: um **banco de dados**.  
Até aqui, o sistema não tinha memória — tudo que ele fazia seria perdido após a execução.  
Agora, passamos a registrar informações de produtos e preços de forma **persistente e organizada**, criando a base para as próximas etapas (como o monitoramento real de preços e envio de alertas).

---

## 🧩 O que foi construído
Implementamos um módulo chamado **`core/database.py`**, responsável por conectar e gerenciar o banco de dados **SQLite**, um sistema leve e gratuito, ideal para projetos pequenos e de prototipagem.

Esse módulo:
- Cria automaticamente o banco de dados na primeira execução.  
- Define duas tabelas principais:
  - **`products`** → onde ficam os produtos monitorados.
  - **`price_history`** → onde ficam as variações de preço ao longo do tempo.  
- Oferece métodos prontos para:
  - Adicionar e remover produtos.
  - Atualizar preços.
  - Registrar histórico de preços.
  - Consultar dados para exibir ou analisar depois.

Em resumo: ele é o **"coração da memória"** do sistema.

---

## 🧱 Estrutura dos Dados

### 🗂️ Tabela `products`
Guarda as informações principais de cada produto.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Identificador único |
| name | TEXT | Nome do produto |
| url | TEXT | Link direto para o produto |
| store | TEXT | Nome da loja |
| target_price | REAL | Preço desejado (para alertas) |
| last_price | REAL | Último preço registrado |
| active | INTEGER | Define se o produto está sendo monitorado |

### 📈 Tabela `price_history`
Guarda todas as mudanças de preço registradas com data e hora.

| Campo | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Identificador do histórico |
| product_id | INTEGER | Referência ao produto monitorado |
| price | REAL | Preço encontrado |
| date | TIMESTAMP | Data/hora automática do registro |

---

## ⚙️ Como funciona na prática
1. Quando o sistema inicia, ele cria o banco de dados se ele ainda não existir.  
2. Sempre que você adiciona um novo produto, ele é gravado na tabela `products`.  
3. A cada nova coleta de preço (via scraping), o valor é atualizado e uma nova linha é inserida na tabela `price_history`.  
4. Isso permite ver **como o preço evolui com o tempo** e facilita futuras análises — como calcular médias e identificar promoções reais.

---

## 🧠 Boas Práticas
Para quem for continuar o desenvolvimento:
- **Centralize tudo no módulo `database.py`** — nunca acesse o banco diretamente de outras partes do código.  
- **Evite duplicar produtos**: a URL é única para cada item.  
- **Não apague históricos**: eles serão usados depois para calcular médias e tendências.  
- **Use testes automatizados (`pytest`)** para validar se o banco está funcionando corretamente.  
- **Prepare-se para crescer**: o código foi feito de forma genérica para, no futuro, migrar facilmente de SQLite para PostgreSQL.  

---

## ✅ O que você tem agora
- Um **banco de dados funcional**, criado automaticamente.  
- Operações de CRUD (criar, ler, atualizar e deletar) testadas.  
- Um sistema capaz de **registrar e lembrar** o que está monitorando.  

---
# PriceWatcher
Aplicação de rastreamento de preços e promoções

### Pré-requisitos
- Python 3.8+
- pip
- make (opcional, para usar o Makefile)

## 🚀 Setup

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/pricewatcher.git
   cd pricewatcher
   ```

2. Crie ambiente virtual:
   ```bash
   make install
   ```
   OU crie manualmente com:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure variáveis:
   ```bash
   cp .env.example .env
   # Edite com suas próprias informações
   ```

4. Rode a aplicação com:
   ```bash
   make run
   ```
   OU manualmente com:
   ```bash
   python main.py
   ```

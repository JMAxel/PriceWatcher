.PHONY: help install run clean lint test venv

# ============================================================================
# TARGETS DE AJUDA
# ============================================================================
help:
	@echo "Comandos disponíveis:"
	@echo "  make venv       - Criar ambiente virtual"
	@echo "  make install    - Instalar dependências"
	@echo "  make run        - Executar a aplicação"
	@echo "  make clean      - Remover arquivos temporários"

# ============================================================================
# TARGETS DE AMBIENTE
# ============================================================================
venv:
	python -m venv .venv
	@echo "Ambiente virtual criado. Ative com: source .venv/bin/activate"

install: venv
	.venv/bin/pip install -r requirements.txt

# ============================================================================
# TARGETS DE EXECUÇÃO
# ============================================================================
run:
	python main.py

# ============================================================================
# TARGETS DE LIMPEZA E TESTES
# ============================================================================
clean:
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@echo "Arquivos temporários removidos!"

.DEFAULT_GOAL := help
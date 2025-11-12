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
	@echo "  make test_env   - Executar testes da env"
	@echo "  make test_db    - Executar testes do banco de dados"

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
# TARGETS DE LIMPEZA
# ============================================================================
clean:
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@echo "Arquivos temporários removidos!"

# ============================================================================
# TARGETS DE TESTE
# ============================================================================
test_env:
	pytest tests/test_env.py

test_db:
    PYTHONPATH=. python3 scripts/test_db.py

.DEFAULT_GOAL := help
.PHONY: setup test lint demo clean

setup:
	cd .. && python scripts/sync_licenses.py
	pip install -e ../aec-schema
	pip install -e ".[dev]"

test:
	python -m pytest tests/ -v

lint:
	ruff check src/ tests/

demo:
	python scripts/demo.py

clean:
	rm -rf __pycache__ src/framing_synth/__pycache__ tests/__pycache__ \
	       .pytest_cache .ruff_cache *.egg-info src/*.egg-info

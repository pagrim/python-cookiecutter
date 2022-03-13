.PHONY: $(MAKECMDGOALS)

test:
	export PYTHONPATH="./src:./test" && pytest test

environment:
	ifeq(, $(wildcard .venv))
		python3 -m venv .venv
	endif
	.venv/bin/pip install -r requirements-dev.txt

build:
	pip install .

targetenvs := python3.7 python3.8 python3.9 3.10
repositories := {{ cookiecutter.pypirc_repositories }}
docker_test_image := quay.io/pypa/manylinux2014_x86_64:latest

.PHONY: clean clean-test clean-pyc clean-build clean-docs test test-all dist install install-develop publish-locally update help publish install-devreqs
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-docs ## remove all build, test, and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -path ./lib -prune -false -o -name '*.egg-info' -exec rm -fr {} +
	find . -path ./lib -prune -false -o -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -path ./lib -prune -false -o -name '*.pyc' -exec rm -f {} +recursive-include docs *.rst *.md conf.py Makefile *.jpg *.png *.gif *.txt
	find . -path ./lib -prune -false -o -name '*.pyo' -exec rm -f {} +
	find . -path ./lib -prune -false -o -name '*~' -exec rm -f {} +
	find . -path ./lib -prune -false -o -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test artifacts
	rm -fr .tox/
	rm -fr .pytest_cache

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox in docker container
	docker pull ${docker_test_image}
	docker run --rm -v ${current_dir}:/project ${docker_test_image} make -C /project test-all-locally

test-all-locally: install-devreqs ## run tests on every Python version with tox
	python3.8 -m pip install tox; \
	python3.8 -m tox

dist: clean install-devreqs ## builds source and wheel package for {{ cookiecutter.project_slug }}
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: ## install the package to the active Python's site-packages
	pip install .

install-develop: install-devreqs ## Install {{ cookiecutter.project_slug }} python code in develop mode
	pip uninstall {{ cookiecutter.project_slug }}
	pip install -e .

publish: install-devreqs ## builds source and wheel package within docker container and publishes to nexus
	docker pull ${docker_test_image}
	docker run --rm -v ${current_dir}:/project -v ${HOME}/.pypirc:/root/.pypirc:ro ${docker_test_image} make -C /project publish-locally

publish-locally: ## builds source and wheel package locally and publishes to nexus
	for pythonenv in $(targetenvs) ; do \
		$(MAKE) clean; \
		$$pythonenv -m pip install twine; \
		$$pythonenv setup.py bdist_wheel; \
		$$pythonenv -m twine check dist/*; \
		for repository in $(repositories) ; do \
			$$pythonenv -m twine upload -r $${repository} dist/*; \
		done \
	done

update: ## install the package without dependencies
	pip install --upgrade --no-deps .

install-devreqs: ## Install development requirements
	pip install -r requirements_dev.txt

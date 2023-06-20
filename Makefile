# defaults
.DEFAULT_GOAL := help

# Use bash not sh
SHELL := /bin/bash



.PHONY: help
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@echo "usage: make [target] ..."
	@echo ""
	@echo "Targets for '$(notdir $(CURDIR))':"
	@echo ""
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""


.PHONY: devenv

.venv:
	@python3 --version
	python3 -m venv $@
	## upgrading tools to latest version in $(shell python3 --version)
	$@/bin/pip3 --quiet install --upgrade \
		pip~=23.1 \
		wheel \
		setuptools
	@$@/bin/pip3 list --verbose

devenv: .venv ## create a development environment (configs, virtual-env, hooks, ...)
	@.venv/bin/pip install --upgrade  pre-commit
	# Installing pre-commit hooks in current .git repo
	@.venv/bin/pre-commit install
	@echo "To activate the venv, execute 'source .venv/bin/activate'"

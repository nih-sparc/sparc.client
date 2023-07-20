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


.venv:
	@python3 --version
	python3 -m venv $@
	## upgrading tools to latest version in $(shell python3 --version)
	$@/bin/pip3 --quiet install --upgrade \
		pip~=23.1 \
		wheel \
		setuptools
	@$@/bin/pip3 list --verbose


.PHONY: devenv
devenv: .venv ## create a development environment (configs, virtual-env, hooks, ...)
	@.venv/bin/pip install --upgrade  pre-commit
	# Installing pre-commit hooks in current .git repo
	@.venv/bin/pre-commit install
	@echo "To activate the venv, execute 'source .venv/bin/activate'"


.PHONY: install-dev
install-dev: ## installs package in editable mode
	pip install --editable '.[test]'


.PHONY: test-dev
test-dev: ## runs tests
	pytest \
		--cov=./src \
		-vv \
		--pdb \
		--cov-append \
		--cov-report=term-missing \
		--cov-report=xml \
		tests/


.PHONY: clean clean-venv clean-hooks

_git_clean_args := -dx --force \
	--exclude=.vscode \
	--exclude=.venv \
	--exclude=.python-version \
	--exclude="*keep*"

.check-clean:
	@git clean -n $(_git_clean_args)
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	@echo -n "$(shell whoami), are you REALLY sure? [y/N] " && read ans && [ $${ans:-N} = y ]

clean-venv: ## Removes .venv into original configuration
	# Cleaning your venv
	-rm -rf .venv

clean-hooks: ## Uninstalls git pre-commit hooks
	@-pre-commit uninstall 2> /dev/null || rm .git/hooks/pre-commit

clean: .check-clean ## cleans all unversioned files in project and temp files create by this makefile
	# Cleaning unversioned
	@git clean $(_git_clean_args)

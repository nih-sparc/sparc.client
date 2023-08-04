@echo off

@REM Auto generated with https://github.com/espositoandrea/Make-to-Batch


IF /I "%1"==".DEFAULT_GOAL " GOTO .DEFAULT_GOAL
IF /I "%1"=="SHELL " GOTO SHELL
IF /I "%1"=="help" GOTO help
IF /I "%1"==".venv" GOTO .venv
IF /I "%1"=="devenv" GOTO devenv
IF /I "%1"=="install-dev" GOTO install-dev
IF /I "%1"=="test-dev" GOTO test-dev
IF /I "%1"=="_git_clean_args " GOTO _git_clean_args
IF /I "%1"==".check-clean" GOTO .check-clean
IF /I "%1"=="clean-venv" GOTO clean-venv
IF /I "%1"=="clean-hooks" GOTO clean-hooks
IF /I "%1"=="clean" GOTO clean
GOTO error

:.DEFAULT_GOAL
	CALL make.bat =
	CALL make.bat help
	GOTO :EOF

:SHELL
	CALL make.bat =
	CALL make.bat /bin/bash
	GOTO :EOF

:help
	@echo "usage: make [target] ..."
	@echo ""
	@echo "Targets for '%notdir $(CURDIR%)':"
	@echo ""
	@awk --posix 'BEGIN {FS = ":.*?
	@echo ""
	GOTO :EOF

:.venv
	@python3 --version
	python3 -m venv $@

	$@/bin/pip3 --quiet install --upgrade pip~=23.1 wheel setuptools
	@$@/bin/pip3 list --verbose
	GOTO :EOF

:devenv
	CALL make.bat .venv
	@.venv/bin/pip install --upgrade  pre-commit

	@.venv/bin/pre-commit install
	@echo "To activate the venv, execute 'source .venv/bin/activate'"
	GOTO :EOF

:install-dev
	pip install --editable '.[test]'
	GOTO :EOF

:test-dev
	pytest --cov=./src -vv --pdb tests/
	GOTO :EOF

:_git_clean_args
	CALL make.bat =
	CALL make.bat -dx
	CALL make.bat --force
	CALL make.bat --exclude=.vscode
	CALL make.bat --exclude=.venv
	CALL make.bat --exclude=.python-version
	CALL make.bat --exclude="*keep*"
	GOTO :EOF

:.check-clean
	@git clean -n %_git_clean_args%
	@echo -n "Are you sure? [y/N] " && read ans && [ $%ans:-N% = y ]
	@echo -n "%shell whoami%, are you REALLY sure? [y/N] " && read ans && [ $%ans:-N% = y ]
	GOTO :EOF

:clean-venv
	-rm -rf .venv
	GOTO :EOF

:clean-hooks
	@-pre-commit uninstall 2> /dev/null || rm .git/hooks/pre-commit
	GOTO :EOF

:clean
	CALL make.bat .check-clean
	@git clean %_git_clean_args%
	GOTO :EOF

:error
    IF "%1"=="" (
        ECHO make: *** No targets specified and no makefile found.  Stop.
    ) ELSE (
        ECHO make: *** No rule to make target '%1%'. Stop.
    )
    GOTO :EOF

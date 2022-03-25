# Makefile related to requirements
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────

SHELL := bash

MK_FILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
ROOT_PATH := $(realpath $(dir $(MK_FILE_PATH)))

SETUP_PATH = $(ROOT_PATH)/setup
SETUP_CONF_PATH = $(SETUP_PATH)/style_conf

DEPLOY_PATH = $(ROOT_PATH)/deploy

SRC_PATH = $(ROOT_PATH)/src

TESTS_PATH = $(ROOT_PATH)/tests
INI_PATH = $(TESTS_PATH)/pytest.ini

# --------------------------------------------------------------------------------------------------------------------
# --- OPTIONS
# --------------------------------------------------------------------------------------------------------------------

.PHONY: clean-pyc clean-build docs

help: ## This help.
	@echo " Usage: make <task>"
	@echo "   task options:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "	\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: clean-pyc ## Remove junk files.

clean-pyc: ## Remove Python file artifacts.
	@find $(ROOT_PATH) -name '*.pyc' -exec rm -f {} +
	@find $(ROOT_PATH) -name '*.pyo' -exec rm -f {} +
	@find $(ROOT_PATH) -name '*~' -exec rm -f {} +

req-install-dev: ## Install only development requirements in the activated local environment
	@make -f $(SETUP_PATH)/Makefile install-req-dev

req-install: ## Install the required libraries.
	@make -f $(SETUP_PATH)/Makefile install-req

req-remove: ## Uninstall all the libraries installed in the Python environment.
	@make -f $(SETUP_PATH)/Makefile remove-req

req-clean: ## Remove all items from the pip cache.
	@make -f $(SETUP_PATH)/Makefile cache-purge

lint: ## Check style with flake8 and pylint.
	@echo ""
	@echo "────────────────────────────────────────────────────────────────────────────────────────────────────────────"
	@echo "─── Checking the project code style [flake8]"
	@echo "────────────────────────────────────────────────────────────────────────────────────────────────────────────"
	@flake8 --config=$(SETUP_CONF_PATH)/.flake8 src tests

	@echo ""
	@echo "────────────────────────────────────────────────────────────────────────────────────────────────────────────"
	@echo "─── Checking the project code style [pylint]"
	@echo "────────────────────────────────────────────────────────────────────────────────────────────────────────────"
	@pylint --rcfile=$(SETUP_CONF_PATH)/.pylintrc src tests

test: ## Run tests quickly with the default Python.
	@cd $(TESTS_PATH) && PYTHONPATH=$(SRC_PATH) pytest -c $(INI_PATH) -rfs $(TESTS_PATH) || true
	@find $(ROOT_PATH) -name '.pytest_cache' -exec rm -rf {} +
	@find $(ROOT_PATH) -name '.coverage*' ! -name ".coveragerc" -exec rm -rf {} +

app-build: ## Build the docker image.
	@make -f $(DEPLOY_PATH)/Makefile app-build

app-config-dev: ## Prints the resolved development application config to the terminal.
	@make -f $(DEPLOY_PATH)/Makefile app-config ENV=dev

app-deploy-dev: ## Deploy the development services.
	@make -f $(DEPLOY_PATH)/Makefile app-deploy ENV=dev

app-stop-dev: ## Stops running development containers without removing them.
	@make -f $(DEPLOY_PATH)/Makefile app-stop ENV=dev

app-down-dev: ## Bring everything of development environment down, removing the containers entirely and the data volumes.
	@make -f $(DEPLOY_PATH)/Makefile app-down ENV=dev

app-config-prod: ## Prints the resolved production application config to the terminal.
	@make -f $(DEPLOY_PATH)/Makefile app-config ENV=prod

app-deploy-prod: ## Deploy the production services.
	@make -f $(DEPLOY_PATH)/Makefile app-deploy ENV=prod

app-stop-prod: ## Stops running production containers without removing them.
	@make -f $(DEPLOY_PATH)/Makefile app-stop ENV=prod

app-down-prod: ## Bring everything of production environment down, removing the containers entirely and the data volumes.
	@make -f $(DEPLOY_PATH)/Makefile app-down ENV=prod


.DEFAULT_GOAL := help
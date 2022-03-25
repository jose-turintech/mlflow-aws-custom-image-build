# Makefile related to requirements
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
SHELL := bash

# --------------------------------------------------------------------------------------------------------------------
# --- REQUIREMENTS
# --------------------------------------------------------------------------------------------------------------------

MK_FILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
SETUP_PATH := $(realpath $(dir $(MK_FILE_PATH)))

REQ_FILES = requirements.txt requirements_develop.txt

REQ_DIST=

REQ_FREEZE = $(SETUP_PATH)/requirements_freeze.txt

# --------------------------------------------------------------------------------------------------------------------
# --- OPTIONS
# --------------------------------------------------------------------------------------------------------------------

# HELP. This will output the help for each task
.PHONY: help

help: ## This help.
	@echo " Usage: make <task>"
	@echo "   task options:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "	\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install-req-dev: ## Install only develop requirements in the activated local environment
	@echo "──────────────────────────────────────────────────────────────────────────────────────────────────────────"
	@echo "─── Install requirements: $(REQ_FILES) $(REQ_DIST)"
	@echo "──────────────────────────────────────────────────────────────────────────────────────────────────────────"
	@pip install -U -r $(SETUP_PATH)/requirements_develop.txt || (echo "install failed $?")
	pip freeze > $(REQ_FREEZE)

install-req: ## Install requirements in the activated local environment
	@echo "──────────────────────────────────────────────────────────────────────────────────────────────────────────"
	@echo "─── Install requirements: $(REQ_FILES) $(REQ_DIST)"
	@echo "──────────────────────────────────────────────────────────────────────────────────────────────────────────"
	@$(foreach var,$(REQ_FILES),pip install -U -r $(SETUP_PATH)/$(var) || (echo "install failed $?");)
	@$(foreach var,$(REQ_DIST),pip install -U -r $(SETUP_PATH)/$(var) || (echo "install failed $?");)
	pip freeze > $(REQ_FREEZE)

remove-req:  ## Remove all installed requirements in the activated local environment
	@echo "──────────────────────────────────────────────────────────────────────────────────────────────────────────"
	@echo "─── Delete all previously installed libraries: $(REQ_FILES) $(REQ_DIST)"
	@echo "──────────────────────────────────────────────────────────────────────────────────────────────────────────"
	@$(foreach var,$(REQ_FILES),pip uninstall -r $(SETUP_PATH)/$(var) -y || (echo "uninstall failed $?");)
	@$(foreach var,$(REQ_DIST),pip uninstall $(SETUP_PATH)/$(var) -y || (echo "uninstall failed $?");)
	@pip freeze | awk '{print $$1}' | xargs pip uninstall -y || (echo "uninstall failed $?")
	pip freeze > $(REQ_FREEZE)

cache-purge:  ## Remove all items from the pip cache.
	@echo "──────────────────────────────────────────────────────────────────────────────────────────────────────────"
	@echo "─── Remove all items from the pip cache."
	@echo "──────────────────────────────────────────────────────────────────────────────────────────────────────────"
	@pip cache purge


.DEFAULT_GOAL := help

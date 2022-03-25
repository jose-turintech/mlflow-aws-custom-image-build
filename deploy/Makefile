# Makefile related to deployment
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
SHELL := bash

# --------------------------------------------------------------------------------------------------------------------
# --- PATHS
# --------------------------------------------------------------------------------------------------------------------

MK_FILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
DEPLOY_PATH := $(realpath $(dir $(MK_FILE_PATH)))
SCRIPTS_PATH := $(DEPLOY_PATH)/scripts
ENVIRONMENTS_PATH := $(DEPLOY_PATH)/environments

DEPLOY_FILE := $(DEPLOY_PATH)/docker-compose.yml

LOCAL_NETRC_PATH ?= ~/.netrc
LOCAL_PIP_CONF_PATH ?= ~/.config/pip/pip.conf

DEPLOY_NETRC_PATH ?= $(DEPLOY_PATH)/pip_conf/.netrc
DEPLOY_PIP_CONF_PATH ?= $(DEPLOY_PATH)/pip_conf/pip.conf

BUILD_KIT_PARAMS := DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 BUILDKIT_PROGRESS=plain


# --------------------------------------------------------------------------------------------------------------------
# --- CONFIGURATION
# --------------------------------------------------------------------------------------------------------------------

# Get all available environments and verify that the specified environment matches any of them
ENV_LIST := $(shell ls -l $(ENVIRONMENTS_PATH) | grep '^d' | awk '{print $$9}')
ENV_PATH := $(if $(filter $(strip $(ENV)),$(ENV_LIST)),$(ENVIRONMENTS_PATH)/$(strip $(ENV)),)

# ────────────────

# import Global config. You can change the default config with 'make CNF="envPath/anotherGlobal.env" <docker task>'
CNF ?= $(DEPLOY_PATH)/.env
include $(CNF)
export $(shell sed 's/=.*//' $(CNF))

# ────────────────

# import Environment config. You can change the default config with 'make CNF_ENV="envPath/.env" <docker task>'
CNF_ENV ?= $(if $(ENV_PATH),$(ENV_PATH)/.env,)
DEPLOY_ENV_FILE := $(if $(ENV_PATH),-f $(ENV_PATH)/docker-compose.yml,)
ifneq ($(CNF_ENV),)
	include $(CNF_ENV)
	export $(shell sed 's/=.*//' $(CNF_ENV))
endif

ACTIVE_ENV=source $(SCRIPTS_PATH)/env_files.sh

# --------------------------------------------------------------------------------------------------------------------
# --- OPTIONS
# --------------------------------------------------------------------------------------------------------------------

# HELP. This will output the help for each task
.PHONY: help

help: ## This help.
	@echo " Usage: make [ENV=<$(ENV_LIST)>] [CNF=globalEnvFile] [CNF_ENV=environmentEnvFile]  <task>"
	@echo "   task options:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "	\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

show:
	@echo ""
	@echo "MK_FILE_PATH      : $(MK_FILE_PATH)"
	@echo "DEPLOY_PATH       : $(DEPLOY_PATH)"
	@echo "ENVIRONMENTS_PATH : $(ENVIRONMENTS_PATH)"
	@echo "ENV_LIST          : $(ENV_LIST)"
	@echo "ENV               : $(ENV)"
	@echo "CNF               : $(CNF)"
	@echo "ENV_PATH          : $(ENV_PATH)"
	@echo "CNF_ENV           : $(CNF_ENV)"
	@echo "DEPLOY_FILE       : $(DEPLOY_FILE)"
	@echo ""

app-config: ## Prints the resolved application config to the terminal. >>> USE: make app-config [ENV=envName]
	@cp $(CNF) $(DEPLOY_PATH)/.env.bck || true
	@$(ACTIVE_ENV) && load_env_file "$(CNF)" && load_env_file "$(CNF_ENV)" && save_env_file "$(CNF)"
	@docker-compose -f $(DEPLOY_FILE) $(DEPLOY_ENV_FILE) config || true
	@rm $(CNF) && mv $(DEPLOY_PATH)/.env.bck $(CNF) || true

app-build: ## Build the docker image. >>> USE: make app-build [ENV=envName]
	@$(BUILD_KIT_PARAMS) docker-compose -f $(DEPLOY_FILE) $(DEPLOY_ENV_FILE) build --no-rm

app-build-nc: ## Build the images without caching. >>> USE: make app-build-nc [ENV=envName]
	@$(BUILD_KIT_PARAMS) docker-compose -f $(DEPLOY_FILE) $(DEPLOY_ENV_FILE) build --no-cache

app-deploy: ## Deploy the services
	@docker-compose -f $(DEPLOY_FILE) $(DEPLOY_ENV_FILE) --project-name=$(APP_ID) up -d
	@echo -e "\nYou can see the log traces by running the following command:"
	@echo -e "\t$ docker logs --tail 100 -f $(APP_ID)"
	@echo -e "\nYou can access to the docker container by running the following command:"
	@echo -e "\t$ docker exec -it $(APP_ID) bash"
	@echo ""

app-stop: ## Stops running containers without removing them. >>> USE: make app-stop ENV=envName
	@docker-compose -f $(DEPLOY_FILE) $(DEPLOY_ENV_FILE) --project-name=$(APP_ID) stop

app-down: ## Bring everything down, removing the containers entirely and the data volumes. >>> USE: make app-down ENV=envName
	@docker-compose -f $(DEPLOY_FILE) $(DEPLOY_ENV_FILE) --project-name=$(APP_ID) down --volumes

app-restart: ## Stop running containers and Spin up again the project. >>> USE: make app-restart ENV=envName
	@make -s stop
	@make -s deploy

replace-pip-conf: ## Replaces the current PyPI configuration with the one found in the deployment machine
	@[ -f $(LOCAL_NETRC_PATH) ] && cp $(LOCAL_NETRC_PATH) $(DEPLOY_NETRC_PATH) && \
		echo "Updated the '$(DEPLOY_NETRC_PATH)' file with the content of the '$(LOCAL_NETRC_PATH)' file" || true
	@[ -f $(LOCAL_PIP_CONF_PATH) ] && cp $(LOCAL_PIP_CONF_PATH) $(DEPLOY_PIP_CONF_PATH) && \
		echo "Updated the '$(DEPLOY_PIP_CONF_PATH)' file with the content of the '$(LOCAL_PIP_CONF_PATH)' file" || true


.DEFAULT_GOAL := help

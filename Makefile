.DEFAULT_GOAL := help
.PHONY: venv
.EXPORT_ALL_VARIABLES:
.DEFAULT_GOAL := help
.PHONY: venv
.EXPORT_ALL_VARIABLES:

## APP VARS ##
PRODUCT_NAME    = booklibray
SERVICE_NAME    = python
DOMAIN          ?= services.peru.com
ELB_NAME        ?= peru-com-dev-alb
VPC_ID          ?= vpc-00a577092869e91c7
CLUSTER         ?= peru-com-dev

## GENERAL VARS ##
ENV            ?= dev
INFRA_BUCKET   ?= perucom.infrastructure.$(ENV)
PROJECT_NAME    = $(PRODUCT_NAME)-$(ENV)-$(SERVICE_NAME)
APP_DIR         = app
VERSION         = v1
PATH_SERVICE    = /$(VERSION)/$(SERVICE_NAME)
NETWORK         = perucom_network

## INCLUDE TARGETS ##
include makefiles/container.mk
include makefiles/deploy.mk
include makefiles/help.mk
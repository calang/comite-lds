# Description

# variable definitions, available to all rules
REPO_ROOT := $(shell git rev-parse --show-toplevel)  # root directory of this git repo
BRANCH := $(shell git branch --show-current)
# BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
# Notes:
# all env variables are available
# = uses recursive substitution
# :=  uses immediate substitution

# ENV_NAME is second word, separated by one space, in file env.yml (conda only)
ENV_NAME := $(if $(wildcard env.yml),$(shell head -1 env.yml | cut -d ' ' -f 2),)

# Enable GPU support for TensorFlow and PyTorch
# CUDA_DIR uses the active conda environment prefix

TF_SETENV := :

# xor

# CUDA_DIR := ${CONDA_PREFIX}
# XLA_FLAGS := --xla_gpu_cuda_data_dir=${CUDA_DIR}
# LD_LIBRARY_PATH := ${CUDA_DIR}/lib:${LD_LIBRARY_PATH}
# TF_ENABLE_ONEDNN_OPTS := 0
# TF_SETENV := export CUDA_DIR=${CUDA_DIR} XLA_FLAGS="${XLA_FLAGS}" LD_LIBRARY_PATH="${LD_LIBRARY_PATH}" TF_ENABLE_ONEDNN_OPTS=${TF_ENABLE_ONEDNN_OPTS}


# target: help - Display callable targets.
help:
	@echo "Usage:  make <target>"
	@echo "  where <target> may be"
	@echo
	@egrep -h "^# target:" [Mm]akefile | sed -e 's/^# target: //'

# target: show-vars - show defined variables
show-vars:
	@echo "REPO_ROOT=${REPO_ROOT}"
	@echo "BRANCH=${BRANCH}"
	@echo "ENV_NAME=${ENV_NAME}"
	@echo "CUDA_DIR=${CUDA_DIR}"
	@echo "XLA_FLAGS=${XLA_FLAGS}"
	@echo "LD_LIBRARY_PATH=${LD_LIBRARY_PATH}"
	@echo "TF_ENABLE_ONEDNN_OPTS=${TF_ENABLE_ONEDNN_OPTS}"
	@echo "TF_SETENV=${TF_SETENV}"

# target: init - first-time project setup. Usage: make init
init:
	if [ ! -f .env ]; then cp .env_template .env; fi
	uv sync
	uv sync --group dev
	rm -f env.yml requirements.txt

# target: update-env - update environment
update-env:
	uv sync

# target: rm-env - remove environment
rm-env:
	rm -rf .venv


# ============================================================
# Utilities
# ============================================================

# target: lint - run pylint with docparams plugin to check for missing docstring parameters
lint:
	pylint --load-plugins=pylint.extensions.docparams scripts src

# target: jupl - start jupyter lab server
jupl:	ALWAYS
	uv run jupyter lab &


# target push - sample docker image push, asking for passwords
# push: TEMPUSR := $(shell mktemp)
# push:
#	@$$SHELL -i -c 'read -p "username: " user;  echo -n $${user} >$(TEMPUSR)'
#	@$$SHELL -i -c 'read -s -p "password: " user;  echo -n $${user} >$(TEMPUSR)1'
#	@docker login -u $$(cat $(TEMPUSR)) -p $$(cat $(TEMPUSR)1) amr-registry.caas.intel.com
#	docker image push ${APP_IMAGE}
#	@rm $(TEMPUSR)*

# ignore files with any of these names
# so that the rules with those as target are always executed
.PHONY: help show-vars init update-env rm-env lint jupl ALWAYS

# always do/refresh ALWAYS target
ALWAYS:

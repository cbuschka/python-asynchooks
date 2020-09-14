TOP_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
VENV_DIR := ${TOP_DIR}/venv/
SHELL := /bin/bash

tests:	init_venv
	@cd ${TOP_DIR} && \
	source ${VENV_DIR}/bin/activate && \
	python3 -B -m unittest discover tests

init_venv:
	@cd ${TOP_DIR} && \
	if [ ! -d "${VENV_DIR}" ]; then \
		echo "Creating virtualenv..." && \
		virtualenv ${VENV_DIR} -p $(shell which python3.8); \
	fi


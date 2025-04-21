SHELL := /bin/bash
PYTHON := python3
PIP := $(PYTHON) -m pip

.PHONY: help install run

help:
	@echo "Available commands:"
	@echo "  make install    Install dependencies"
	@echo "  make run        Run the Discord bot"

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) main.py
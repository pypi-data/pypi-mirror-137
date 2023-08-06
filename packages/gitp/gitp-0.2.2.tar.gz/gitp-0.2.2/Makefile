.PHONY: build chmod install test

SHELL := $(shell command -v bash)

build: chmod
	@sudo python3 -m build  -o $$(mktemp -d)

chmod:
	@chmod -R +x bin/* 2>/dev/null || true

install:
	@sudo python3 -m pip --quiet uninstall $$(basename "$PWD")
	@sudo python3 -m pip --quiet install --upgrade --no-cache $$(basename "$PWD")

test:
	@pytest

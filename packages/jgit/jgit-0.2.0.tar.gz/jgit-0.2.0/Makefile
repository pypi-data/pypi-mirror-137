.PHONY: build

SHELL := $(shell command -v bash)
tmp_build := $(shell mktemp -d)

build: chmod
	@python3 -m build  -o $(tmp_build)

chmod:
	@chmod -R +x bin/*

test:
	@pytest

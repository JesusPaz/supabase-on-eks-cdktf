SHELL := /bin/bash

.PHONY: bootstrap synth plan deploy destroy provider-list provider-upgrade

bootstrap:
	python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && cdktf get

synth:
	source .venv/bin/activate && cdktf synth | cat

plan:
	source .venv/bin/activate && cdktf plan | cat

deploy:
	source .venv/bin/activate && cdktf deploy --auto-approve | cat

destroy:
	source .venv/bin/activate && cdktf destroy --auto-approve | cat

provider-list:
	source .venv/bin/activate && cdktf provider list | cat

provider-upgrade:
	source .venv/bin/activate && cdktf provider upgrade $(PROVIDER) | cat
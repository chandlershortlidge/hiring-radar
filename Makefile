# Short names for the long commands. Run `make` to list them.
# Ops runbook: deploy/README.md

ZONE := europe-west3-a
VM   := hiring-radar

.DEFAULT_GOAL := help
.PHONY: help ssh

help: ## List the available commands
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-8s %s\n", $$1, $$2}'

ssh: ## Open a shell on the hiring-radar VM
	gcloud compute ssh $(VM) --zone $(ZONE)

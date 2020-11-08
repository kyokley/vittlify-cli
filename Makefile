help: ## This help
	@grep -F "##" $(MAKEFILE_LIST) | grep -vF '@grep -F "##" $$(MAKEFILE_LIST)' | sed -E 's/(:).*##/\1/' | sort

list: ## List all targets
	@make -qp | awk -F':' '/^[a-zA-Z0-9][^$$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print A[i]}'

build: ## Build container
	docker build -t kyokley/vt --target=prod .

build-dev: ## Build container
	docker build -t kyokley/vt --target=dev .

publish: build ## Build and push container to DockerHub
	docker push kyokley/vt

test: build-dev ## Run tests
	docker run --rm -it -v $$(pwd):/app --entrypoint poetry kyokley/vt run pytest

shell: build-dev ## Open a shell inside container
	docker run --rm -it -v $$(pwd):/app --entrypoint /bin/sh kyokley/vt

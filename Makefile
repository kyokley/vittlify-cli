NO_CACHE?=0

help: ## This help
	@grep -F "##" $(MAKEFILE_LIST) | grep -vF '@grep -F "##" $$(MAKEFILE_LIST)' | sed -E 's/(:).*##/\1/' | sort

list: ## List all targets
	@make -qp | awk -F':' '/^[a-zA-Z0-9][^$$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print A[i]}'

build: ## Build container
ifeq ($(NO_CACHE), 1)
	docker build --no-cache -t kyokley/vt --target=prod .
else
	docker build -t kyokley/vt --target=prod .
endif

build-dev: ## Build container
ifeq ($(NO_CACHE), 1)
	docker build --no-cache -t kyokley/vt --target=dev .
else
	docker build -t kyokley/vt --target=dev .
endif

publish: build ## Build and push container to DockerHub
	docker push kyokley/vt

tests: build-dev ## Run tests
	docker run --rm -it -v $$(pwd):/app --entrypoint pytest kyokley/vt

shell: build-dev ## Open a shell inside container
	docker run --rm -it -v $$(pwd):/app --entrypoint /bin/sh kyokley/vt

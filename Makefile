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
	docker run --rm -t -v $$(pwd):/app --entrypoint pytest kyokley/vt

check-formatting: build-dev
	docker run --rm -t -v $$(pwd):/app --entrypoint /bin/sh kyokley/vt -c " \
	git ls-files | grep -E '\.py$$' | xargs black -S --check && \
	git ls-files | grep -E '\.py$$' | xargs flake8 --select F821,F401 \
	"

autoformat: build-dev
	docker run --rm -t -v $$(pwd):/app --entrypoint /bin/sh kyokley/vt -c " \
	git ls-files | grep -E '\.py$$' | xargs isort -m 3 -tc && \
	git ls-files | grep -E '\.py$$' | xargs black -S \
	"

shell: build-dev ## Open a shell inside container
	docker run --rm -it -v $$(pwd):/app --entrypoint /bin/sh kyokley/vt

## CONTAINER VARS ##
USERNAME_LOCAL      ?= "$(shell whoami)"
UID_LOCAL           ?= "$(shell id -u)"
GID_LOCAL           ?= "$(shell id -g)"
CONTAINER_NAME      = $(PROJECT_NAME)_backend
IMAGE_BUILD         = node:11-slim
APP_DIR             = app
IMAGE_BUILD_LOCAL   = $(IMAGE_DEPLOY)
NETWORK             = perucom_network


container-up: ##@Local Start the project
	docker-compose up

container-start:
	docker run -it -p 9000:9000 --name $(CONTAINER_NAME) -e PORT=9000 -e BUILD_ENV='development' -e DATABASE_URL='mysql+pymysql://user:pass@host:port/dbname' $(IMAGE_BUILD_LOCAL)

container-down: ##@Local Destroy the project
	@docker-compose -p $(PROJECT_NAME) down

container-log: ##@Local Show project logs
	@docker logs -f $(CONTAINER_NAME)

container-ssh: ##@Local Access the docker container
	@docker container run -it --rm \
	-u ${UID_LOCAL}:${GID_LOCAL} \
	-v "${PWD}/${APP_DIR}":/usr/src/app \
	$(IMAGE_BUILD_LOCAL) bash

container-remove: ##@Local remove container
	@docker-compose rm -v

install-lib: ## Connect to container for ssh protocol install with pip: make install-lib
	docker exec -it $(CONTAINER_NAME) pip install $(LIB)

build: ## construccion de la imagen: make build IMAGE_DEPLOY=IMAGE_TEST
	cp ./app/requirements.txt ./docker/dev/resources/
	docker build -f docker/dev/Dockerfile -t $(IMAGE_DEPLOY) docker/dev/;

doc: ##@Global Build project
	@docker container run --workdir "/${APP_DIR}" --rm -i \
		-u ${UID_LOCAL}:${GID_LOCAL} \
		-v "${PWD}/${APP_DIR}":/${APP_DIR} \
		-p 8080:8080 \
		${IMAGE_BUILD} \
		yarn doc:serve

development: container-up container-log ##@Local Prepare the project for development
	@echo "The development environment is ready and running"
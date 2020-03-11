## DEPLOY VARS ##
BUILD_NUMBER    ?= 000001
BUILD_TIMESTAMP ?= 1560121554
DEPLOY_REGION   ?= eu-west-1
DESIRED_COUNT   ?= 1
MIN_SCALING     ?= 1
MAX_SCALING     ?= 2
MEMORY_SIZE     ?= 128
AUTOSCALING     ?= false
TAG_DEPLOY      ?= $(BUILD_TIMESTAMP).$(BUILD_NUMBER)
ACCOUNT_ID      = 041923611455
IMAGE_DEPLOY    = $(PROJECT_NAME):$(ENV)
DEPLOY_REGISTRY = ${ACCOUNT_ID}.dkr.ecr.${DEPLOY_REGION}.amazonaws.com
STACK_PATH      = ${INFRA_BUCKET}/build/cloudformation/${PRODUCT_NAME}/${ENV}/${PROJECT_NAME}
CLUSTER         ?= ${PRODUCT_NAME}-${ENV}

deploy-sync-params: ##@Deploy Sync parameters files from S3
	@aws s3 sync s3://$(INFRA_BUCKET)/config/deploy/$(PRODUCT_NAME)/$(ENV)/$(SERVICE_NAME)/ deploy/
	
deploy-sync-cloudformation: ##@Deploy Sync additional cloudformation resources in S3
	aws s3 sync ./cloudformation/stacks s3://$(STACK_PATH)

deploy-sync-task-definition: ##@Deploy Sync task definition
	@cp ./cloudformation/task-definition.json ./cloudformation/deploy-task-definition.json
	@sed -i -e \
		's/PRODUCT_NAME/${PRODUCT_NAME}/g; s/ENV/${ENV}/g; s/SERVICE_NAME/${SERVICE_NAME}/g; s/PROJECT_NAME/${PROJECT_NAME}/g; s/DEPLOY_REGION/${DEPLOY_REGION}/g; s/IMAGE_DEPLOY/${IMAGE_DEPLOY}/g; s/MEMORY_SIZE/${MEMORY_SIZE}/g; s/ACCOUNT_ID/${ACCOUNT_ID}/g' \
		./cloudformation/deploy-task-definition.json
	@cat ./cloudformation/deploy-task-definition.json

build-image: ##@Global Create a Docker image with the dependencies packaged
	@docker build -f docker/deploy/Dockerfile --no-cache -t $(IMAGE_DEPLOY) .

deploy-image: deploy-validate-registry ##@Deploy Push image to aws ECR
	docker tag ${IMAGE_DEPLOY} ${DEPLOY_REGISTRY}/${IMAGE_DEPLOY}
	aws --region ${DEPLOY_REGION} ecr get-login --no-include-email | sh
	docker push ${DEPLOY_REGISTRY}/${IMAGE_DEPLOY}

test: ##@Global Unit test
	@docker container run --workdir "/${APP_DIR}" --rm -i \
		-u ${UID_LOCAL}:${GID_LOCAL} \
		-v "${PWD}/${APP_DIR}":/${APP_DIR} \
		${IMAGE_BUILD} \
		yarn test

test-cov: ##@Global Unit test
	@docker container run --workdir "/${APP_DIR}" --rm -i \
		-u ${UID_LOCAL}:${GID_LOCAL} \
		-v "${PWD}/${APP_DIR}":/${APP_DIR} \
		${IMAGE_BUILD} \
		yarn test:cov
	
unit-test: ##@Global Unit test
	@docker container run --workdir "/${APP_DIR}" --rm -i \
		-u ${UID_LOCAL}:${GID_LOCAL} \
		-v "${PWD}/${APP_DIR}":/${APP_DIR} \
		${IMAGE_BUILD} \
		yarn test --ci --reporters='jest-html-reporters'

deploy-validate-registry: ##@Deploy Create registry in aws ECR service
	$(eval EXIST_REPOSITORY := $(shell aws ecr \
		describe-repositories \
		--repository-name ${PROJECT_NAME} \
		--region $(DEPLOY_REGION) \
		| grep "repositoryName" \
		| sed 's/repositoryName//g'\
		| sed 's/://g'| sed 's/,//g'| sed 's/ //g'| sed 's/"//g'))
	@if [ "${EXIST_REPOSITORY}" != "${PROJECT_NAME}" ]; then \
		$(info "Create repository ${PROJECT_NAME} in the region ${DEPLOY_REGION}...") \
		aws cloudformation deploy \
			--template-file ./cloudformation/registry.yml \
			--stack-name ${PROJECT_NAME}-registry \
			--parameter-overrides \
				ProjectName=$(PROJECT_NAME) \
			--region $(DEPLOY_REGION) \
			--capabilities CAPABILITY_IAM; \
	fi

deploy-update-service: deploy-sync-cloudformation ##@Deploy service with cloudformation
	aws cloudformation deploy \
	--template-file ./cloudformation/master.yml \
	--stack-name ${PROJECT_NAME}-service \
	--parameter-overrides \
		S3Path=${STACK_PATH} \
		DesiredCount=${DESIRED_COUNT} \
		MaxScaling=${MAX_SCALING} \
		MinScaling=${MIN_SCALING} \
		Image=${DEPLOY_REGISTRY}/${IMAGE_DEPLOY} \
		ServiceName=${SERVICE_NAME} \
		Env=${ENV} \
		Owner=${PRODUCT_NAME} \
		ContainerPort=80 \
		MemorySize=${MEMORY_SIZE} \
		Autoscaling=${AUTOSCALING} \
		ElbName=${ELB_NAME} \
		VpcId=${VPC_ID} \
		Domain=${DOMAIN} \
		PathService=${PATH_SERVICE} \
		Cluster=${CLUSTER} \
	--region ${DEPLOY_REGION} \
	--capabilities CAPABILITY_NAMED_IAM
	
deploy-update-ecs: deploy-sync-task-definition ##@Deploy
	aws ecs register-task-definition --cli-input-json file://cloudformation/deploy-task-definition.json --region ${DEPLOY_REGION}
	aws ecs update-service --cluster ${CLUSTER} --service ${PROJECT_NAME} --task-definition ${PROJECT_NAME} --desired-count ${DESIRED_COUNT} --region ${DEPLOY_REGION}
	@rm -r ./cloudformation/deploy-task-definition.json

deploy-rollback: deploy-update-ecs ##@Deploy
	@echo "Rollback sucess!!"

deploy-list-images: ##@Deploy
	@aws ecr describe-images --region ${DEPLOY_REGION} --repository-name ${PROJECT_NAME} --query 'reverse(sort_by(imageDetails,& imagePushedAt))[:5].imageTags[0]' --output text

login-aws: ## Run the end to end Tests
	aws ecr get-login --no-include-email --region $(DEPLOY_REGION) | sh
APP_NAME=cron-service-amazon
PROCESS_TYPE=worker

.PHONY: build local

build:
	@echo "MAKE build ==========================================="
	docker-compose build  

local:
	@echo "MAKE local ==========================================="
	docker-compose up --build

heroku_build:
	@echo "MAKE heroku_build ==========================================="
	heroku container:push $(PROCESS_TYPE) -a $(APP_NAME)

heroku_deploy:
	@echo "MAKE heroku_deploy ==========================================="
	heroku container:release $(PROCESS_TYPE) -a $(APP_NAME)


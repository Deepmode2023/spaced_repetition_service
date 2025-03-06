SHELL=/bin/bash

dev_compose := docker-compose --env-file ./app/config/env
project_path := $(shell pwd)
config_dir := ./app/config
dev_req = $(config_dir)/req/requirements.$*.txt
success := Ready to use

dev:
	$(dev_compose) up -d 

%.build: %.clean
	@echo "Using requirements file: $($*_req)"; \
	$($*_compose) up --build


%.update_env:
	@if [ ! -f "$(config_dir)/.env" ]; then \
		echo "Файл .env не найден. Создаём..."; \
		touch "$(config_dir)/.env"; \
	fi; \
	if grep -q '^REQUIREMENT_FILE=' "$(config_dir)/env"; then \
		if sed --version >/dev/null 2>&1; then \
			sed -i 's|^REQUIREMENT_FILE=.*|REQUIREMENT_FILE=$($*_req)|' "$(config_dir)/env"; \
		else \
			sed -i '' 's|^REQUIREMENT_FILE=.*|REQUIREMENT_FILE=$($*_req)|' "$(config_dir)/env"; \
		fi; \
	else \
		echo "Добавляем REQUIREMENT_FILE=$($*_req)"; \
		printf "\nREQUIREMENT_FILE=%s\n" "$($*_req)" >> "$(config_dir)/env"; \
	fi

%.clean: %.update_env
	@docker-compose down
	@echo Has been cleaned successfull.
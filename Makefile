SHELL=/bin/bash

dev_compose := docker-compose --env-file ./app/config/env
project_path := $(shell pwd)
config_dir := $(project_path)/app/config
req_file_dir := $(config_dir)/req
req_files := $(wildcard $(req_file_dir)/*.txt)
absolute_path_req_file=$(foreach file, $(req_files), $(if $(findstring .$*,$(file)),$(file)))
req_file = $(patsubst $(project_path)%, .%, $(absolute_path_req_file))
success := Ready to use

%.build: %.clean
	@echo "Using requirements file: $(req_file)"; \
	$($*_compose) up --build


%.update_env:
	@if [ ! -f "$(config_dir)/.env" ]; then \
		echo "Файл .env не найден. Создаём..."; \
		touch "$(config_dir)/.env"; \
	fi; \
	if grep -q '^REQUIREMENT_FILE=' "$(config_dir)/env"; then \
		if sed --version >/dev/null 2>&1; then \
			sed -i 's|^REQUIREMENT_FILE=.*|REQUIREMENT_FILE=$(req_file)|' "$(config_dir)/env"; \
		else \
			sed -i '' 's|^REQUIREMENT_FILE=.*|REQUIREMENT_FILE=$(req_file)|' "$(config_dir)/env"; \
		fi; \
	else \
		echo "Добавляем REQUIREMENT_FILE=$(req_file)"; \
		printf "\nREQUIREMENT_FILE=%s\n" "$(req_file)" >> "$(config_dir)/env"; \
	fi

%.clean: %.update_env
	@docker-compose down
	@echo Has been cleaned successfull.
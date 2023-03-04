# инструкция по работе с файлом "Makefile" – https://bytes.usc.edu/cs104/wiki/makefile/

# обновление сборки Docker-контейнера
build:
	docker compose build

# остановка приложения
down:
	docker compose down

# генерация документации
docs-html:
	docker compose run --no-deps --workdir /docs countries-informer-app /bin/bash -c "make html"

# запуск форматирования кода
format:
	docker compose run --no-deps --workdir / countries-informer-app /bin/bash -c "black src docs/source/*.py; isort --profile black src/*.py docs/source/*.py"

# запуск статического анализа кода (выявление ошибок типов и форматирования кода)
lint:
	docker compose run --no-deps --workdir / countries-informer-app /bin/bash -c "pylint --load-plugins pylint_django --load-plugins pylint_django.checkers.migrations --django-settings-module=app.settings src; flake8 src; mypy src; black --check src"

# запуск автоматических тестов
test:
	docker compose run countries-informer-app ./manage.py test
# запуск базы данных
db:
	docker compose up countries-informer-db -d
# запуск приложения
up:
	docker compose up --build -d

# запуск миграций
migrate: db
	docker compose run countries-informer-app python manage.py migrate

# создание миграций
migrations:
	docker compose run countries-informer-app python manage.py makemigrations

# создание админа
superuser:
	docker compose run countries-informer-app python manage.py createsuperuser

# запуск всех функций поддержки качества кода
all: format lint test

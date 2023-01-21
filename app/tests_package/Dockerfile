FROM python:3.10-slim

WORKDIR /apps
# Копируем файл с зависимостями проекта
COPY ["requirements.txt", "."]
# Копируем файл с доп. зависимостями для тестирования
COPY ["tests_package/requirements_test.txt", "."]
# Устанавливаем зависимости проекта
RUN pip install -r requirements.txt
# Устанавливаем зависимости для тестов
RUN pip install -r requirements_test.txt
# Копируем файлы проекта
COPY . .
# Заменяем .env файл на .env с тестовыми параметрами внутри (коннект к тестовой БД)
COPY ["tests_package/.env", "."]
# Перемещаем файл запуска тестов
COPY ["tests_package/run_test.py", "."]
Требования: Docker

1) Клонировать репозиторий
2) Запустить докер: docker-compose up -d
3) Узнать id контейнера web: docker container ls
4) Войти в контейнер: docker exec -it {id контейнера} bash
5) Применить миграции внутри контейнера: alembic upgrade head
6) Можно запускать тесты

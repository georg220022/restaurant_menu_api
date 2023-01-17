Требования: Docker

1) Клонировать репозиторий, перейти в папку с проектом
2) Запустить докер: docker-compose up -d
3) Узнать id контейнера web: docker container ls
4) Войти в контейнер: docker exec -it сюда_id_контейнера bash
5) Применить миграции внутри контейнера: alembic upgrade head

Можно запускать тесты :)
 
 ![Иллюстрация к проекту](https://github.com/georg220022/Google_Sheet/blob/main/1.png)

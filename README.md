#### Требования: Docker  
##### 1) Клонировать репозиторий  
##### 2) Перейти в папку с проектом  
  
##### Запуск тестового контейнера(pytest):  
> docker-compose -f docker-compose-test.yml up  
##### Запуск в обычном режиме, который можно протестировать через тесты POSTMAN из первого задания:  
> docker-compose up  
  
##### [ВАЖНО] После загрузки тестовых данных тесты НЕ ПРОЙДУТ. Перед запуском тестов БД должна быть пустая.  
###### Загрузка тестовых данных:  
> [GET] localhost:8000/api/v1/load_data  
###### Старт задачи генерации файла:  
> [POST] localhost:8000/api/v1/create_xlsx  
> Запрос вернет ссылку с task_id  
###### Проверка статуса задачи:  
> [GET] localhost:8000/api/v1/status/task_id  
> Если задача выполнена вернется статус + ссылка на скичивание  
> Иначе вернется просто статус задачи  
###### Загрузка готового файла:  
> [GET] localhost:8000/api/v1/download/task_id  
  
###### Скриншоты:
![Пройденные постман тесты](https://github.com/georg220022/restaurant_menu_api/blob/main/img/postman.png)
![Пройденные PyTest](https://github.com/georg220022/restaurant_menu_api/blob/main/img/pytest.png)

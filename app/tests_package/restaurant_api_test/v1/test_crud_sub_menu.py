from api.v1.app import app as apps
from fastapi.testclient import TestClient

from .test_crud_menu import DATA as menu_data

client = TestClient(apps)
# Создадим в БД меню, что бы переменная URL была валидна
response_post = client.post('api/v1/menus', json=menu_data)
# Получим id созданного меню
menu_id = response_post.json()['id']

URL = f'/api/v1/menus/{menu_id}/submenus'


DATA = {'title': 'Test title sub menu', 'description': 'Test description sub menu'}
UPDATED_DATA = {
    'title': 'Updated test title sub menu',
    'description': 'Updated test description sub menu',
}


class TestGroupSubMenu:
    async def setup_class(self):
        self.response_sub_menu = client.post(URL, json=DATA)
        self.sub_menu_id = self.response_sub_menu.json()['id']

    async def test_post_sub_menu(self):
        """Тест создания подменю"""
        response = self.response_sub_menu
        # При создании подменю ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()['title'] == DATA['title']
        # Проверка description
        assert response.json()['description'] == DATA['description']
        # id должен быть строкой
        assert type(response.json()['id']) == str
        # При запуске тестов нет блюд
        assert response.json()['dishes_count'] == 0
        # При создании возвращается статус-код 201
        assert response.status_code == 201

    async def test_get_sub_menu(self):
        """Тест получения 1 подменю"""
        response = client.get(URL + f'/{self.sub_menu_id}')
        # При запросе 1 подменю ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()['title'] == DATA['title']
        # Проверка description
        assert response.json()['description'] == DATA['description']
        # id должен быть строкой
        assert type(response.json()['id']) == str
        # При запуске тестов нет блюд
        assert response.json()['dishes_count'] == 0
        # При получении 1 подменю возвращается статус-код 200
        assert response.status_code == 200
        # Пытаемся взять не существующее подменю
        response_404 = client.get(URL + '/2213123')
        # Ответ для не существующего подменю
        assert response_404.json() == dict(detail='submenu not found')
        # 404 статус код для не существующего
        assert response_404.status_code == 404

    @staticmethod
    async def test_get_list_sub_menu():
        response = client.get(URL)
        # При запросе 1 подменю ответ должен быть в list
        assert type(response.json()) == list
        # Проверка title
        assert response.json()[0]['title'] == DATA['title']
        # Проверка description
        assert response.json()[0]['description'] == DATA['description']
        # id должен быть строкой
        assert type(response.json()[0]['id']) == str
        # При запуске тестов нет блюд
        assert response.json()[0]['dishes_count'] == 0
        # При получении списка подменю возвращается статус-код 200
        assert response.status_code == 200

    async def test_patch_sub_menu(self):
        response = client.patch(URL + f'/{self.sub_menu_id}', json=UPDATED_DATA)
        # При редактировании 1 подменю ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()['title'] == UPDATED_DATA['title']
        # Проверка description
        assert response.json()['description'] == UPDATED_DATA['description']
        # При получении 1 подменю возвращается статус-код 200
        assert response.status_code == 200
        # Пытаемся изменить не существующее подменю
        response_404 = client.patch(URL + '/4353', json=UPDATED_DATA)
        # Ответ на попытку изменения не существующего подменю
        assert response_404.json() == dict(detail='submenu not found')
        # 404 статус код для не существующего
        assert response_404.status_code == 404

    async def test_delete_sub_menu(self):
        """Тест удаления подменю"""
        response_data = {'status': True, 'message': 'The submenu has been deleted'}
        response = client.delete(URL + f'/{self.sub_menu_id}')
        assert response.json() == response_data
        assert response.status_code == 200

    async def test_get_deleted_sub_menu(self):
        """Попытка получить удаленное подменю"""
        response = client.get(URL + f'/{self.sub_menu_id}')
        assert response.status_code == 404
        assert response.json() == dict(detail='submenu not found')

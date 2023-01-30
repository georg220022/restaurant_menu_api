from api.v1.app import app as apps
from fastapi.testclient import TestClient

client = TestClient(apps)
URL = '/api/v1/menus'

DATA = {'title': 'Test title menu', 'description': 'Test description menu'}
UPDATED_DATA = {
    'title': 'Updated test title menu',
    'description': 'Updated test description menu',
}


class TestGroupMenu:
    async def setup_class(self):
        self.response_menu = client.post(URL, json=DATA)
        self.menu_id = self.response_menu.json()['id']

    async def test_post_menu(self):
        """Тест создания меню"""
        response = self.response_menu
        # При создании поста ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()['title'] == DATA['title']
        # Проверка description
        assert response.json()['description'] == DATA['description']
        # id должен быть строкой
        assert type(response.json()['id']) == str
        # При запуске тестов нет подменю
        assert response.json()['submenus_count'] == 0
        # При запуске тестов нет блюд
        assert response.json()['dishes_count'] == 0
        # При создании возвращается статус-код 201
        assert response.status_code == 201

    async def test_get_menu(self):
        """Тест получения 1 меню"""
        response = client.get(URL + f'/{self.menu_id}')
        # При запросе 1 меню ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()['title'] == DATA['title']
        # Проверка description
        assert response.json()['description'] == DATA['description']
        # id должен быть строкой
        assert type(response.json()['id']) == str
        # При запуске тестов нет подменю
        assert response.json()['submenus_count'] == 0
        # При запуске тестов нет блюд
        assert response.json()['dishes_count'] == 0
        # При получении 1 меню возвращается статус-код 200
        assert response.status_code == 200
        # Пытаемся взять не существующее меню
        response_404 = client.get(URL + 'menus/2213')
        # Ответ для не существующего меню
        assert response_404.json() == dict(detail='Not Found')
        # 404 статус код для не существующего
        assert response_404.status_code == 404

    @staticmethod
    async def test_get_list_menu():
        """Тест получения списка меню"""
        response = client.get(URL)
        # При запросе 1 меню ответ должен быть в list
        assert type(response.json()) == list
        # Проверка title
        assert response.json()[0]['title'] == DATA['title']
        # Проверка description
        assert response.json()[0]['description'] == DATA['description']
        # id должен быть строкой
        assert type(response.json()[0]['id']) == str
        # При запуске тестов нет подменю
        assert response.json()[0]['submenus_count'] == 0
        # При запуске тестов нет блюд
        assert response.json()[0]['dishes_count'] == 0
        # При получении списка меню возвращается статус-код 200
        assert response.status_code == 200

    async def test_patch_menu(self):
        """Тест изменения меню"""
        response = client.patch(URL + f'/{self.menu_id}', json=UPDATED_DATA)
        # При редактировании 1 меню ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()['title'] == UPDATED_DATA['title']
        # Проверка description
        assert response.json()['description'] == UPDATED_DATA['description']
        # При получении 1 меню возвращается статус-код 200
        assert response.status_code == 200
        # Пытаемся изменить не существующее меню
        response_404 = client.patch(URL + 'menus/2', json=UPDATED_DATA)
        # Ответ на попытку изменения не существующего меню
        assert response_404.json() == dict(detail='Not Found')
        # 404 статус код для не существующего
        assert response_404.status_code == 404

    async def test_delete_menu(self):
        """Тест удаления меню"""
        response_data = {'status': True, 'message': 'The menu has been deleted'}
        response = client.delete(URL + f'/{self.menu_id}')
        assert response.json() == response_data
        assert response.status_code == 200

    async def test_get_deleted_menu(self):
        """Попытка получить удаленное меню"""
        response = client.get(URL + f'/{self.menu_id}')
        assert response.status_code == 404
        assert response.json() == dict(detail='menu not found')

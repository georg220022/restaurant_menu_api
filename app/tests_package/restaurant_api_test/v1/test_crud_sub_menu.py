import pytest

from .test_crud_menu import DATA as menu_data

DATA = {'title': 'Test dish', 'description': 'Test dish description', 'price': '12.5'}
UPDATED_DATA = {
    'title': 'Updated test dish',
    'description': 'Updated test dish description',
    'price': '25.48',
}


class TestGroupSubMenu:

    def setup_class(self):
        self.url = None
        self.url_with_id = None

    @pytest.mark.asyncio
    async def test_make_valid_url(self, async_app_client):
        # Создадим в БД меню, что бы переменная url была валидна
        response_post_menu = await async_app_client.post(
            'http://test/api/v1/menus', json=menu_data
        )
        # Получим id созданного меню
        menu_id = response_post_menu.json()['id']
        # Прокинем url в self
        type(self).url = f'http://test/api/v1/menus/{str(menu_id)}/submenus'

    @pytest.mark.asyncio
    async def test_post_sub_menu(self, async_app_client):
        '''Тест создания подменю'''
        response = await async_app_client.post(self.url, json=DATA)
        # При создании подменю ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()['title'] == DATA['title']
        # Проверка description
        assert response.json()['description'] == DATA['description']
        # id должен быть строкой
        sub_menu_id = response.json()['id']
        type(self).url_with_id = self.url + '/' + sub_menu_id
        assert type(sub_menu_id) == str
        # При запуске тестов нет блюд
        assert response.json()['dishes_count'] == 0
        # При создании возвращается статус-код 201
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_get_sub_menu(self, async_app_client):
        '''Тест получения 1 подменю'''
        response = await async_app_client.get(self.url_with_id)
        # Пытаемся взять не существующее подменю
        response_404 = await async_app_client.get(self.url + '/2213123')
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
        # Ответ для не существующего подменю
        assert response_404.json() == dict(detail='submenu not found')
        # 404 статус код для не существующего
        assert response_404.status_code == 404

    @pytest.mark.asyncio
    async def test_get_list_sub_menu(self, async_app_client):
        response = await async_app_client.get(self.url)
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

    @pytest.mark.asyncio
    async def test_patch_sub_menu(self, async_app_client):
        response = await async_app_client.patch(self.url_with_id, json=UPDATED_DATA)
        # Пытаемся изменить не существующее подменю
        response_404 = await async_app_client.patch(
            self.url + '/34234234', json=UPDATED_DATA
        )
        # При редактировании 1 подменю ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()['title'] == UPDATED_DATA['title']
        # Проверка description
        assert response.json()['description'] == UPDATED_DATA['description']
        # При получении 1 подменю возвращается статус-код 200
        assert response.status_code == 200

        # Ответ на попытку изменения не существующего подменю
        assert response_404.json() == dict(detail='submenu not found')
        # 404 статус код для не существующего
        assert response_404.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_sub_menu(self, async_app_client):
        '''Тест удаления подменю'''
        response_data = {'status': True, 'message': 'The submenu has been deleted'}
        response = await async_app_client.delete(self.url_with_id)
        assert response.json() == response_data
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_deleted_sub_menu(self, async_app_client):
        '''Попытка получить удаленное подменю'''
        response = await async_app_client.get(self.url_with_id)
        assert response.status_code == 404
        assert response.json() == dict(detail='submenu not found')

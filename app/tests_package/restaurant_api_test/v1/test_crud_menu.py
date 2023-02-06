import pytest

DATA = {"title": "Test title menu", "description": "Test description menu"}
UPDATED_DATA = {
    "title": "Updated test title menu",
    "description": "Updated test description menu",
}


class TestGroupMenu:
    """Класс тестирования основного меню"""

    def setup_class(self):
        self.url = "http://test/api/v1/menus"
        self.url_with_id = None

    @pytest.mark.asyncio
    async def test_post_menu(self, async_app_client):
        """Тест создания меню"""
        response = await async_app_client.post(self.url, json=DATA)
        # При создании поста ответ должен быть в dict
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()["title"] == DATA["title"]
        # Проверка description
        assert response.json()["description"] == DATA["description"]
        menu_id = response.json()["id"]
        # id должен быть строкой
        assert type(menu_id) == str
        # Прокинем полный урл с id в self
        type(self).url_with_id = self.url + "/" + menu_id
        # При запуске тестов нет подменю
        assert response.json()["submenus_count"] == 0
        # При запуске тестов нет блюд
        assert response.json()["dishes_count"] == 0
        # При создании возвращается статус-код 201
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_get_menu(self, async_app_client):
        """Тест получения 1 меню"""
        response = await async_app_client.get(self.url_with_id)
        # Пытаемся взять не существующее меню
        response_404 = await async_app_client.get(self.url + "/2768213")
        # При запросе 1 меню ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()["title"] == DATA["title"]
        # Проверка description
        assert response.json()["description"] == DATA["description"]
        # id должен быть строкой
        assert type(response.json()["id"]) == str
        # При запуске тестов нет подменю
        assert response.json()["submenus_count"] == 0
        # При запуске тестов нет блюд
        assert response.json()["dishes_count"] == 0
        # При получении 1 меню возвращается статус-код 200
        assert response.status_code == 200
        # Ответ для не существующего меню
        assert response_404.json() == dict(detail="menu not found")
        # 404 статус код для не существующего
        assert response_404.status_code == 404

    @pytest.mark.asyncio
    async def test_get_list_menu(self, async_app_client):
        """Тест получения списка меню"""
        response = await async_app_client.get(self.url)
        # При запросе 1 меню ответ должен быть в list
        assert type(response.json()) == list
        # Проверка title
        assert response.json()[0]["title"] == DATA["title"]
        # Проверка description
        assert response.json()[0]["description"] == DATA["description"]
        # id должен быть строкой
        assert type(response.json()[0]["id"]) == str
        # При запуске тестов нет подменю
        assert response.json()[0]["submenus_count"] == 0
        # При запуске тестов нет блюд
        assert response.json()[0]["dishes_count"] == 0
        # При получении списка меню возвращается статус-код 200
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_patch_menu(self, async_app_client):
        """Тест изменения меню"""
        response = await async_app_client.patch(self.url_with_id, json=UPDATED_DATA)
        # Пытаемся изменить не существующее меню
        response_404 = await async_app_client.patch(
            self.url + "1233124", json=UPDATED_DATA
        )
        # При редактировании 1 меню ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()["title"] == UPDATED_DATA["title"]
        # Проверка description
        assert response.json()["description"] == UPDATED_DATA["description"]
        # При получении 1 меню возвращается статус-код 200
        assert response.status_code == 200
        # Ответ на попытку изменения не существующего меню
        assert response_404.json() == dict(detail="Not Found")
        # 404 статус код для не существующего
        assert response_404.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_menu(self, async_app_client):
        """Тест удаления меню"""
        response_data = {"status": True, "message": "The menu has been deleted"}
        response = await async_app_client.delete(self.url_with_id)
        assert response.json() == response_data
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_deleted_menu(self, async_app_client):
        """Попытка получить удаленное меню"""
        response = await async_app_client.get(self.url_with_id)
        assert response.status_code == 404
        assert response.json() == dict(detail="menu not found")

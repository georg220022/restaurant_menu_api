import pytest

from .test_crud_menu import DATA as menu_data
from .test_crud_sub_menu import UPDATED_DATA as sub_menu_data

DATA = {"title": "Test dish", "description": "Test dish description", "price": "12.5"}
UPDATED_DATA = {
    "title": "Updated test dish",
    "description": "Updated test dish description",
    "price": "25.48",
}


class TestGroupDish:
    """Класс тестирования блюд"""

    def setup_class(self):
        self.url = None
        self.url_with_id = None

    @pytest.mark.asyncio
    async def test_make_valid_url(self, async_app_client):
        """Тест + создание валидного URL"""
        # Создадим в БД меню, что бы переменная url была валидна
        response_post_menu = await async_app_client.post(
            "http://test/api/v1/menus", json=menu_data
        )
        # Получим id созданного меню
        menu_id = response_post_menu.json()["id"]
        # Создадим подменю
        response_post_sub_menu = await async_app_client.post(
            f"http://test/api/v1/menus/{menu_id}/submenus", json=sub_menu_data
        )
        # Получим id созданного блюда
        sub_menu_id = response_post_sub_menu.json()["id"]
        # Прокинем url в self
        type(
            self
        ).url = f"http://test/api/v1/menus/{str(menu_id)}/submenus/{str(sub_menu_id)}/dishes"

    @pytest.mark.asyncio
    async def test_create_dish(self, async_app_client):
        """Тест создания блюда"""
        response = await async_app_client.post(self.url, json=DATA)
        # При создании блюда ответ должен быть в dict
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()["title"] == DATA["title"]
        # Проверка description
        assert response.json()["description"] == DATA["description"]
        dish_id = response.json()["id"]
        # id должен быть строкой
        assert type(dish_id) == str
        # Прокинем полный урл с id в self
        type(self).url_with_id = self.url + "/" + dish_id
        # Проверяем цену
        assert response.json()["price"] == DATA["price"]
        # При создании возвращается статус-код 201
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_get_dish(self, async_app_client):
        """Тест получения блюда"""
        response = await async_app_client.get(self.url_with_id)
        # Пытаемся взять не существующее блюдо
        response_404 = await async_app_client.get(self.url + "/2768")
        # При запросе 1 блюдо ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()["title"] == DATA["title"]
        # Проверка description
        assert response.json()["description"] == DATA["description"]
        # id должен быть строкой
        assert type(response.json()["id"]) == str
        # При получении 1 блюдо возвращается статус-код 200
        assert response.status_code == 200
        # Ответ для не существующего блюдо
        assert response_404.json() == dict(detail="dish not found")
        # 404 статус код для не существующего
        assert response_404.status_code == 404

    @pytest.mark.asyncio
    async def test_get_list_dish(self, async_app_client):
        """Тест получения списка блюд"""
        response = await async_app_client.get(self.url)
        # При запросе 1 блюдо ответ должен быть в list
        assert type(response.json()) == list
        # Проверка title
        assert response.json()[0]["title"] == DATA["title"]
        # Проверка description
        assert response.json()[0]["description"] == DATA["description"]
        # id должен быть строкой
        assert type(response.json()[0]["id"]) == str
        # При получении списка блюдо возвращается статус-код 200
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_patch_dish(self, async_app_client):
        """Тест изменения блюда"""
        response = await async_app_client.patch(self.url_with_id, json=UPDATED_DATA)
        # Пытаемся изменить не существующее блюдо
        response_404 = await async_app_client.patch(
            self.url + "/4353", json=UPDATED_DATA
        )
        # При редактировании 1 блюдо ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()["title"] == UPDATED_DATA["title"]
        # Проверка description
        assert response.json()["description"] == UPDATED_DATA["description"]
        # При получении 1 блюдо возвращается статус-код 200
        assert response.status_code == 200
        # Ответ на попытку изменения не существующего блюдо
        assert response_404.json() == dict(detail="dish not found")
        # 404 статус код для не существующего
        assert response_404.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_dish(self, async_app_client):
        """Тест удаления блюда"""
        response_data = {"status": True, "message": "The submenu has been deleted"}
        response = await async_app_client.delete(self.url_with_id)
        assert response.json() == response_data
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_deleted_dish(self, async_app_client):
        """Попытка получить удаленное блюдо"""
        response = await async_app_client.get(self.url_with_id)
        assert response.status_code == 404
        assert response.json() == dict(detail="dish not found")

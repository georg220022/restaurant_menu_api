from api.v1.app import app as apps
from fastapi.testclient import TestClient
from .test_crud_menu import DATA as menu_data
from .test_crud_sub_menu import DATA as sub_menu_data

client = TestClient(apps)
# Создадим в БД меню, что бы переменная url была валидна
response_post_menu = client.post("api/v1/menus", json=menu_data)
# Получим id созданного меню
menu_id = response_post_menu.json()["id"]
# Создадим блюдо
response_post_sub_menu = client.post(
    f"api/v1/menus/{menu_id}/submenus", json=sub_menu_data
)
# Получим id созданного блюда
sub_menu_id = response_post_sub_menu.json()["id"]

# Присвоим переменную при тесте создания блюда через global
dish_id = None

url = f"/api/v1/menus/{str(menu_id)}/submenus/{str(sub_menu_id)}/dishes"


DATA = {"title": "Test dish", "description": "Test dish description", "price": "12.50"}
UPDATED_DATA = {
    "title": "Updated test dish",
    "description": "Updated test dish description",
    "price": "25.48",
}


class TestGroupDish:
    @staticmethod
    def test_post_dish():
        """Тест создания блюда"""
        response = client.post(url, json=DATA)
        # Присвоим сгенерированный id в постгресе при создании блюдо
        global dish_id
        dish_id = response.json()["id"]
        # При создании блюдо ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()["title"] == DATA["title"]
        # Проверка description
        assert response.json()["description"] == DATA["description"]
        # id должен быть строкой
        assert type(response.json()["id"]) == str
        # Проверяем цену
        assert response.json()["price"] == DATA["price"]
        # При создании возвращается статус-код 201
        assert response.status_code == 201

    @staticmethod
    def test_get_dish():
        """Тест получения 1 блюда"""
        response = client.get(url + f"/{dish_id}")
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
        # Пытаемся взять не существующее блюдо
        response_404 = client.get(url + "/2768")
        # Ответ для не существующего блюдо
        assert response_404.json() == dict(detail="dish not found")
        # 404 статус код для не существующего
        assert response_404.status_code == 404

    @staticmethod
    def test_get_list_dish():
        """Тест получения списка блюд"""
        response = client.get(url)
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

    @staticmethod
    def test_patch_dish():
        """Тест изменения блюда"""
        response = client.patch(url + f"/{dish_id}", json=UPDATED_DATA)
        # При редактировании 1 блюдо ответ должен быть НЕ в list
        assert type(response.json()) == dict
        # Проверка title
        assert response.json()["title"] == UPDATED_DATA["title"]
        # Проверка description
        assert response.json()["description"] == UPDATED_DATA["description"]
        # При получении 1 блюдо возвращается статус-код 200
        assert response.status_code == 200
        # Пытаемся изменить не существующее блюдо
        response_404 = client.patch(url + "/4353", json=UPDATED_DATA)
        # Ответ на попытку изменения не существующего блюдо
        assert response_404.json() == dict(detail="dish not found")
        # 404 статус код для не существующего
        assert response_404.status_code == 404

    @staticmethod
    def test_delete_dish():
        """Тест удаления блюда"""
        response_data = {"status": True, "message": "The submenu has been deleted"}
        response = client.delete(url + f"/{dish_id}")
        assert response.json() == response_data
        assert response.status_code == 200

    @staticmethod
    def test_get_deleted_dish():
        """Попытка получить удаленное блюдо"""
        response = client.get(url + f"/{dish_id}")
        assert response.status_code == 404
        assert response.json() == dict(detail="dish not found")

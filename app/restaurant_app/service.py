import os
from uuid import uuid4

from fastapi.responses import FileResponse, JSONResponse
from settings.db import get_cache, get_db

from restaurant_app.cache_module import CacheDish, CacheMenu, CacheSubMenu
from restaurant_app.crud import CrudDish, CrudMenu, CrudSubMenu
from restaurant_app.tasks import app_celery, start_create_xlsx

from .load_data import LoadTestData

BASE_URL = "http://localhost:8000/api/v1"


class MenuService:
    """Логика для меню"""

    @staticmethod
    async def list_menu() -> list[dict]:
        """Метод получения списка меню либо из кеша либо из Postgres"""
        gener_cache = get_cache()
        asyn_cache = await gener_cache.__anext__()
        if await CacheMenu.check_cache(asyn_cache):
            return await CacheMenu.get_menu(asyn_cache)
        response_data = await CrudMenu.get_menu_db()
        return await CacheMenu.set_menu(asyn_cache, response_data)

    @staticmethod
    async def get_menu_id(menu_id) -> dict:
        """Метод получения меню по id либо из кеша либо из Postgres"""
        gener_cache = get_cache()
        asyn_cache = await gener_cache.__anext__()
        if await CacheMenu.check_cache(asyn_cache, menu_id):
            return await CacheMenu.get_menu(asyn_cache, menu_id)
        response_data = await CrudMenu.get_menu_db(menu_id)
        if response_data == "NotFound":
            return JSONResponse(content={"detail": "menu not found"}, status_code=404)
        return await CacheMenu.set_menu(asyn_cache, response_data, menu_id)

    @staticmethod
    async def create_menu(request_data) -> dict:
        """Метод добавления меню в БД и очистки не актуального кеша"""
        gener_cache = get_cache()
        gener_db = get_db()
        asyn_cache = await gener_cache.__anext__()
        asyn_db = await gener_db.__anext__()
        response_data = await CrudMenu.create_menu_db(request_data, asyn_db)
        await CacheMenu.clear_cache(asyn_cache)
        return response_data

    @staticmethod
    async def edit_menu(menu_id, request_data) -> dict:
        """Метод редактирования меню в БД и очистки не актуального кеша"""
        gener_cache = get_cache()
        gener_db = get_db()
        asyn_cache = await gener_cache.__anext__()
        asyn_db = await gener_db.__anext__()
        response_data = await CacheMenu.clear_cache(asyn_cache, menu_id)
        if response_data == "NotFound":
            return JSONResponse(content={"detail": "menu not found"}, status_code=404)
        return await CrudMenu.edit_menu_db(menu_id, request_data, asyn_db)

    @staticmethod
    async def delete_menu(menu_id) -> dict:
        """Метод удаления меню в БД и очистки не актуального кеша"""
        gener_cache = get_cache()
        gener_db = get_db()
        asyn_cache = await gener_cache.__anext__()
        asyn_db = await gener_db.__anext__()
        await CacheMenu.clear_cache(asyn_cache, menu_id)
        return await CrudMenu.delete_menu_db(menu_id, asyn_db)


class SubMenuService:
    """Логика для подменю"""

    @staticmethod
    async def list_submenu(menu_id) -> list[dict]:
        gener_cache = get_cache()
        asyn_cache = await gener_cache.__anext__()
        """Метод получения списка подменю либо из кеша либо из Postgres"""
        if await CacheSubMenu.check_cache(asyn_cache, menu_id):
            return await CacheSubMenu.get_sub_menu(asyn_cache, menu_id)
        response_data = await CrudSubMenu.get_sub_menu_db(menu_id)
        if response_data == []:
            return response_data
        return await CacheSubMenu.set_sub_menu(asyn_cache, response_data, menu_id)

    @staticmethod
    async def get_submenu_id(menu_id, sub_menu_id) -> dict:
        """Метод получения подменю по id либо из кеша либо из Postgres"""
        gener_cache = get_cache()
        asyn_cache = await gener_cache.__anext__()
        if await CacheSubMenu.check_cache(asyn_cache, menu_id, sub_menu_id):
            return await CacheSubMenu.get_sub_menu(asyn_cache, menu_id, sub_menu_id)
        response_data = await CrudSubMenu.get_sub_menu_db(menu_id, sub_menu_id)
        if response_data == "NotFound":
            return JSONResponse(
                content={"detail": "submenu not found"}, status_code=404
            )
        return await CacheSubMenu.set_sub_menu(
            asyn_cache, response_data, menu_id, sub_menu_id
        )

    @staticmethod
    async def create_submenu(menu_id, request_data) -> dict:
        """Метод добавления подменю в БД и очистки не актуального кеша"""
        gener_cache = get_cache()
        gener_db = get_db()
        asyn_cache = await gener_cache.__anext__()
        asyn_db = await gener_db.__anext__()
        response_data = await CrudSubMenu.create_sub_menu_db(
            menu_id, request_data, asyn_db
        )
        await CacheSubMenu.clear_cache(asyn_cache, menu_id)
        return response_data

    @staticmethod
    async def edit_submenu(menu_id, sub_menu_id, request_data) -> dict:
        """Метод редактирования подменю в БД и очистки не актуального кеша"""
        gener_cache = get_cache()
        gener_db = get_db()
        asyn_cache = await gener_cache.__anext__()
        asyn_db = await gener_db.__anext__()
        response_data = await CrudSubMenu.edit_sub_menu_db(
            menu_id, sub_menu_id, request_data, asyn_db
        )
        if response_data == "NotFound":
            return JSONResponse(
                content={"detail": "submenu not found"}, status_code=404
            )
        await CacheSubMenu.clear_cache(asyn_cache, menu_id, sub_menu_id)
        return response_data

    @staticmethod
    async def delete_submenu(menu_id, sub_menu_id) -> dict:
        """Метод удаления подменю в БД и очистки не актуального кеша"""
        gener_cache = get_cache()
        gener_db = get_db()
        asyn_cache = await gener_cache.__anext__()
        asyn_db = await gener_db.__anext__()
        response_data = await CrudSubMenu.delete_sub_menu_db(
            menu_id, sub_menu_id, asyn_db
        )
        await CacheSubMenu.clear_cache(asyn_cache, menu_id, sub_menu_id)
        return response_data


class DishService:
    """Логика для блюд"""

    @staticmethod
    async def list_dish(menu_id, sub_menu_id) -> list[dict]:
        """Метод получения списка блюд либо из кеша либо из Postgres"""
        gener_cache = get_cache()
        gener_db = get_db()
        asyn_cache = await gener_cache.__anext__()
        asyn_db = await gener_db.__anext__()
        if await CacheDish.check_cache(asyn_cache, menu_id, sub_menu_id):
            return await CacheDish.get_dish(asyn_cache, menu_id, sub_menu_id)
        response_data = await CrudDish.get_dish_db(menu_id, sub_menu_id, asyn_db)
        return await CacheDish.set_dish(asyn_cache, response_data, menu_id, sub_menu_id)

    @staticmethod
    async def get_dish_id(
        menu_id,
        sub_menu_id,
        dish_id,
    ) -> dict:
        """Метод получения блюда по id либо из кеша либо из Postgres"""
        gener_cache = get_cache()
        gener_db = get_db()
        asyn_cache = await gener_cache.__anext__()
        asyn_db = await gener_db.__anext__()
        if await CacheDish.check_cache(asyn_cache, menu_id, sub_menu_id, dish_id):
            return await CacheDish.get_dish(asyn_cache, menu_id, sub_menu_id, dish_id)
        response_data = await CrudDish.get_dish_db(
            menu_id, sub_menu_id, asyn_db, dish_id
        )
        if response_data == "NotFound":
            return JSONResponse(content={"detail": "dish not found"}, status_code=404)
        return await CacheDish.set_dish(
            asyn_cache, response_data, menu_id, sub_menu_id, dish_id
        )

    @staticmethod
    async def create_dish(
        menu_id,
        sub_menu_id,
        request_data,
    ) -> dict:
        """Метод добавления блюда в БД и очистки не актуального кеша"""
        gener_cache = get_cache()
        gener_db = get_db()
        asyn_cache = await gener_cache.__anext__()
        asyn_db = await gener_db.__anext__()
        response_data = await CrudDish.create_dish_db(
            menu_id, sub_menu_id, request_data, asyn_db
        )
        await CacheDish.clear_cache(asyn_cache, menu_id, sub_menu_id)
        return response_data

    @staticmethod
    async def edit_dish(
        menu_id,
        sub_menu_id,
        dish_id,
        request_data,
    ) -> dict:
        """Метод редактирования блюда в БД и очистки не актуального кеша"""
        gener_cache = get_cache()
        gener_db = get_db()
        asyn_cache = await gener_cache.__anext__()
        asyn_db = await gener_db.__anext__()
        response_data = await CrudDish.edit_dish_db(
            menu_id, sub_menu_id, dish_id, request_data, asyn_db
        )
        if response_data == "NotFound":
            return JSONResponse(content={"detail": "dish not found"}, status_code=404)
        await CacheDish.clear_cache(asyn_cache, menu_id, sub_menu_id, dish_id)
        return response_data

    @staticmethod
    async def delete_dish(
        menu_id,
        sub_menu_id,
        dish_id,
    ) -> dict:
        """Метод удаления блюда в БД и очистки не актуального кеша"""
        gener_cache = get_cache()
        gener_db = get_db()
        asyn_cache = await gener_cache.__anext__()
        asyn_db = await gener_db.__anext__()
        response_data = await CrudDish.delete_dish_db(
            menu_id, sub_menu_id, dish_id, asyn_db
        )
        await CacheDish.clear_cache(asyn_cache, menu_id, sub_menu_id, dish_id)
        return response_data


class LoadData:
    """Логика загрузки данны в БД"""

    @staticmethod
    async def test_data_to_db() -> JSONResponse:
        """Метод загрузки тестовых данных в БД"""
        bool_load = await LoadTestData.to_db()
        if bool_load:
            return JSONResponse(content={"detail": "Данные загружены"}, status_code=200)
        return JSONResponse(
            content={"detail": "Ошибка при загрузке данных"}, status_code=500
        )


class TaskXLSX:
    """Логика создания/получения пользовательских файлов"""

    @staticmethod
    async def generate_xlsx_menu() -> JSONResponse:
        """Метод запуска задачи на генерацию .xlsx файла меню"""
        gener_cache = get_cache()
        asyn_cache = await gener_cache.__anext__()
        unique_name_file = str(uuid4())
        task_id = str(start_create_xlsx.delay(unique_name_file))
        await asyn_cache.set(task_id, unique_name_file)
        info_data = {
            "detail": f"Принято, GET запрос узнать статус задачи: '{BASE_URL}/status/{task_id}'"
        }
        return JSONResponse(content=info_data, status_code=202)

    @staticmethod
    async def status_task(task_id) -> JSONResponse:
        status_task = app_celery.AsyncResult(task_id).status
        info_data = {"status task": status_task}
        if status_task == "SUCCESS":
            #  Если задача выполнена, добавляем ссылку для скачивания в ответ
            info_data.update({"Download link": f"{BASE_URL}/download/{task_id}"})
        return JSONResponse(content=info_data, status_code=200)

    @staticmethod
    async def download_menu(task_id) -> JSONResponse | FileResponse:
        gener_cache = get_cache()
        asyn_cache = await gener_cache.__anext__()
        name_file = await asyn_cache.get(str(task_id))
        if name_file:
            path_file = f"storage/{name_file}.xlsx"
            #  Проверка существования файла
            if os.path.exists(path_file):
                return FileResponse(
                    path=path_file,
                    filename="FullMenu.xlsx",
                    media_type="application/octet-stream",
                )
        return JSONResponse(content={"detail": "NotFound"}, status_code=404)

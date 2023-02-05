import os
from typing import Any, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, FastAPI
from fastapi.responses import FileResponse, JSONResponse
from redis.asyncio import Connection as RedisConn
from restaurant_app.cache_module import CacheDish, CacheMenu, CacheSubMenu
from restaurant_app.crud import CrudDish, CrudMenu, CrudSubMenu
from restaurant_app.load_data import LoadData
from restaurant_app.tasks import app_celery, start_create_xlsx
from settings.db import get_cache, get_db
from sqlalchemy.orm import Session

from .schemas import (
    DeleteRestaurantDishSchema,
    DeleteRestaurantSubMenuSchema,
    DeleteResturantMenuSchema,
    ErrorSchema,
    GetRestaurantDishSchema,
    GetRestaurantMenuSchema,
    GetRestaurantSubMenuSchema,
    NotFoundDish,
    NotFoundMenu,
    NotFoundSubMenu,
    RequestPatchRestaurantDishSchema,
    RequestPatchRestaurantSubMenuSchema,
    RequestPathRestaurantMenuSchema,
    RequestPostRestaurantDishSchema,
    RequestPostRestaurantMenuSchema,
    RequestPostRestaurantSubMenuSchema,
    ResponseCreateXlsxMenu,
    ResponseGetStatusTask,
    ResponseGetStatusTaskSucces,
    ResponseLoadTestData,
    ResponsePatchRestaurantDishSchema,
    ResponsePatchRestaurantSubMenuSchema,
    ResponsePathRestaurantMenuSchema,
    ResponsePostRestaurantDishSchema,
    ResponsePostRestaurantMenuSchema,
    ResponsePostRestaurantSubMenu,
)

app = FastAPI()
router = APIRouter()

BASE_URL = "http://localhost:8000/api/v1"

"""ОСНОВНОЕ МЕНЮ"""


@app.get(
    "/api/v1/menus",
    response_model=Optional[list[GetRestaurantMenuSchema] | list],
)
async def get_list_menu(
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Получить список основного меню"""
    if await CacheMenu.check_cache(asyn_cache):
        return await CacheMenu.get_menu(asyn_cache)
    response_data = await CrudMenu.get_menu_db()
    return await CacheMenu.set_menu(asyn_cache, response_data)


@app.get(
    "/api/v1/menus/{menu_id}",
    responses={200: {"model": GetRestaurantMenuSchema}, 404: {"model": NotFoundMenu}},
)
async def get_menu(
    menu_id: int,
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Получить определенное основное меню"""
    if await CacheMenu.check_cache(asyn_cache, menu_id):
        return await CacheMenu.get_menu(asyn_cache, menu_id)
    response_data = await CrudMenu.get_menu_db(menu_id)
    if response_data == "NotFound":
        return JSONResponse(content={"detail": "menu not found"}, status_code=404)
    return await CacheMenu.set_menu(asyn_cache, response_data, menu_id)


@app.post(
    "/api/v1/menus",
    status_code=201,
    response_model=Optional[ResponsePostRestaurantMenuSchema | ErrorSchema],
)
async def post_menu(
    request_data: RequestPostRestaurantMenuSchema,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache),
):
    """Создать основное меню"""
    response_data = await CrudMenu.create_menu_db(request_data, asyn_db)
    await CacheMenu.clear_cache(asyn_cache)
    return response_data


@app.patch(
    "/api/v1/menus/{menu_id}",
    response_model=ResponsePathRestaurantMenuSchema
)
async def patch_menu(
    menu_id: int,
    request_data: RequestPathRestaurantMenuSchema | ErrorSchema | None,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache),
):
    """Изменить основное меню"""
    response_data = await CacheMenu.clear_cache(asyn_cache, menu_id)
    if response_data == "NotFound":
        return JSONResponse(content={"detail": "menu not found"}, status_code=404)
    return await CrudMenu.edit_menu_db(menu_id, request_data, asyn_db)


@app.delete(
    "/api/v1/menus/{menu_id}",
    response_model=DeleteResturantMenuSchema
)
async def delete_menu(
    menu_id: int,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache),
):
    """Удалить основное меню"""
    await CacheMenu.clear_cache(asyn_cache, menu_id)
    return await CrudMenu.delete_menu_db(menu_id, asyn_db)


"""ПОДМЕНЮ"""


@app.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=Optional[list[GetRestaurantSubMenuSchema] | Any],
)
async def get_list_submenu(
    menu_id: int,
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Получить список подменю"""
    if await CacheSubMenu.check_cache(asyn_cache, menu_id):
        return await CacheSubMenu.get_sub_menu(asyn_cache, menu_id)
    response_data = await CrudSubMenu.get_sub_menu_db(menu_id)
    if response_data == []:
        return response_data
    return await CacheSubMenu.set_sub_menu(asyn_cache, response_data, menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}",
    response_model=GetRestaurantSubMenuSchema,
    responses={404: {"model": NotFoundSubMenu}},
)
async def get_submenu(
    menu_id: int,
    sub_menu_id: int,
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Получить определенное подменю"""
    if await CacheSubMenu.check_cache(asyn_cache, menu_id, sub_menu_id):
        return await CacheSubMenu.get_sub_menu(asyn_cache, menu_id, sub_menu_id)
    response_data = await CrudSubMenu.get_sub_menu_db(menu_id, sub_menu_id)
    if response_data == "NotFound":
        return JSONResponse(content={"detail": "submenu not found"}, status_code=404)
    return await CacheSubMenu.set_sub_menu(
        asyn_cache, response_data, menu_id, sub_menu_id
    )


@app.post(
    "/api/v1/menus/{menu_id}/submenus",
    status_code=201,
    response_model=ResponsePostRestaurantSubMenu,
)
async def post_sub_menu(
    menu_id: int,
    request_data: RequestPostRestaurantSubMenuSchema,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache),
):
    """Создать подменю"""
    response_data = await CrudSubMenu.create_sub_menu_db(menu_id, request_data, asyn_db)
    await CacheSubMenu.clear_cache(asyn_cache, menu_id)
    return response_data


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}",
    response_model=Optional[ResponsePatchRestaurantSubMenuSchema | ErrorSchema],
)
async def patch_sub_menu(
    menu_id: int,
    sub_menu_id: int,
    request_data: RequestPatchRestaurantSubMenuSchema,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache),
):
    """Изменить подменю"""
    response_data = await CrudSubMenu.edit_sub_menu_db(
        menu_id, sub_menu_id, request_data, asyn_db
    )
    if response_data == "NotFound":
        return JSONResponse(content={"detail": "submenu not found"}, status_code=404)
    await CacheSubMenu.clear_cache(asyn_cache, menu_id, sub_menu_id)
    return response_data


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}",
    response_model=DeleteRestaurantSubMenuSchema,
)
async def delete_sub_menu(
    menu_id: int,
    sub_menu_id: int,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache),
):
    """Удалить подменю"""
    response_data = await CrudSubMenu.delete_sub_menu_db(menu_id, sub_menu_id, asyn_db)
    await CacheSubMenu.clear_cache(asyn_cache, menu_id, sub_menu_id)
    return response_data


"""БЛЮДА"""


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes",
    response_model=list[GetRestaurantDishSchema],
)
async def get_list_dish(
    menu_id: int,
    sub_menu_id: int,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache),
):
    """Получить список блюд"""
    if await CacheDish.check_cache(asyn_cache, menu_id, sub_menu_id):
        return await CacheDish.get_dish(asyn_cache, menu_id, sub_menu_id)
    response_data = await CrudDish.get_dish_db(menu_id, sub_menu_id, asyn_db)
    return await CacheDish.set_dish(asyn_cache, response_data, menu_id, sub_menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}",
    response_model=GetRestaurantDishSchema,
    responses={404: {"model": NotFoundDish}},
)
async def get_dish(
    menu_id: int,
    sub_menu_id: int,
    dish_id: int,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache),
):
    """Получить определенное блюдо"""
    if await CacheDish.check_cache(asyn_cache, menu_id, sub_menu_id, dish_id):
        return await CacheDish.get_dish(asyn_cache, menu_id, sub_menu_id, dish_id)
    response_data = await CrudDish.get_dish_db(menu_id, sub_menu_id, asyn_db, dish_id)
    if response_data == "NotFound":
        return JSONResponse(content={"detail": "dish not found"}, status_code=404)
    return await CacheDish.set_dish(
        asyn_cache, response_data, menu_id, sub_menu_id, dish_id
    )


@app.post(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes",
    status_code=201,
    response_model=ResponsePostRestaurantDishSchema,
)
async def post_dish(
    menu_id: int,
    sub_menu_id: int,
    request_data: RequestPostRestaurantDishSchema,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache),
):
    """Создать блюдо"""
    response_data = await CrudDish.create_dish_db(
        menu_id, sub_menu_id, request_data, asyn_db
    )
    await CacheDish.clear_cache(asyn_cache, menu_id, sub_menu_id)
    return response_data


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}",
    response_model=Optional[ResponsePatchRestaurantDishSchema | ErrorSchema],
)
async def patch_dish(
    menu_id: int,
    sub_menu_id: int,
    dish_id: int,
    request_data: RequestPatchRestaurantDishSchema,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache),
):
    """Изменить блюдо"""
    response_data = await CrudDish.edit_dish_db(
        menu_id, sub_menu_id, dish_id, request_data, asyn_db
    )
    if response_data == "NotFound":
        return JSONResponse(content={"detail": "dish not found"}, status_code=404)
    await CacheDish.clear_cache(asyn_cache, menu_id, sub_menu_id, dish_id)
    return response_data


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}",
    response_model=DeleteRestaurantDishSchema,
)
async def delete_dish(
    menu_id: int,
    sub_menu_id: int,
    dish_id: int,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache),
):
    """Удалить блюдо"""
    response_data = await CrudDish.delete_dish_db(
        menu_id, sub_menu_id, dish_id, asyn_db
    )
    await CacheDish.clear_cache(asyn_cache, menu_id, sub_menu_id, dish_id)
    return response_data


"""ГЕНЕРАЦИЯ/ПОЛУЧЕНИЕ .XLSX МЕНЮ"""


@app.get(
    "/api/v1/load_data",
    responses={200: {"model": ResponseLoadTestData}, 500: {"model": ErrorSchema}},
)
async def load_data_to_db(
    asyn_db: Session = Depends(get_db)
):
    """Загрузка тестовых данных"""
    bool_load = await LoadData.to_db(asyn_db)
    if bool_load:
        return JSONResponse(content={"detail": "Данные загружены"}, status_code=200)
    return JSONResponse(
        content={"detail": "Ошибка при загрузке данных"}, status_code=500
    )


@app.post(
    "/api/v1/create_xlsx",
    responses={202: {"model": ResponseCreateXlsxMenu}},
    status_code=202,
)
async def create_full_menu_to_xlsx(
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Запуск задания создания .xlsx"""
    unique_name_file = str(uuid4())
    task_id = str(start_create_xlsx.delay(unique_name_file))
    await asyn_cache.set(task_id, unique_name_file)
    info_data = {
        "detail": f"Принято, GET запрос узнать статус задачи: '{BASE_URL}/status/{task_id}'"
    }
    return JSONResponse(content=info_data, status_code=202)


@app.get(
    "/api/v1/status/{task_id}",
    responses={
        206: {"model": ResponseGetStatusTask},
        200: {"model": ResponseGetStatusTaskSucces},
    },
    status_code=200,
)
async def get_status_task(
    task_id: str
):
    """Проверка статуса задачи"""
    status_task = app_celery.AsyncResult(task_id).status
    info_data = {"status task": status_task}
    if status_task == "SUCCESS":
        info_data.update({"Download link": f"{BASE_URL}/download/{task_id}"})
    return JSONResponse(content=info_data, status_code=200)


@app.get(
    "/api/v1/download/{task_id}",
    status_code=200
)
async def download(
    task_id: str,
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Загрузка .xlsx меню"""
    name_file = await asyn_cache.get(str(task_id))
    if name_file:
        path_file = f"storage/{name_file}.xlsx"
        if os.path.exists(path_file):
            return FileResponse(
                path=path_file,
                filename="FullMenu.xlsx",
                media_type="multipart/form-data",
            )
    return JSONResponse(content={"detail": "NotFound"}, status_code=404)

from typing import Any, List, Optional

from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from restaurant_app.cache_module import CacheDish, CacheMenu, CacheSubMenu
from restaurant_app.crud import CrudDish, CrudMenu, CrudSubMenu

from .schemas import (DeleteRestaurantDishSchema,
                      DeleteRestaurantSubMenuSchema, DeleteResturantMenuSchema,
                      ErrorSchema, GetRestaurantDishSchema,
                      GetRestaurantMenuSchema, GetRestaurantSubMenuSchema,
                      RequestPatchRestaurantDishSchema,
                      RequestPatchRestaurantSubMenuSchema,
                      RequestPathRestaurantMenuSchema,
                      RequestPostRestaurantDishSchema,
                      RequestPostRestaurantMenuSchema,
                      RequestPostRestaurantSubMenuSchema,
                      ResponsePatchRestaurantDishSchema,
                      ResponsePatchRestaurantSubMenuSchema,
                      ResponsePathRestaurantMenuSchema,
                      ResponsePostRestaurantDishSchema,
                      ResponsePostRestaurantMenuSchema,
                      ResponsePostRestaurantSubMenu)

app = FastAPI()
router = APIRouter()

"""ОСНОВНОЕ МЕНЮ"""


@app.get(
    "/api/v1/menus",
    response_model=Optional[List[GetRestaurantMenuSchema] | list],
)
def get_list_menu():
    """Получить список основного меню"""
    if CacheMenu.check_cache():
        return CacheMenu.get_menu()
    response_data = CrudMenu.get_menu_db()
    return CacheMenu.set_menu(response_data)


@app.get(
    "/api/v1/menus/{menu_id}",
    response_model=Optional[GetRestaurantMenuSchema | ErrorSchema],
)
def get_menu(menu_id: int):
    """Получить определенное основное меню"""
    if CacheMenu.check_cache(menu_id):
        return CacheMenu.get_menu(menu_id)
    response_data = CrudMenu.get_menu_db(menu_id)
    return CacheMenu.set_menu(response_data, menu_id)


@app.post(
    "/api/v1/menus",
    status_code=201,
    response_model=Optional[ResponsePostRestaurantMenuSchema | ErrorSchema],
)
def post_menu(request_data: RequestPostRestaurantMenuSchema):
    """Создать основное меню"""
    response_data = CrudMenu.create_menu_db(request_data)
    CacheMenu.clear_cache()
    return response_data


@app.patch("/api/v1/menus/{menu_id}", response_model=ResponsePathRestaurantMenuSchema)
def patch_menu(menu_id: int, request_data: Optional[RequestPathRestaurantMenuSchema | ErrorSchema]):
    """Изменить основное меню"""
    response_data = CacheMenu.clear_cache(menu_id)
    if response_data == "NotFound":
        return JSONResponse(content={"detail": "menu not found"}, status_code=404)
    return CrudMenu.edit_menu_db(menu_id, request_data)


@app.delete("/api/v1/menus/{menu_id}", response_model=DeleteResturantMenuSchema)
def delete_menu(menu_id: int):
    """Удалить основное меню"""
    CacheMenu.clear_cache(menu_id)
    return CrudMenu.delete_menu_db(menu_id)


"""ПОДМЕНЮ"""


@app.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=Optional[List[GetRestaurantSubMenuSchema] | Any]
)
def get_list_submenu(menu_id: int):
    """Получить список подменю"""
    if CacheSubMenu.check_cache(menu_id):
        return CacheSubMenu.get_sub_menu(menu_id)
    response_data = CrudSubMenu.get_sub_menu_db(menu_id)
    if response_data == []:
        return response_data
    return CacheSubMenu.set_sub_menu(response_data, menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}",
    response_model=Optional[GetRestaurantSubMenuSchema | Any],
)
def get_submenu(menu_id: int, sub_menu_id: int):
    """Получить определенное подменю"""
    if CacheSubMenu.check_cache(menu_id, sub_menu_id):
        return CacheSubMenu.get_sub_menu(menu_id, sub_menu_id)
    response_data = CrudSubMenu.get_sub_menu_db(menu_id, sub_menu_id)
    return CacheSubMenu.set_sub_menu(response_data, menu_id, sub_menu_id)


@app.post(
    "/api/v1/menus/{menu_id}/submenus",
    status_code=201,
    response_model=ResponsePostRestaurantSubMenu,
)
def post_sub_menu(menu_id: int, request_data: RequestPostRestaurantSubMenuSchema):
    """Создать подменю"""
    response_data = CrudSubMenu.create_sub_menu_db(menu_id, request_data)
    CacheSubMenu.clear_cache(menu_id)
    return response_data


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}",
    response_model=Optional[ResponsePatchRestaurantSubMenuSchema | ErrorSchema]
)
def patch_sub_menu(
    menu_id: int, sub_menu_id: int,
    request_data: RequestPatchRestaurantSubMenuSchema
):
    """Изменить подменю"""
    response_data = CrudSubMenu.edit_sub_menu_db(menu_id, sub_menu_id, request_data)
    if response_data == "NotFound":
        return JSONResponse(content={"detail": "submenu not found"}, status_code=404)
    CacheSubMenu.clear_cache(menu_id, sub_menu_id)
    return response_data


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}",
    response_model=DeleteRestaurantSubMenuSchema,
)
def delete_sub_menu(menu_id: int, sub_menu_id: int):
    """Удалить подменю"""
    response_data = CrudSubMenu.delete_sub_menu_db(menu_id, sub_menu_id)
    CacheSubMenu.clear_cache(menu_id, sub_menu_id)
    return response_data


"""БЛЮДА"""


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes",
    response_model=List[GetRestaurantDishSchema],
)
def get_list_dish(menu_id: int, sub_menu_id: int):
    """Получить список блюд"""
    if CacheDish.check_cache(menu_id, sub_menu_id):
        print("Из кеша")
        return CacheDish.get_dish(menu_id, sub_menu_id)
    response_data = CrudDish.get_dish_db(menu_id, sub_menu_id)
    return CacheDish.set_dish(response_data, menu_id, sub_menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}",
    response_model=Optional[GetRestaurantDishSchema | Any],
)
def get_dish(menu_id: int, sub_menu_id: int, dish_id: int):
    """Получить определенное блюдо"""
    if CacheDish.check_cache(menu_id, sub_menu_id, dish_id):
        return CacheDish.get_dish(menu_id, sub_menu_id, dish_id)
    response_data = CrudDish.get_dish_db(menu_id, sub_menu_id, dish_id)
    return CacheDish.set_dish(response_data, menu_id, sub_menu_id, dish_id)


@app.post(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes",
    status_code=201,
    response_model=ResponsePostRestaurantDishSchema,
)
def post_dish(menu_id: int, sub_menu_id: int, request_data: RequestPostRestaurantDishSchema):
    """Создать блюдо"""
    response_data = CrudDish.create_dish_db(menu_id, sub_menu_id, request_data)
    CacheDish.clear_cache(menu_id, sub_menu_id)
    return response_data


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}",
    response_model=Optional[ResponsePatchRestaurantDishSchema | ErrorSchema]
)
def patch_dish(
    menu_id: int, sub_menu_id: int, dish_id: int, request_data: RequestPatchRestaurantDishSchema
):
    """Изменить блюдо"""
    response_data = CrudDish.edit_dish_db(menu_id, sub_menu_id, dish_id, request_data)
    if response_data == "NotFound":
        return JSONResponse(content={"detail": "dish not found"}, status_code=404)
    CacheDish.clear_cache(menu_id, sub_menu_id, dish_id)
    return response_data


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}",
    response_model=DeleteRestaurantDishSchema,
)
def delete_dish(menu_id: int, sub_menu_id: int, dish_id: int):
    """Удалить блюдо"""
    response_data = CrudDish.delete_dish_db(menu_id, sub_menu_id, dish_id)
    CacheDish.clear_cache(menu_id, sub_menu_id, dish_id)
    return response_data

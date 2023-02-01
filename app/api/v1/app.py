from typing import Any, List, Optional

from sqlalchemy.orm import Session
from settings.db import get_db, get_cache
from fastapi import Depends
from redis.asyncio import Connection as RedisConn

from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from restaurant_app.cache_module import CacheDish, CacheMenu, CacheSubMenu
from restaurant_app.crud import CrudDish, CrudMenu, CrudSubMenu

from .schemas import (DeleteRestaurantDishSchema,
                      DeleteRestaurantSubMenuSchema, DeleteResturantMenuSchema,
                      ErrorSchema, GetRestaurantDishSchema,
                      GetRestaurantMenuSchema, GetRestaurantSubMenuSchema,
                      NotFoundDish, NotFoundMenu, NotFoundSubMenu,
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
    '/api/v1/menus',
    response_model=Optional[List[GetRestaurantMenuSchema] | list],
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
    '/api/v1/menus/{menu_id}',
    responses={200: {'model': GetRestaurantMenuSchema}, 404: {'model': NotFoundMenu}},
)
async def get_menu(
    menu_id: int,
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Получить определенное основное меню"""
    if await CacheMenu.check_cache(asyn_cache, menu_id):
        return await CacheMenu.get_menu(asyn_cache, menu_id)
    response_data = await CrudMenu.get_menu_db(menu_id)
    if response_data == 'NotFound':
        return JSONResponse(content={'detail': 'menu not found'}, status_code=404)
    return await CacheMenu.set_menu(asyn_cache, response_data, menu_id)


@app.post(
    '/api/v1/menus',
    status_code=201,
    response_model=Optional[ResponsePostRestaurantMenuSchema | ErrorSchema],
)
async def post_menu(
    request_data: RequestPostRestaurantMenuSchema,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Создать основное меню"""
    response_data = await CrudMenu.create_menu_db(request_data, asyn_db)
    await CacheMenu.clear_cache(asyn_cache)
    return response_data


@app.patch(
    '/api/v1/menus/{menu_id}',
    response_model=ResponsePathRestaurantMenuSchema
)
async def patch_menu(
    menu_id: int,
    request_data: Optional[RequestPathRestaurantMenuSchema | ErrorSchema],
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Изменить основное меню"""
    response_data = await CacheMenu.clear_cache(asyn_cache, menu_id)
    if response_data == 'NotFound':
        return JSONResponse(content={'detail': 'menu not found'}, status_code=404)
    return await CrudMenu.edit_menu_db(menu_id, request_data, asyn_db)


@app.delete(
    '/api/v1/menus/{menu_id}',
    response_model=DeleteResturantMenuSchema
)
async def delete_menu(
    menu_id: int,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Удалить основное меню"""
    await CacheMenu.clear_cache(asyn_cache, menu_id)
    return await CrudMenu.delete_menu_db(menu_id, asyn_db)


"""ПОДМЕНЮ"""


@app.get(
    '/api/v1/menus/{menu_id}/submenus',
    response_model=Optional[List[GetRestaurantSubMenuSchema] | Any],
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
    '/api/v1/menus/{menu_id}/submenus/{sub_menu_id}',
    response_model=GetRestaurantSubMenuSchema,
    responses={404: {'model': NotFoundSubMenu}},
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
    if response_data == 'NotFound':
        return JSONResponse(content={'detail': 'submenu not found'}, status_code=404)
    return await CacheSubMenu.set_sub_menu(asyn_cache, response_data, menu_id, sub_menu_id)


@app.post(
    '/api/v1/menus/{menu_id}/submenus',
    status_code=201,
    response_model=ResponsePostRestaurantSubMenu,
)
async def post_sub_menu(
    menu_id: int,
    request_data: RequestPostRestaurantSubMenuSchema,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Создать подменю"""
    response_data = await CrudSubMenu.create_sub_menu_db(menu_id, request_data, asyn_db)
    await CacheSubMenu.clear_cache(asyn_cache, menu_id)
    return response_data


@app.patch(
    '/api/v1/menus/{menu_id}/submenus/{sub_menu_id}',
    response_model=Optional[ResponsePatchRestaurantSubMenuSchema | ErrorSchema],
)
async def patch_sub_menu(
    menu_id: int,
    sub_menu_id: int,
    request_data: RequestPatchRestaurantSubMenuSchema,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Изменить подменю"""
    response_data = await CrudSubMenu.edit_sub_menu_db(menu_id, sub_menu_id, request_data, asyn_db)
    if response_data == 'NotFound':
        return JSONResponse(content={'detail': 'submenu not found'}, status_code=404)
    await CacheSubMenu.clear_cache(asyn_cache, menu_id, sub_menu_id)
    return response_data


@app.delete(
    '/api/v1/menus/{menu_id}/submenus/{sub_menu_id}',
    response_model=DeleteRestaurantSubMenuSchema,
)
async def delete_sub_menu(
    menu_id: int,
    sub_menu_id: int,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Удалить подменю"""
    response_data = await CrudSubMenu.delete_sub_menu_db(menu_id, sub_menu_id, asyn_db)
    await CacheSubMenu.clear_cache(asyn_cache, menu_id, sub_menu_id)
    return response_data


"""БЛЮДА"""


@app.get(
    '/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes',
    response_model=List[GetRestaurantDishSchema],
)
async def get_list_dish(
    menu_id: int,
    sub_menu_id: int,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Получить список блюд"""
    if await CacheDish.check_cache(asyn_cache, menu_id, sub_menu_id):
        return await CacheDish.get_dish(asyn_cache, menu_id, sub_menu_id)
    response_data = await CrudDish.get_dish_db(menu_id, sub_menu_id, asyn_db)
    return await CacheDish.set_dish(asyn_cache, response_data, menu_id, sub_menu_id)


@app.get(
    '/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}',
    response_model=GetRestaurantDishSchema,
    responses={404: {'model': NotFoundDish}},
)
async def get_dish(
    menu_id: int,
    sub_menu_id: int,
    dish_id: int,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Получить определенное блюдо"""
    if await CacheDish.check_cache(asyn_cache, menu_id, sub_menu_id, dish_id):
        return await CacheDish.get_dish(asyn_cache, menu_id, sub_menu_id, dish_id)
    response_data = await CrudDish.get_dish_db(menu_id, sub_menu_id, asyn_db, dish_id)
    if response_data == 'NotFound':
        return JSONResponse(content={'detail': 'dish not found'}, status_code=404)
    return await CacheDish.set_dish(asyn_cache, response_data, menu_id, sub_menu_id, dish_id)


@app.post(
    '/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes',
    status_code=201,
    response_model=ResponsePostRestaurantDishSchema,
)
async def post_dish(
    menu_id: int,
    sub_menu_id: int,
    request_data: RequestPostRestaurantDishSchema,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Создать блюдо"""
    response_data = await CrudDish.create_dish_db(menu_id, sub_menu_id, request_data, asyn_db)
    await CacheDish.clear_cache(asyn_cache, menu_id, sub_menu_id)
    return response_data


@app.patch(
    '/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}',
    response_model=Optional[ResponsePatchRestaurantDishSchema | ErrorSchema],
)
async def patch_dish(
    menu_id: int,
    sub_menu_id: int,
    dish_id: int,
    request_data: RequestPatchRestaurantDishSchema,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Изменить блюдо"""
    response_data = await CrudDish.edit_dish_db(menu_id, sub_menu_id, dish_id,
                                                request_data, asyn_db)
    if response_data == 'NotFound':
        return JSONResponse(content={'detail': 'dish not found'}, status_code=404)
    await CacheDish.clear_cache(asyn_cache, menu_id, sub_menu_id, dish_id)
    return response_data


@app.delete(
    '/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}',
    response_model=DeleteRestaurantDishSchema,
)
async def delete_dish(
    menu_id: int,
    sub_menu_id: int,
    dish_id: int,
    asyn_db: Session = Depends(get_db),
    asyn_cache: RedisConn = Depends(get_cache)
):
    """Удалить блюдо"""
    response_data = await CrudDish.delete_dish_db(menu_id, sub_menu_id, dish_id, asyn_db)
    await CacheDish.clear_cache(asyn_cache, menu_id, sub_menu_id, dish_id)
    return response_data

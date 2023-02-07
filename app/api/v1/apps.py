from typing import Any, Optional

from fastapi import APIRouter, FastAPI
from restaurant_app.service import (
    DishService,
    LoadData,
    MenuService,
    SubMenuService,
    TaskXLSX,
)

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


"""ОСНОВНОЕ МЕНЮ"""


@app.get(
    "/api/v1/menus",
    response_model=Optional[list[GetRestaurantMenuSchema] | list],
    tags=["Меню"],
)
async def get_list_menu():
    """Получить список основного меню"""
    return await MenuService.list_menu()


@app.get(
    "/api/v1/menus/{menu_id}",
    responses={200: {"model": GetRestaurantMenuSchema}, 404: {"model": NotFoundMenu}},
    tags=["Меню"],
)
async def get_menu(menu_id: int):
    """Получить определенное основное меню"""
    return await MenuService.get_menu_id(menu_id)


@app.post(
    "/api/v1/menus",
    status_code=201,
    response_model=Optional[ResponsePostRestaurantMenuSchema | ErrorSchema],
    tags=["Меню"],
)
async def post_menu(
    request_data: RequestPostRestaurantMenuSchema,
):
    """Создать основное меню"""
    return await MenuService.create_menu(request_data)


@app.patch(
    "/api/v1/menus/{menu_id}",
    response_model=ResponsePathRestaurantMenuSchema,
    tags=["Меню"],
)
async def patch_menu(
    menu_id: int,
    request_data: RequestPathRestaurantMenuSchema | ErrorSchema | None,
):
    """Изменить основное меню"""
    return await MenuService.edit_menu(menu_id, request_data)


@app.delete(
    "/api/v1/menus/{menu_id}",
    response_model=DeleteResturantMenuSchema,
    tags=["Меню"],
)
async def delete_menu(
    menu_id: int,
):
    """Удалить основное меню"""
    return await MenuService.delete_menu(menu_id)


"""ПОДМЕНЮ"""


@app.get(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=Optional[list[GetRestaurantSubMenuSchema] | Any],
    tags=["Подменю"],
)
async def get_list_submenu(menu_id: int):
    """Получить список подменю"""
    return await SubMenuService.list_submenu(menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}",
    response_model=GetRestaurantSubMenuSchema,
    responses={404: {"model": NotFoundSubMenu}},
    tags=["Подменю"],
)
async def get_submenu(menu_id: int, sub_menu_id: int):
    """Получить определенное подменю"""
    return await SubMenuService.get_submenu_id(menu_id, sub_menu_id)


@app.post(
    "/api/v1/menus/{menu_id}/submenus",
    status_code=201,
    response_model=ResponsePostRestaurantSubMenu,
    tags=["Подменю"],
)
async def post_sub_menu(menu_id: int, request_data: RequestPostRestaurantSubMenuSchema):
    """Создать подменю"""
    return await SubMenuService.create_submenu(menu_id, request_data)


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}",
    response_model=Optional[ResponsePatchRestaurantSubMenuSchema | ErrorSchema],
    tags=["Подменю"],
)
async def patch_sub_menu(
    menu_id: int, sub_menu_id: int, request_data: RequestPatchRestaurantSubMenuSchema
):
    """Изменить подменю"""
    return await SubMenuService.edit_submenu(menu_id, sub_menu_id, request_data)


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}",
    response_model=DeleteRestaurantSubMenuSchema,
    tags=["Подменю"],
)
async def delete_sub_menu(menu_id: int, sub_menu_id: int):
    """Удалить подменю"""
    return await SubMenuService.delete_submenu(menu_id, sub_menu_id)


"""БЛЮДА"""


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes",
    response_model=list[GetRestaurantDishSchema],
    tags=["Блюда"],
)
async def get_list_dish(menu_id: int, sub_menu_id: int):
    """Получить список блюд"""
    return await DishService.list_dish(menu_id, sub_menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}",
    response_model=GetRestaurantDishSchema,
    responses={404: {"model": NotFoundDish}},
    tags=["Блюда"],
)
async def get_dish(
    menu_id: int,
    sub_menu_id: int,
    dish_id: int,
):
    """Получить определенное блюдо"""
    return await DishService.get_dish_id(menu_id, sub_menu_id, dish_id)


@app.post(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes",
    status_code=201,
    response_model=ResponsePostRestaurantDishSchema,
    tags=["Блюда"],
)
async def post_dish(
    menu_id: int,
    sub_menu_id: int,
    request_data: RequestPostRestaurantDishSchema,
):
    """Создать блюдо"""
    return await DishService.create_dish(menu_id, sub_menu_id, request_data)


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}",
    response_model=Optional[ResponsePatchRestaurantDishSchema | ErrorSchema],
    tags=["Блюда"],
)
async def patch_dish(
    menu_id: int,
    sub_menu_id: int,
    dish_id: int,
    request_data: RequestPatchRestaurantDishSchema,
):
    """Изменить блюдо"""
    return await DishService.edit_dish(menu_id, sub_menu_id, dish_id, request_data)


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}",
    response_model=DeleteRestaurantDishSchema,
    tags=["Блюда"],
)
async def delete_dish(menu_id: int, sub_menu_id: int, dish_id: int):
    """Удалить блюдо"""
    return await DishService.delete_dish(menu_id, sub_menu_id, dish_id)


"""ЗАГРУЗКА ТЕСТОВЫХ ДАННЫХ"""


@app.get(
    "/api/v1/load_data",
    responses={200: {"model": ResponseLoadTestData}, 500: {"model": ErrorSchema}},
    tags=["Получение .xlsx файла"],
)
async def load_data_to_db():
    """Загрузка тестовых данных"""
    return await LoadData.test_data_to_db()


"""ГЕНЕРАЦИЯ/ПОЛУЧЕНИЕ .XLSX МЕНЮ"""


@app.post(
    "/api/v1/create_xlsx",
    responses={202: {"model": ResponseCreateXlsxMenu}},
    status_code=202,
    tags=["Получение .xlsx файла"],
)
async def create_full_menu_to_xlsx():
    """Запуск задания создания .xlsx"""
    return await TaskXLSX.generate_xlsx_menu()


@app.get(
    "/api/v1/status/{task_id}",
    responses={
        206: {"model": ResponseGetStatusTask},
        200: {"model": ResponseGetStatusTaskSucces},
    },
    status_code=200,
    tags=["Получение .xlsx файла"],
)
async def get_status_task(task_id: str):
    """Проверка статуса задачи"""
    return await TaskXLSX.status_task(task_id)


@app.get(
    "/api/v1/download/{task_id}",
    status_code=200,
    tags=["Получение .xlsx файла"],
)
async def download_xlsx_menu(task_id: str):
    """Загрузка .xlsx меню"""
    return await TaskXLSX.download_menu(task_id)

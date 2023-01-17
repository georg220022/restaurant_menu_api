from typing import List
from fastapi import FastAPI, APIRouter
from .shemas import *
from .crud import CrudDish, CrudMenu, CrudSubMenu


app = FastAPI()
router = APIRouter()


@app.get(
    "/api/v1/menus",
    response_model=Optional[List[GetRestaurantMenuSchema] | List[ErrorSchema]],
)
def get_list_menu():
    return CrudMenu.get_menu_db()


@app.get(
    "/api/v1/menus/{menu_id}",
    response_model=Optional[GetRestaurantMenuSchema | ErrorSchema],
)
def get_menu(menu_id: int):
    return CrudMenu.get_menu_db(menu_id)


@app.post(
    "/api/v1/menus",
    status_code=201,
    response_model=Optional[ResponsePostRestaurantMenuSchema | ErrorSchema],
)
def post_menu(data: RequestPostRestaurantMenuSchema):
    return CrudMenu.create_menu_db(data)


@app.patch("/api/v1/menus/{menu_id}", response_model=ResponsePathRestaurantMenuSchema)
def patch_menu(menu_id: int, data: RequestPathRestaurantMenuSchema):
    return CrudMenu.edit_menu_db(menu_id, data)


@app.delete("/api/v1/menus/{menu_id}", response_model=DeleteResturantMenuSchema)
def delete_menu(menu_id: int):
    return CrudMenu.delete_menu_db(menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus", response_model=List[GetRestaurantSubMenuSchema]
)
def get_list_submenu(menu_id: int):
    return CrudSubMenu.get_sub_menu_db(menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}",
    response_model=GetRestaurantSubMenuSchema,
)
def get_submenu(menu_id: int, sub_menu_id: int):
    return CrudSubMenu.get_sub_menu_db(menu_id, sub_menu_id)


@app.post(
    "/api/v1/menus/{menu_id}/submenus",
    status_code=201,
    response_model=ResponsePostRestaurantSubMenu,
)
def post_sub_menu(menu_id: int, data: RequestPostRestaurantSubMenuSchema):
    return CrudSubMenu.create_sub_menu_db(menu_id, data)


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}",
    response_model=ResponsePatchRestaurantSubMenuSchema,
)
def patch_sub_menu(
    menu_id: int, sub_menu_id: int, data: RequestPatchRestaurantSubMenuSchema
):
    return CrudSubMenu.edit_sub_menu_db(menu_id, sub_menu_id, data)


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}",
    response_model=DeleteRestaurantSubMenuSchema,
)
def delete_sub_menu(menu_id: int, sub_menu_id: int):
    return CrudSubMenu.delete_sub_menu_db(menu_id, sub_menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes",
    response_model=List[GetRestaurantDishSchema],
)
def get_dish(menu_id: int, sub_menu_id: int):
    return CrudDish.get_dish_db(menu_id, sub_menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}",
    response_model=GetRestaurantDishSchema,
)
def get_dishes(menu_id: int, sub_menu_id: int, dish_id: int):
    return CrudDish.get_dish_db(menu_id, sub_menu_id, dish_id)


@app.post(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes",
    status_code=201,
    response_model=ResponsePostRestaurantDishSchema,
)
def post_dish(menu_id: int, sub_menu_id: int, data: RequestPostRestaurantDishSchema):
    return CrudDish.create_dish_db(menu_id, sub_menu_id, data)


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}",
    response_model=ResponsePatchRestaurantDishSchema,
)
def patch_dish(
    menu_id: int, sub_menu_id: int, dish_id: int, data: RequestPatchRestaurantDishSchema
):
    return CrudDish.edit_dish_db(menu_id, sub_menu_id, dish_id, data)


@app.delete(
    "/api/v1/menus/{menu_id}/submenus/{sub_menu_id}/dishes/{dish_id}",
    response_model=DeleteRestaurantDishSchema,
)
def delete_dish(menu_id: int, sub_menu_id: int, dish_id: int):
    return CrudDish.delete_dish_db(menu_id, sub_menu_id, dish_id)

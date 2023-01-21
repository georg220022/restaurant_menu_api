from pydantic import BaseModel
from typing import Optional, List


class ErrorSchema(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "detail": "Error message",
        }


class BaseRestaurantMenuSchema(BaseModel):
    """Базовая схема основного меню"""

    title: str
    description: str

    class Config:
        orm_mode = True


class GetRestaurantMenuSchema(BaseRestaurantMenuSchema):
    """Схема GET ответа главного меню"""

    id: str
    submenus_count: int
    dishes_count: int


class ResponsePostRestaurantMenuSchema(GetRestaurantMenuSchema):
    """Схема ответа к POST запросу главного меню"""

    pass


class RequestPostRestaurantMenuSchema(BaseRestaurantMenuSchema):
    """Схема POST запроса главного меню"""

    pass


class RequestPathRestaurantMenuSchema(BaseRestaurantMenuSchema):
    """Схема PATCH запроса главного меню"""

    pass


class ResponsePathRestaurantMenuSchema(BaseRestaurantMenuSchema):
    """Схема ответа к PATCH запросу главного меню"""

    pass


class DeleteResturantMenuSchema(BaseModel):
    """Схема ответа к DELETE запросу главного меню"""

    status: bool
    message: str


class BaseRestaurantSubMenuSchema(BaseModel):
    """Базовая схема подменю"""

    title: str
    description: str

    class Config:
        orm_mode = True


class ResponsePostRestaurantSubMenu(BaseRestaurantSubMenuSchema):
    """Схема ответа к POST запросу подменю"""

    id: str
    dishes_count: int


class RequestPostRestaurantSubMenuSchema(BaseRestaurantSubMenuSchema):
    """Схема POST запроса подменю"""

    pass


class ResponsePatchRestaurantSubMenuSchema(BaseRestaurantSubMenuSchema):
    """Схема ответа к PATCH запросу подменю"""

    id: str
    dishes_count: int


class RequestPatchRestaurantSubMenuSchema(BaseRestaurantSubMenuSchema):
    """Схема PATCH запроса подменю"""

    pass


class GetRestaurantSubMenuSchema(BaseRestaurantSubMenuSchema):
    """Схема ответа к GET запросу подменю"""

    id: str
    dishes_count: int


class DeleteRestaurantSubMenuSchema(BaseModel):
    """Схема ответа к DELTE запросу подменю"""

    status: bool
    message: str


class BaseRestaurantDishSchema(BaseModel):
    """Базовая схема Блюд"""

    title: str
    description: str
    price: str

    class Config:
        orm_mode = True


class RequestPostRestaurantDishSchema(BaseRestaurantDishSchema):
    """Схема POST запроса блюда"""

    pass


class ResponsePostRestaurantDishSchema(BaseRestaurantDishSchema):
    """Схема ответа к POST запросу блюда"""

    id: str


class RequestPatchRestaurantDishSchema(BaseRestaurantDishSchema):
    """Схема PATCH запроса блюда"""

    pass


class ResponsePatchRestaurantDishSchema(BaseRestaurantDishSchema):
    """Схема ответа к PATCH запросу блюда"""

    id: str


class GetRestaurantDishSchema(BaseRestaurantDishSchema):
    """Схема ответа к GET запросу блюда"""

    id: str


class DeleteRestaurantDishSchema(BaseModel):
    """Схема ответа к DELETE запросу блюда"""

    status: bool
    message: str
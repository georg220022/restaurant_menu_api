from typing import Optional

from pydantic import BaseModel

"""СХЕМЫ ОШИБОК / 404"""  # Схемы ошибок составлены на будущее


class NotFoundMenu(BaseModel):
    """Схема ошибки меню"""
    detail: str


class NotFoundSubMenu(NotFoundMenu):
    """Схема ошибки подменю"""
    pass


class NotFoundDish(NotFoundMenu):
    """Схема ошибки блюда"""
    pass


class ErrorSchema(BaseModel):
    """Схема ошибки"""

    detail: Optional[str | list]

    class Config:
        schema_extra = {
            'detail': 'Error message',
        }


"""СХЕМЫ МЕНЮ"""


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


"""СХЕМЫ ПОДМЕНЮ"""


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


"""СХЕМЫ БЛЮД"""


class BaseRestaurantDishSchema(BaseModel):
    """Базовая схема Блюд"""

    title: str
    description: str
    price: str

    class Config:
        orm_mode = True


class RequestPostRestaurantDishSchema(BaseRestaurantDishSchema):
    """Схема POST запроса блюда"""
    price: float


class ResponsePostRestaurantDishSchema(BaseRestaurantDishSchema):
    """Схема ответа к POST запросу блюда"""

    id: str


class RequestPatchRestaurantDishSchema(BaseRestaurantDishSchema):
    """Схема PATCH запроса блюда"""

    price: float


class ResponsePatchRestaurantDishSchema(BaseRestaurantDishSchema):
    """Схема ответа к PATCH запросу блюда"""

    id: str

    class Config:
        orm_mode = False


class GetRestaurantDishSchema(BaseRestaurantDishSchema):
    """Схема ответа к GET запросу блюда"""
    price: str
    id: str


class DeleteRestaurantDishSchema(BaseModel):
    """Схема ответа к DELETE запросу блюда"""

    status: bool
    message: str

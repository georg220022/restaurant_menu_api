import json
from typing import Optional

from settings.settings import cache_redis


class CacheMenu:

    """Модуль содержащий методы работы с кешем основного меню"""

    menu_404 = {'detail': 'menu not found'}

    @staticmethod
    def check_cache(menu_id: Optional[int | None] = None) -> bool:
        """Метод проверки существования запрошенного меню в кеше"""
        if menu_id:
            return bool(cache_redis.exists(f'menu_{menu_id}'))
        return bool(cache_redis.exists('menu'))

    @classmethod
    def set_menu(
        cls, response_data: Optional[dict | list], menu_id: Optional[int | None] = None
    ) -> Optional[dict | list | str]:
        """Метод сохранения ответа из БД в кеш для меню"""
        if response_data == 'NotFound':
            # Что бы не кешировать постоянно NotFound на любой новый
            # не существующий id, будем отдавать шаблон
            return 'NotFound'
        if response_data:
            if menu_id:
                cache_redis.hmset(f'menu_{menu_id}', response_data)
            else:
                cache_redis.set('menu', json.dumps(response_data))
        return response_data

    @staticmethod
    def get_menu(menu_id: Optional[int | None] = None) -> Optional[dict | list]:
        """Метод получения меню из кеша"""
        if menu_id:
            return cache_redis.hgetall(f'menu_{menu_id}')
        return json.loads(cache_redis.get('menu'))

    @staticmethod
    def clear_cache(menu_id: Optional[int | None] = None) -> None:
        """
        Метод очистки кеша меню, если запись изменилась/удалилась/добавилась
        в зависимости от типа операции (удаление, редактирование, создание).
        """
        if menu_id:
            # Если изменилось/удалилось конкретное меню, то
            # удаляем заготовленный список всех меню и конкретное меню из кеша
            cache_redis.delete('menu', f'menu_{menu_id}')
        else:
            # Если добавилось новое меню, тогда удаляем только кеш всего списка меню
            cache_redis.delete('menu')


"""КЕШ ПОДМЕНЮ"""


class CacheSubMenu:

    """Модуль содержащий методы работы с кешем подменю"""

    sub_menu_404 = {'detail': 'submenu not found'}

    @staticmethod
    def check_cache(menu_id: int, sub_menu_id: Optional[int | None] = None) -> bool:
        """Метод проверки существования запрошенного подменю в кеше"""
        if sub_menu_id:
            return bool(cache_redis.exists(f'menu_{menu_id}_sub_menus_{sub_menu_id}'))
        return bool(cache_redis.exists(f'menu_{menu_id}_sub_menus'))

    @classmethod
    def set_sub_menu(
        cls, response_data: dict, menu_id: int, sub_menu_id: Optional[int | None] = None
    ) -> Optional[dict | str]:
        """Метод сохранения ответа из БД в кеш для подменю"""
        if response_data == 'NotFound':
            # Что бы не кешировать постоянно NotFound на любой новый
            # не существующий id, будем отдавать шаблон
            return 'NotFound'
        if response_data:
            if sub_menu_id:
                cache_redis.hmset(
                    f'menu_{menu_id}_sub_menus_{sub_menu_id}', response_data
                )
            else:
                cache_redis.set(f'menu_{menu_id}_sub_menus', json.dumps(response_data))
        return response_data

    @staticmethod
    def get_sub_menu(
        menu_id: int, sub_menu_id: Optional[int | None] = None
    ) -> Optional[dict | list]:
        """Метод получения подменю из кеша"""
        if sub_menu_id:
            return cache_redis.hgetall(f'menu_{menu_id}_sub_menus_{sub_menu_id}')
        return json.loads(cache_redis.get(f'menu_{menu_id}_sub_menus'))

    @staticmethod
    def clear_cache(menu_id: int, sub_menu_id: Optional[int | None] = None) -> None:
        """
        Метод очистки кеша, если изменилось/удалилось/добавилось подменю.
        При вызове этого метода так же очищается некоторый
        или весь кеш основного меню в зависимости
        от типа операции (удаление, редактирование, создание).
        """
        delete_keys = (
            'menu',
            f'menu_{menu_id}',
            f'menu_{menu_id}_sub_menus',
        )
        if sub_menu_id:
            delete_keys += (f'menu_{menu_id}_sub_menus_{sub_menu_id}',)
        cache_redis.delete(*delete_keys)


"""КЕШ БЛЮД"""


class CacheDish:

    """Модуль содержащий методы работы с кешем блюд"""

    dish_404 = {'detail': 'dish not found'}

    @staticmethod
    def check_cache(
        menu_id: int, sub_menu_id: int, dish_id: Optional[int | None] = None
    ) -> bool:
        """Метод проверки существования запрошенного блюда в кеше"""
        if dish_id:
            return bool(
                cache_redis.exists(
                    f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish_{dish_id}'
                )
            )
        return bool(cache_redis.exists(f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish'))

    @classmethod
    def set_dish(
        cls,
        response_data: Optional[dict | list],
        menu_id: int,
        sub_menu_id: int,
        dish_id: Optional[int | None] = None,
    ) -> Optional[dict | list | str]:
        """Метод сохранения ответа из БД в кеш для блюд"""
        if response_data == 'NotFound':
            #  Что бы не кешировать постоянно NotFound на любой новый
            #  не существующий id, будем отдавать шаблон
            return 'NotFound'
        if response_data:
            if dish_id:
                cache_redis.hmset(
                    f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish_{dish_id}',
                    response_data,
                )
            else:
                cache_redis.set(
                    f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish',
                    json.dumps(response_data),
                )
        return response_data

    @staticmethod
    def get_dish(
        menu_id: int, sub_menu_id: int, dish_id: Optional[int | None] = None
    ) -> Optional[dict | list]:
        """Метод получения блюд из кеша"""
        if dish_id:
            return cache_redis.hgetall(
                f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish_{dish_id}'
            )
        return json.loads(
            cache_redis.get(f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish')
        )

    @staticmethod
    def clear_cache(
        menu_id: int, sub_menu_id: int, dish_id: Optional[int | None] = None
    ) -> None:
        """
        Метод очистки кеша, если изменилось/удалилось/добавилось блюдо.
        При вызове этого метода так же очищается некоторый
        или весь кеш подменюменю и основного меню в зависимости
        от типа операции (удаление, редактирование, создание).
        """
        delete_keys = (
            'menu',
            f'menu_{menu_id}',
            f'menu_{menu_id}_sub_menus',
            f'menu_{menu_id}_sub_menus_{sub_menu_id}',
            f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish',
        )
        if dish_id:
            delete_keys += (f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish_{dish_id}',)
        cache_redis.delete(*delete_keys)

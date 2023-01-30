import json
from typing import Optional


class CacheMenu:

    """Модуль содержащий методы работы с кешем основного меню"""

    menu_404 = {'detail': 'menu not found'}

    @staticmethod
    async def check_cache(
        async_cache,
        menu_id: Optional[int | None] = None
    ) -> bool:
        """Метод проверки существования запрошенного меню в кеше"""
        if menu_id:
            return bool(await async_cache.exists(f'menu_{menu_id}'))
        return bool(await async_cache.exists('menu'))

    @classmethod
    async def set_menu(
        cls,
        async_cache,
        response_data: Optional[dict | list],
        menu_id: Optional[int | None] = None
    ) -> Optional[dict | list | str]:
        """Метод сохранения ответа из БД в кеш для меню"""
        if response_data == 'NotFound':
            # Что бы не кешировать постоянно NotFound на любой новый
            # не существующий id, будем отдавать шаблон
            return 'NotFound'
        if response_data:
            if menu_id:
                await async_cache.hmset(f'menu_{menu_id}', response_data)
            else:
                await async_cache.set('menu', json.dumps(response_data))
        return response_data

    @staticmethod
    async def get_menu(
        async_cache,
        menu_id: Optional[int | None] = None
    ) -> Optional[dict | list]:
        """Метод получения меню из кеша"""
        if menu_id:
            return await async_cache.hgetall(f'menu_{menu_id}')
        return json.loads(await async_cache.get('menu'))

    @staticmethod
    async def clear_cache(
        asyn_cache,
        menu_id: Optional[int | None] = None
    ) -> None:
        """
        Метод очистки кеша меню, если запись изменилась/удалилась/добавилась
        в зависимости от типа операции (удаление, редактирование, создание).
        """
        if menu_id:
            # Если изменилось/удалилось конкретное меню, то
            # удаляем заготовленный список всех меню и конкретное меню из кеша
            await asyn_cache.delete('menu', f'menu_{menu_id}')
        else:
            # Если добавилось новое меню, тогда удаляем только кеш всего списка меню
            await asyn_cache.delete('menu')


"""КЕШ ПОДМЕНЮ"""


class CacheSubMenu:

    """Модуль содержащий методы работы с кешем подменю"""

    sub_menu_404 = {'detail': 'submenu not found'}

    @staticmethod
    async def check_cache(
        asyn_cache,
        menu_id: int,
        sub_menu_id: Optional[int | None] = None
    ) -> bool:
        """Метод проверки существования запрошенного подменю в кеше"""
        if sub_menu_id:
            return bool(await asyn_cache.exists(f'menu_{menu_id}_sub_menus_{sub_menu_id}'))
        return bool(await asyn_cache.exists(f'menu_{menu_id}_sub_menus'))

    @classmethod
    async def set_sub_menu(
        cls,
        asyn_cache,
        response_data: dict,
        menu_id: int,
        sub_menu_id: Optional[int | None] = None
    ) -> Optional[dict | str]:
        """Метод сохранения ответа из БД в кеш для подменю"""
        if response_data == 'NotFound':
            # Что бы не кешировать постоянно NotFound на любой новый
            # не существующий id, будем отдавать шаблон
            return 'NotFound'
        if response_data:
            if sub_menu_id:
                await asyn_cache.hmset(
                    f'menu_{menu_id}_sub_menus_{sub_menu_id}', response_data
                )
            else:
                await asyn_cache.set(f'menu_{menu_id}_sub_menus', json.dumps(response_data))
        return response_data

    @staticmethod
    async def get_sub_menu(
        asyn_cache,
        menu_id: int,
        sub_menu_id: Optional[int | None] = None
    ) -> Optional[dict | list]:
        """Метод получения подменю из кеша"""
        if sub_menu_id:
            return await asyn_cache.hgetall(f'menu_{menu_id}_sub_menus_{sub_menu_id}')
        return json.loads(await asyn_cache.get(f'menu_{menu_id}_sub_menus'))

    @staticmethod
    async def clear_cache(
        asyn_cache,
        menu_id: int,
        sub_menu_id: Optional[int | None] = None
    )-> None:
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
        await asyn_cache.delete(*delete_keys)


"""КЕШ БЛЮД"""


class CacheDish:

    """Модуль содержащий методы работы с кешем блюд"""

    dish_404 = {'detail': 'dish not found'}

    @staticmethod
    async def check_cache(
        asyn_cache,
        menu_id: int,
        sub_menu_id: int,
        dish_id: Optional[int | None] = None
    ) -> bool:
        """Метод проверки существования запрошенного блюда в кеше"""
        if dish_id:
            return bool(
                await asyn_cache.exists(
                    f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish_{dish_id}'
                )
            )
        return bool(await asyn_cache.exists(f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish'))

    @classmethod
    async def set_dish(
        cls,
        asyn_cache,
        response_data,
        menu_id,
        sub_menu_id,
        dish_id: Optional[int | None] = None,
    ) -> Optional[dict | list | str]:
        """Метод сохранения ответа из БД в кеш для блюд"""
        if response_data == 'NotFound':
            #  Что бы не кешировать постоянно NotFound на любой новый
            #  не существующий id, будем отдавать шаблон
            return 'NotFound'
        if response_data:
            if dish_id:
                await asyn_cache.hmset(
                    f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish_{dish_id}',
                    response_data,
                )
            else:
                await asyn_cache.set(
                    f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish',
                    json.dumps(response_data),
                )
        return response_data

    @staticmethod
    async def get_dish(
        asyn_cache,
        menu_id: int,
        sub_menu_id: int,
        dish_id: Optional[int | None] = None
    ) -> Optional[dict | list]:
        """Метод получения блюд из кеша"""
        if dish_id:
            return await asyn_cache.hgetall(
                f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish_{dish_id}'
            )
        return json.loads(await asyn_cache.get(f'menu_{menu_id}_sub_menus_{sub_menu_id}_dish')
        )

    @staticmethod
    async def clear_cache(
        asyn_cache,
        menu_id: int,
        sub_menu_id: int,
        dish_id: Optional[int | None] = None
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
        await asyn_cache.delete(*delete_keys)

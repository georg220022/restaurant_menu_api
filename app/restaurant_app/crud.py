import decimal
from typing import Optional

from asyncpg import PostgresError
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from settings.settings import engine

from .models import (RestaurantDish, RestaurantMenu, RestaurantSubMenu, dish,
                     menus, sub_menus)


class CrudMenu:
    @staticmethod
    async def get_menu_db(
        menu_id: Optional[int] = None
    ) -> Optional[str | list | dict]:
        '''Метод возвращающий весь список меню, либо определенную запись меню по id'''
        query_str = """
            select id, title, description, coalesce(sc, 0) as sub_menu_count, coalesce(dc, 0)
                as dishes_count
            from "RestaurantMenu" rm
            left join (select menu_id, count(*) as sc
                from "RestaurantSubMenu"
                group by menu_id
                order by menu_id) rsm on rsm.menu_id = rm.id
            left join (select menu_id, count(*) as dc
                from "RestaurantDish" as rd_join
                join "RestaurantSubMenu" rsm ON rsm.id  = rd_join.sub_menu_id
                group by menu_id) rd on rd.menu_id = rm.id
            """
        if menu_id:
            query_str += f'\nwhere rm.id={menu_id}'
        async with engine.begin() as conn:
            query = await conn.execute(text(query_str))
        data = []
        for obj in query.fetchall():
            data.append(
                dict(
                    id=str(obj[0]), title=obj[1], description=obj[2],
                    submenus_count=obj[3], dishes_count=obj[4],
                )
            )
        if data:
            if menu_id:
                return data[0]
            return data
        if not menu_id:
            return []
        return 'NotFound'

    @staticmethod
    async def create_menu_db(
        data,
        asyn_db
    ) -> dict:
        '''Метод создания меню'''
        obj = RestaurantMenu(**data.dict())
        try:
            asyn_db.add(obj)
            await asyn_db.commit()
        except PostgresError as exc:
            asyn_db.rollback()
            raise exc
        return dict(
            id=str(obj.id),
            title=obj.title,
            description=obj.description,
            submenus_count=0,
            dishes_count=0,
        )

    @staticmethod
    async def edit_menu_db(
        menu_id,
        data,
        asyn_db
    ):
        '''Метод редактирования меню'''
        query = (menus.update().where(menus.c.id == menu_id).
                 values(title=data.title, description=data.description))
        try:
            await asyn_db.execute(query)
            await asyn_db.commit()
        except PostgresError as exc:
            asyn_db.rollback()
            raise exc
        return await CrudMenu.get_menu_db(menu_id)

    @staticmethod
    async def delete_menu_db(
        menu_id,
        asyn_db
    ):
        '''Метод удаления меню'''
        try:
            await asyn_db.execute(menus.delete().where(menus.c.id == menu_id))
            await asyn_db.commit()
        except PostgresError as exc:
            asyn_db.rollback()
            raise exc
        return {'status': True, 'message': 'The menu has been deleted'}


class CrudSubMenu:
    @staticmethod
    async def get_sub_menu_db(
        menu_id,
        sub_menu_id=None
    ):
        '''Метод получения списка подменю либо определенного меню по id'''
        query_str = f"""
            select id, title, description, coalesce(dc, 0) as dishes_count
            from "RestaurantSubMenu" rsm
            left join (select sub_menu_id, count(*) as dc
                from "RestaurantDish"
                group by sub_menu_id
                order by sub_menu_id) rd on rd.sub_menu_id = rsm.id
            where rsm.menu_id = {menu_id}
        """
        if sub_menu_id:
            query_str += f' AND rsm.id={sub_menu_id}'
        async with engine.begin() as conn:
            query = await conn.execute(text(query_str))
        data = []
        for obj in query:
            data.append(
                dict(
                    id=str(obj[0]), title=obj[1],
                    description=obj[2], dishes_count=obj[3],
                )
            )
        if data:
            if sub_menu_id:
                return data[0]
            return data
        if not sub_menu_id:
            return []
        return 'NotFound'

    @staticmethod
    async def create_sub_menu_db(
        menu_id,
        data,
        asyn_db
    ):
        '''Метод создания подменю'''
        obj = RestaurantSubMenu(**data.dict(), menu_id=menu_id)
        try:
            asyn_db.add(obj)
            await asyn_db.commit()
        except PostgresError as exc:
            asyn_db.rollback()
            raise exc
        return dict(
            id=str(obj.id), title=obj.title, description=obj.description, dishes_count=0
        )

    @staticmethod
    async def edit_sub_menu_db(
        menu_id,
        sub_menu_id,
        data,
        asyn_db
    ):
        '''Метод редактирования подменю'''
        query = (sub_menus.update().where(sub_menus.c.id == sub_menu_id).
                 values(title=data.title, description=data.description))
        try:
            await asyn_db.execute(query)
            await asyn_db.commit()
        except PostgresError as exc:
            asyn_db.rollback()
            raise exc
        return await CrudSubMenu.get_sub_menu_db(menu_id, sub_menu_id)

    @staticmethod
    async def delete_sub_menu_db(
        menu_id,
        sub_menu_id,
        asyn_db
    ):
        '''Метод удаления подменю'''
        try:
            await asyn_db.execute(sub_menus.delete().where(sub_menus.c.id == sub_menu_id))
            await asyn_db.commit()
        except PostgresError as exc:
            asyn_db.rollback()
            raise exc
        return {'status': True, 'message': 'The submenu has been deleted'}


"""Блюда"""


class CrudDish:
    @staticmethod
    async def get_dish_db(
        menu_id,
        sub_menu_id,
        asyn_db,
        dish_id=None
    ):
        '''Метод получения списка блюд либо определенного блюда по id'''
        data = []
        if not dish_id:
            for obj in await asyn_db.execute(dish.select()):
                data.append(
                    dict(
                        id=str(obj.id),
                        title=obj.title,
                        description=obj.description,
                        price=str(decimal.Decimal(obj.price).normalize()),
                    )
                )
        else:
            query_obj = await asyn_db.execute(dish.select().where(dish.c.id == dish_id))
            if query_obj:
                for obj in query_obj:
                    data = dict(
                        id=str(obj.id),
                        title=obj.title,
                        description=obj.description,
                        price=str(decimal.Decimal(obj.price).normalize()),
                    )
        if data:
            return data
        if not dish_id:
            return []
        return 'NotFound'

    @staticmethod
    async def create_dish_db(
        menu_id,
        sub_menu_id,
        data,
        asyn_db
    ):
        '''Метод создания блюда'''
        obj = RestaurantDish(**data.dict(), sub_menu_id=sub_menu_id)
        try:
            asyn_db.add(obj)
            await asyn_db.commit()
        except IntegrityError as e:
            asyn_db.rollback()
            raise e
        return dict(
            id=str(obj.id),
            title=obj.title,
            description=obj.description,
            price=str(obj.price),
        )

    @staticmethod
    async def edit_dish_db(
        menu_id,
        sub_menu_id,
        dish_id,
        data,
        asyn_db
    ):
        '''Метод редактирования блюда'''
        query = (dish.update().where(dish.c.id == dish_id).
                 values(title=data.title, description=data.description, price=data.price))
        try:
            await asyn_db.execute(query)
            await asyn_db.commit()
        except PostgresError as exc:
            asyn_db.rollback()
            raise exc
        return await CrudDish.get_dish_db(None, None, asyn_db, dish_id)

    @staticmethod
    async def delete_dish_db(
        menu_id,
        sub_menu_id,
        dish_id,
        asyn_db
    ):
        '''Метод удаления блюда'''
        try:
            await asyn_db.execute(dish.delete().where(dish.c.id == dish_id))
            await asyn_db.commit()
        except PostgresError as exc:
            asyn_db.rollback()
            raise exc
        return {'status': True, 'message': 'The submenu has been deleted'}

from .models import RestaurantDish, RestaurantMenu, RestaurantSubMenu
from settings.settings import session as db, engine
from fastapi.responses import JSONResponse
from typing import Optional


class CrudMenu:
    @staticmethod
    def get_menu_db(menu_id: Optional[int] = None):
        query_str = """
            select id, title, description, coalesce(sc, 0) as sub_menu_count, coalesce(dc, 0) as dishes_count
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
            query_str += f"\nwhere rm.id={menu_id}"
        query = engine.execute(query_str)
        data = []
        for obj in query:
            data.append(
                dict(
                    id=str(obj[0]),
                    title=obj[1],
                    description=obj[2],
                    submenus_count=obj[3],
                    dishes_count=obj[4],
                )
            )
        if data:
            if menu_id:
                return data[0]
            return data
        if not menu_id:
            return JSONResponse(content=[], status_code=200)
        return JSONResponse(content={"detail": "menu not found"}, status_code=404)

    @staticmethod
    def create_menu_db(data):
        obj = RestaurantMenu(title=data.title, description=data.description)
        db.add(obj)
        db.commit()
        return dict(
            id=str(obj.id),
            title=obj.title,
            description=obj.description,
            submenus_count=0,
            dishes_count=0,
        )

    @staticmethod
    def edit_menu_db(menu_id, data):
        db.query(RestaurantMenu).filter(RestaurantMenu.id == menu_id).update(
            {"title": data.title, "description": data.description}
        )
        db.commit()
        return CrudMenu.get_menu_db(menu_id)

    @staticmethod
    def delete_menu_db(menu_id):
        db.query(RestaurantMenu).filter(RestaurantMenu.id == menu_id).delete()
        db.commit()
        return {"status": True, "message": "The menu has been deleted"}


class CrudSubMenu:
    @staticmethod
    def get_sub_menu_db(menu_id, sub_menu_id=None):
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
            query_str += f" AND rsm.id={sub_menu_id}"
        query = engine.execute(query_str)
        data = []
        for obj in query:
            data.append(
                dict(
                    id=str(obj[0]),
                    title=obj[1],
                    description=obj[2],
                    dishes_count=obj[3],
                )
            )
        if data:
            if sub_menu_id:
                return data[0]
            return data
        if not sub_menu_id:
            return JSONResponse(content=[], status_code=200)
        return JSONResponse(content={"detail": "submenu not found"}, status_code=404)

    @staticmethod
    def create_sub_menu_db(menu_id, data):
        obj = RestaurantSubMenu(
            title=data.title, description=data.description, menu_id=menu_id
        )
        db.add(obj)
        db.commit()
        return dict(
            id=str(obj.id), title=obj.title, description=obj.description, dishes_count=0
        )

    @staticmethod
    def edit_sub_menu_db(menu_id, sub_menu_id, data):
        db.query(RestaurantSubMenu).filter(
            RestaurantSubMenu.id == sub_menu_id, RestaurantSubMenu.menu_id == menu_id
        ).update({"title": data.title, "description": data.description})
        db.commit()
        return CrudSubMenu.get_sub_menu_db(menu_id, sub_menu_id)

    @staticmethod
    def delete_sub_menu_db(menu_id, sub_menu_id):
        db.query(RestaurantSubMenu).filter(
            RestaurantSubMenu.id == sub_menu_id, RestaurantSubMenu.menu_id == menu_id
        ).delete()
        db.commit()
        return {"status": True, "message": "The submenu has been deleted"}


class CrudDish:
    @staticmethod
    def get_dish_db(menu_id, sub_menu_id, dish_id=None):
        data = []
        if not dish_id:
            query_obj = (
                db.query(RestaurantDish)
                .filter(RestaurantDish.sub_menu_id == sub_menu_id)
                .all()
            )
            for obj in query_obj:
                data.append(
                    dict(
                        id=str(obj.id),
                        title=obj.title,
                        description=obj.description,
                        price=str(obj.price),
                    )
                )
        else:
            query_obj = (
                db.query(RestaurantDish).filter(RestaurantDish.id == dish_id).first()
            )
            if query_obj:
                data = dict(
                    id=str(query_obj.id),
                    title=query_obj.title,
                    description=query_obj.description,
                    price=str(query_obj.price),
                )
        if data:
            return data
        if not dish_id:
            return JSONResponse(content=[], status_code=200)
        return JSONResponse(content={"detail": "dish not found"}, status_code=404)

    @staticmethod
    def create_dish_db(menu_id, sub_menu_id, data):
        obj = RestaurantDish(
            title=data.title,
            description=data.description,
            price=data.price,
            sub_menu_id=sub_menu_id,
        )
        db.add(obj)
        db.commit()
        return dict(
            id=str(obj.id),
            title=obj.title,
            description=obj.description,
            price=str(obj.price),
        )

    @staticmethod
    def edit_dish_db(menu_id, sub_menu_id, dish_id, data):
        db.query(RestaurantDish).filter(RestaurantDish.id == dish_id).update(
            {"title": data.title, "description": data.description, "price": data.price}
        )
        db.commit()
        return CrudDish.get_dish_db(None, None, dish_id)

    @staticmethod
    def delete_dish_db(menu_id, sub_menu_id, dish_id):
        db.query(RestaurantDish).filter(RestaurantDish.id == dish_id).delete()
        db.commit()
        return {"status": True, "message": "The submenu has been deleted"}

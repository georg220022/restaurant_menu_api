from asyncpg import PostgresError
from .models import dish, menus, sub_menus
from sqlalchemy.exc import IntegrityError

DATA_MENU = [
    dict(title="Горчяие блюда", description="Любые горячие блюда"),
    dict(title="Холодные блюда", description="Любые холодные блюда"),
]

DATA_SUB_MENU = [
    dict(title="Супы", description="Любые супы"),
    dict(title="Каши", description="Любые каши"),
    dict(title="Салаты", description="Любые салаты"),
    dict(title="Бутерброды", description="Любые бутерброды"),
]

DATA_DISH = [
    dict(title="Суп куриный", description="Суп куриный вкусный", price=12.34),
    dict(title="Суп лапшичный", description="Суп лапшичный вкусный", price=12.35),
    dict(title="Каша манная", description="Каша манная вкусная", price=12.36),
    dict(title="Каша гречневая", description="Каша гречневая вкусная", price=12.37),
    dict(title="Салат оливье", description="Салат оливье вкусный", price=12.38),
    dict(title="Салат цезарь", description="Салат цезарь вкусный", price=12.39),
    dict(
        title="Бутерброд с колбасой",
        description="Бутерброд с колбасой вкусный",
        price=12.40,
    ),
    dict(
        title="Бутерброд с беконом",
        description="Бутерброд с беконом вкусный",
        price=12.41,
    ),
]


class LoadData:
    @staticmethod
    async def to_db(db_conn) -> bool:
        query_load_menu = menus.insert().returning(menus.c.id).values(DATA_MENU)
        result_menu = (await db_conn.execute(query_load_menu)).fetchall()
        indx = 0
        for ids in result_menu:
            for _ in range(0, 2):
                DATA_SUB_MENU[indx].update(menu_id=ids._asdict()["id"])
                indx += 1
        query_load_sub_menu = (
            sub_menus.insert().returning(sub_menus.c.id).values(DATA_SUB_MENU)
        )
        result_sub_menu = (await db_conn.execute(query_load_sub_menu)).fetchall()
        indx = 0
        for ids in result_sub_menu:
            for _ in range(0, 2):
                DATA_DISH[indx].update(sub_menu_id=ids._asdict()["id"])
                indx += 1
        query_load_dish = dish.insert().values(DATA_DISH)
        try:
            await db_conn.execute(query_load_dish)
            await db_conn.commit()
        except IntegrityError:
            return False
        except PostgresError:
            return False
        return True

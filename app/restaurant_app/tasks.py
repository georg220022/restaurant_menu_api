import asyncio
import os

import xlsxwriter
from celery import Celery
from dotenv import load_dotenv
from restaurant_app.models import RestaurantDish, RestaurantMenu, RestaurantSubMenu
from settings.settings import db_async_session
from sqlalchemy import func, select

load_dotenv()

RMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")
RMQ_URL = os.getenv("RMQ_URL")
app_celery = Celery(
    "restaurant_app",
    broker=f"pyamqp://{RMQ_USER}:{RMQ_PASSWORD}@{RMQ_URL}:5672",
    backend="rpc://redis_db:6379",
    task_track_started=True,
)
app_celery.autodiscover_tasks()


async def get_full_menu_from_db():
    rm = RestaurantMenu
    rsm = RestaurantSubMenu
    rd = RestaurantDish
    dish_m = (
        (
            select(
                func.json_agg(
                    func.json_build_object(
                        "title",
                        rd.title,
                        "description",
                        rd.description,
                        "price",
                        rd.price,
                    )
                )
            )
        )
        .where(rsm.id == rd.sub_menu_id)
        .scalar_subquery()
    )
    sub_m = (
        select(
            func.json_agg(
                func.json_build_object(
                    "title", rsm.title, "description", rsm.description, "dishes", dish_m
                )
            )
        )
        .where(rm.id == rsm.menu_id)
        .scalar_subquery()
    )
    stmt = select(
        func.json_agg(
            func.json_build_object(
                "title", rm.title, "description", rm.description, "submenus", sub_m
            )
        )
    )
    return await db_async_session().execute(stmt)


async def create_xlsx(unique_name):
    data = await get_full_menu_from_db()
    workbook = xlsxwriter.Workbook(f"storage/{unique_name}.xlsx")
    worksheet = workbook.add_worksheet()
    row = 0
    not_empty_data = list(data)[0][0]
    if not_empty_data:
        for menu in enumerate(not_empty_data, 1):
            if menu[0]:
                if row > 0:
                    row += 1
                num_menu = menu[0]
                menu_title = menu[1]["title"]
                menu_description = menu[1]["description"]
                worksheet.write(row, 0, num_menu)
                worksheet.write(row, 1, menu_title)
                worksheet.write(row, 2, menu_description)
                if menu[1]["submenus"]:
                    for sub_menu in enumerate(menu[1]["submenus"], 1):
                        if sub_menu[0]:
                            row += 1
                            num_submenu = sub_menu[0]
                            submenu_title = sub_menu[1]["title"]
                            submenu_description = sub_menu[1]["description"]
                            worksheet.write(row, 1, num_submenu)
                            worksheet.write(row, 2, submenu_title)
                            worksheet.write(row, 3, submenu_description)
                            if sub_menu[1]["dishes"]:
                                for dish in enumerate(sub_menu[1]["dishes"], 1):
                                    if dish[0]:
                                        row += 1
                                        num_dish = dish[0]
                                        dish_title = dish[1]["title"]
                                        dish_description = dish[1]["description"]
                                        dish_price = dish[1]["price"]
                                        worksheet.write(row, 2, num_dish)
                                        worksheet.write(row, 3, dish_title)
                                        worksheet.write(row, 4, dish_description)
                                        worksheet.write(
                                            row, 5, f"{round(dish_price, 2):.2f}"
                                        )
    workbook.close()


@app_celery.task
def start_create_xlsx(unique_name):
    asyncio.run(create_xlsx(unique_name))

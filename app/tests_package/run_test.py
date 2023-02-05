"""Импорты тестов стоят в порядке их выполнения! меню -> подменю -> блюда.
Смена порядка выполнения приведет к ошибкам в тестах!!!"""
from tests_package.conftest import async_app_client, event_loop  # NOQA
from tests_package.restaurant_api_test.v1.test_crud_menu import TestGroupMenu  # NOQA
from tests_package.restaurant_api_test.v1.test_crud_sub_menu import (  # NOQA
    TestGroupSubMenu,
)
from tests_package.restaurant_api_test.v1.test_crud_dish import TestGroupDish  # NOQA

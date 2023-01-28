from tests_package.restaurant_api_test.v1.test_crud_dish import TestGroupDish
from tests_package.restaurant_api_test.v1.test_crud_menu import TestGroupMenu
from tests_package.restaurant_api_test.v1.test_crud_sub_menu import \
    TestGroupSubMenu

if __name__ == "__main__":
    TestGroupMenu()
    TestGroupSubMenu()
    TestGroupDish()

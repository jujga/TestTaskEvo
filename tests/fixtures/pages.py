import allure
import pytest
from tests.pages.pageobjects import MainPage
from tests.fixtures.drivers import driver
from tests.test_data.endpoints import PromEndpoints
from tests import common


@pytest.fixture
@allure.step(f'Jumping to {PromEndpoints.velosipednye_shiny()} and logining')
def logined_page(driver: driver):
    driver.get(PromEndpoints.velosipednye_shiny())
    main_page = MainPage(driver)
    main_page.sign_in_link.click()
    common.login_steps(main_page)
    return main_page.go_logined_page()


@pytest.fixture
@allure.step(f'Jumping to {PromEndpoints.velosipednye_shiny()}')
def main_page(driver: driver):
    driver.get(PromEndpoints.velosipednye_shiny())
    return MainPage(driver)

import pytest
from tests.pages.pageobjects import MainPage
from tests.fixtures.drivers import driver
import tests.test_data.endpoints
from tests import common


@pytest.fixture
def logined_page(driver: driver):
    driver.get(tests.test_data.endpoints.velosipednye_shiny_url)
    main_page = MainPage(driver)
    main_page.comein_link.click()
    common.login_steps(main_page)
    return main_page.go_logined_page()


@pytest.fixture
def main_page(driver: driver):
    driver.get(tests.test_data.endpoints.velosipednye_shiny_url)
    return MainPage(driver)

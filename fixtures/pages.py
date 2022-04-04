import pytest
from pages.pageobjects import MainPage
from fixtures.drivers import driver
import test_data.endpoints
import common


@pytest.fixture
def logined_page(driver: driver):
    driver.get(test_data.endpoints.velosipednye_shiny_url)
    main_page = MainPage(driver)
    main_page.comein_link.click()
    common.login_steps(main_page)
    return main_page.go_logined_page()


@pytest.fixture
def main_page(driver: driver):
    driver.get(test_data.endpoints.velosipednye_shiny_url)
    return MainPage(driver)

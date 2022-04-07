import pytest
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
# import tests.test_data.endpoints
from tests.test_data.endpoints import PromEndpoints
from tests.pages.pageobjects import FavoritePage


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)

    def fin():
        driver.get(PromEndpoints.favorites())
        # очищается список избранных после каждого теста
        for cross_button_index in FavoritePage(driver).del_favs_button:
            sleep(1)  # пока что ничего лучшего тут не вышло(
            cross_button_index.click()
        sleep(1)
        driver.close()

    request.addfinalizer(fin)
    return driver

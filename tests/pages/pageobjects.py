# не смог одолеть проблему циклического импорта,
# потому все пейжобжекты поместил в один файл

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage(object):
    # базовая страница. типа абстрактный класс
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(driver, 10)

    def browser_back_button_click(self):
        self.driver.back()

    @staticmethod
    def goods_heart_button(web_item):
        return web_item.find_element(By.XPATH,
                                     './/span[@data-qaid="add_favorite"]')

    @property
    def comein_link(self):
        return self.driver.find_element(By.XPATH,
                                        '//button[@data-qaid="sign-in"]')

    @property
    def email_button(self):
        return self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@data-qaid="email_btn"]')))

    @property
    def email_field(self):
        return self.driver.find_element(By.XPATH,
                                        '//input[@id="email_field"]')

    @property
    def next_button(self):
        return self.driver.find_element(By.XPATH,
                                        '//button[@id="emailConfirmButton"]')

    @property
    def password_field(self):
        return self.driver.find_element(By.XPATH,
                                        '//input[@id="enterPassword"]')

    @property
    def comein_button(self):
        return self.driver.find_element(
            By.XPATH, '//button[@id="enterPasswordConfirmButton"]')

    def comein_button_click(self):
        self.comein_button.click()

    def go_logined_page(self):
        return LoginedPage(self.driver)


class MainPage(BasePage):
    # основная страница до логина
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def goods_list(self):
        # эксплисит ждет, пока не появится список товаров
        return self.wait.until(EC.visibility_of_any_elements_located(
            (By.XPATH, '//div[@data-qaid="product_block"]')))

    # def goods_click(self,i):
    #     self.goods_list[i].click()


class LoginedPage(MainPage):
    # страница, когда залогинены
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def fav_page_button(self):
        return self.driver.find_element(
            By.XPATH, '//button[@data-qaid = "favorite_cabinet_button"]')

    def fav_page_button_click(self):
        self.fav_page_button.click()
        return FavoritePage(self.driver)

    def goods_click(self, i):
        self.goods_list[i].click()
        return GoodsDetail(self.driver)

    @staticmethod
    def good_name_text(web_item):
        return web_item.find_element(
            By.XPATH, './/span[@data-qaid="product_name"]').text

    @staticmethod
    def goods_heart_button(web_item):
        return web_item.find_element(By.XPATH,
                                     './/span[@data-qaid="add_favorite"]')

    @property
    def fav_button_counter_text(self):
        return self.driver.find_element(By.XPATH,
                                        '//div[@data-qaid="counter"]').text

    @staticmethod
    def goods_link(web_item):
        return self.driver.find_element(By.XPATH,
                                        '//div[@data-qaid="counter"]').text


class FavoritePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def fav_button_counter_text(self):
        return self.driver.find_element(
            By.XPATH, '//div[@data-qaid="counter"]//span').text

    @property
    def del_favs_button(self):
        return self.driver.find_elements(By.XPATH,
                                         '//span[@data-qaid="delete_icon"]')

    @property
    def fav_list(self):
        return self.driver.find_elements(By.XPATH,
                                         '//a[@data-qaid="product_name"]')


class GoodsDetail(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @property
    def fav_add_button(self):
        return self.driver.find_element(By.XPATH,
                                        '//span[@data-qaid="add_favorite"]')

    @property
    def good_code_text(self):
        return self.driver.find_element(
            By.XPATH, '//span[@data-qaid="product-sku"]').text

    @property
    def good_name_txt(self):
        return self.driver.find_element(
            By.XPATH, '//h1[@data-qaid="product_name"]').text

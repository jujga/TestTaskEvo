import pytest
import pytest_check as check
from tests.pages.pageobjects import LoginedPage
import tests.common as common

"""параметризуем массивом индексов товаров и признаком,
добавляем в избранное из списка или из товара"""


@pytest.mark.ui
@pytest.mark.parametrize('fav_numbers, add_fav_from_detail', (
        ((0, 1), 'add_from_goods_list'),
        ((0, 2, 4), 'add_from_goods_list'),
        ((2, 5), 'add_from_goods_detail')))
def test_add2fav(logined_page, fav_numbers: tuple, add_fav_from_detail: str):
    goods_for_fav = logined_page.goods_list
    fav_goods_names_expected = []
    for goods_index in fav_numbers:
        match add_fav_from_detail:
            case 'add_from_goods_list':
                # goods_for_fav = logined_page.goods_list
                # набиваем список названий товаров,потом их искать в избранном
                fav_goods_names_expected.append(
                    LoginedPage.good_name_text(goods_for_fav[goods_index]))
                # клик по сердцу - добавление в избранное
                LoginedPage.goods_heart_button(
                    goods_for_fav[goods_index]).click()
            case 'add_from_goods_detail':  # добавляем в избранное c товара
                # проваливаемся в товар
                goodsdetail_page = logined_page.goods_click(goods_index)
                # запоминаем товар
                fav_goods_names_expected.append(goodsdetail_page.good_name_txt)
                goodsdetail_page.fav_add_button.click()
                goodsdetail_page.browser_back_button_click()

    check.equal(logined_page.fav_button_counter_text,
                str(len(fav_numbers)),
                'Индекс количества элементов в избранном '
                'на странице с товарами')
    favorite_page = logined_page.fav_page_button_click()

    check.equal(favorite_page.fav_button_counter_text, str(len(fav_numbers)),
                'Количество элементов в избранном на странице Избранное')
    assert_goodsnames_in_fav(favorite_page.fav_list, fav_goods_names_expected)


# добавляется один товар в избранное без предварительного логина
@pytest.mark.ui
def test_add2fav_out_of_login(main_page):
    # запоминаем товар, что добавляется в избранное
    fav_goods_names_expected = \
        {(LoginedPage.good_name_text(main_page.goods_list[1]))}
    LoginedPage.goods_heart_button(
        main_page.goods_list[1]).click()
    common.login_steps(main_page)
    logined_page = main_page.go_logined_page()
    check.equal(logined_page.fav_button_counter_text, '1',
                'Количество избранных на кнопке Избранное')
    favorite_page = logined_page.fav_page_button_click()
    check.equal(favorite_page.fav_button_counter_text, '1',
                'Количество на странице Избранное')
    assert_goodsnames_in_fav(favorite_page.fav_list, fav_goods_names_expected)


# добавляется с индексом 1 и 2, с индексом 1 убирается
@pytest.mark.ui
def test_add2fav_1_2_1(logined_page):
    goods_for_fav = logined_page.goods_list
    LoginedPage.goods_heart_button(
        goods_for_fav[1]).click()
    from time import sleep
    fav_goods_names_expected = {
        LoginedPage.good_name_text(goods_for_fav[2])}
    LoginedPage.goods_heart_button(
        goods_for_fav[2]).click()
    LoginedPage.goods_heart_button(
        goods_for_fav[1]).click()

    favorite_page = logined_page.fav_page_button_click()
    check.equal(favorite_page.fav_button_counter_text, '1',
                'Количество на странице Избранное')
    assert_goodsnames_in_fav(favorite_page.fav_list, fav_goods_names_expected)


# HELPERS
def assert_goodsnames_in_fav(actual_fav_goods_set, expected_fav_goods_set):
    assert {i.text for i in actual_fav_goods_set} == \
           {i for i in expected_fav_goods_set}, \
           'Набор товаров в избранном равен набору,' \
           'который добавлялся в избранное'

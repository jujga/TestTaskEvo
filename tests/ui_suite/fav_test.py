import pytest
import allure
import pytest_check as check
from tests.pages.pageobjects import LoginedPage, MainPage
import tests.common as common


"""параметризуем массивом индексов товаров и признаком,
добавляем в избранное из списка или из товара"""
@allure.title('Adding some goods to favorites when user is logined')
@pytest.mark.ui
@pytest.mark.parametrize('fav_numbers, add_fav_from_detail',
                         (
                                 ((0, 1), 'add_from_goods_list'),
                                 ((0, 2, 4), 'add_from_goods_list'),
                                 ((2, 5), 'add_from_goods_detail')
                         )
                         )
def test_add2fav(logined_page, fav_numbers: tuple, add_fav_from_detail: str):
# uncomment below and comment above from "@pytest.mark.parametrize" to def test_add2fav to do only one test without parametrize
# def test_add2fav(logined_page, fav_numbers = (0,1), add_fav_from_detail='add_from_goods_detail'):
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
                # with allure.step('Add desired goods to favorites using heart button'):
                #     LoginedPage.goods_heart_button(goods_for_fav[goods_index]).click()
                #     do_allure_attach(f'After clicking on the {goods_index}-th goods/s heart button')
                LoginedPage.click_goods_heart_button(goods_for_fav, goods_index)


            case 'add_from_goods_detail':  # добавляем в избранное c товара
                #with allure.step('Enter into goods details by clicking on the concrete goods'):
                    # проваливаемся в товар
                goodsdetail_page = logined_page.click_on_goods(goods_index)
                # запоминаем товар
                fav_goods_names_expected.append(goodsdetail_page.good_name_txt)
                # with allure.step('Add current goods using heart button'):
                #     goodsdetail_page.fav_add_button.click()
                #     do_allure_screenshot(f'After clicking on the goods/s heart button on the goods detail poge')
                goodsdetail_page.click_fav_add_button()
                # with allure.step('Go back to goods list'):
                goodsdetail_page.click_browser_back_button()
                #    do_allure_screenshot(f'Goods list')

    check.equal(logined_page.fav_button_counter_text,
                str(len(fav_numbers)),
                'Индекс количества элементов в избранном '
                'на странице с товарами')
    # with allure.step('Jump to favorite page'):
    favorite_page = logined_page.click_fav_page_button()
    #    do_allure_screenshot(f'Favorite page')
    check.equal(favorite_page.fav_button_counter_text, str(len(fav_numbers)),
                'Количество элементов в избранном на странице Избранное')
    assert_goodsnames_in_fav(favorite_page.fav_list, fav_goods_names_expected)


# добавляется один товар в избранное без предварительного логина
@pytest.mark.ui
def test_add2fav_out_of_login(main_page):
    goods_index = 1
    # remember goods (for expected result)
    fav_goods_names_expected = \
        {(MainPage.good_name_text(main_page.goods_list[goods_index]))}
    MainPage.click_goods_heart_button(main_page.goods_list, goods_index)
    common.login_steps(main_page)
    logined_page = main_page.go_logined_page()
    check.equal(logined_page.fav_button_counter_text, '1',
                'Количество избранных на кнопке Избранное')
    favorite_page = logined_page.click_fav_page_button()
    check.equal(favorite_page.fav_button_counter_text, '1',
                'Количество на странице Избранное')
    assert_goodsnames_in_fav(favorite_page.fav_list, fav_goods_names_expected)


# добавляется с индексом 1 и 2, с индексом 1 убирается
@pytest.mark.ui
@pytest.mark.parametrize('sequence_of_goods_heart_clicking',
                         (
                                 (1, 2, 1),
                                 (0, 0, 2, 2, 3)
                         )
                         )
def test_add2fav_and_remove(logined_page, sequence_of_goods_heart_clicking: tuple):
    # expected_goods_indices_dict: keys - goods's index in the page, value - flag means resulting adding to the favorites
    # True value - There is odd clicks on the goods according to the given sequence.
    # It means goods will be added to the favorites in sum.
    # False value - There are even clicks.
    # It means goods won't be added to the favorites
    expected_goods_indices_dict = dict()
    for i in sequence_of_goods_heart_clicking:
        if i not in expected_goods_indices_dict: # first definition is True
            expected_goods_indices_dict[i] = True
        else: # inverting of flag when key occurs in the sequence_of_goods_heart_clicking one more time
            expected_goods_indices_dict[i] = not (expected_goods_indices_dict[i])
    expected_goods_indices = set(filter(lambda x: expected_goods_indices_dict[x], expected_goods_indices_dict))
    goods_for_fav = logined_page.goods_list
    fav_goods_names_expected = {LoginedPage.good_name_text(goods_for_fav[i]) for i in expected_goods_indices}
    for goods_index in sequence_of_goods_heart_clicking:
        LoginedPage.click_goods_heart_button(goods_for_fav, goods_index)
    favorite_page = logined_page.click_fav_page_button()
    check.equal(favorite_page.fav_button_counter_text, f'{len(expected_goods_indices)}',
                'Количество на странице Избранное')
    assert_goodsnames_in_fav(favorite_page.fav_list, fav_goods_names_expected)


# HELPERS
@allure.step('Comparing actual favorite list with expected')
def assert_goodsnames_in_fav(actual_fav_goods_set, expected_fav_goods_set):
    assert {i.text for i in actual_fav_goods_set} == {i for i in expected_fav_goods_set}, \
        'Набор товаров в избранном равен набору, который добавлялся в избранное'

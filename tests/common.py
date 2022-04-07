from tests.test_data.credentials import Credentials


def login_steps(main_page):
    main_page.email_button.click()
    main_page.email_field.send_keys(Credentials.login_email)
    main_page.next_button.click()
    main_page.password_field.send_keys(Credentials.login_passw)
    main_page.submit_button_click()

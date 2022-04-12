import allure
import pytest
import requests
import json
from tests.test_data.endpoints import gorest_users_url
from tests.test_data.rest_data import Users
from tests.helpers import get_url_userid
from tests.test_data.rest_data import Config


class RequestComponents:
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 4aa39ba4771752ba989306eb2ef68943963538efeaf4d2feedb7b22ebe3368a7'
    }


@pytest.mark.rest
@allure.title('Creating user. Used method POST')
def test_create_user():

    payload = json.dumps({
        "name": "User for test1",
        "gender": "male",
        "email": "user_for_test1@15ce.com",
        "status": "active"
    })

    response = requests.request(
        'POST', gorest_users_url, headers=RequestComponents.headers, data=payload)
    Config.logger.info(f'response code - {response.status_code}')
    Config.logger.info(f'response body - {response.json()}')

    assert response.status_code == 201
    actual_response = response.json().copy()
    Users.users.append(actual_response.pop('id'))  # get id for delete for teardown
    assert actual_response == \
           {"name": "User for test1",
            "email": "user_for_test1@15ce.com",
            "gender": "male",
            "status": "active"}


@allure.title('Getting user info. Used method GET')
@pytest.mark.rest
def test_get_user():
    user_id = Users.users[0]
    response = requests.request(
        "GET", get_url_userid(gorest_users_url, user_id), headers=RequestComponents.headers)
    Config.logger.info(f'response code - {response.status_code}')
    Config.logger.info(f'response body - {response.json()}')
    assert response.status_code == 200
    assert response.json() == \
           {"id": user_id,
            "name": "User for test_get_user",
            "gender": "male",
            "email": "user_for_test_get_user@15ce.com",
            "status": "active"}


@allure.title('Updating user. Used method PATCH')
@pytest.mark.rest
def test_update_user():
    user_id = Users.users[1]
    payload = json.dumps({
        "name": "Changed Name",
        "email": "changed_mail@15ce.com",
        "status": "inactive"
    })
    response = requests.request(
        'PATCH', get_url_userid(gorest_users_url, user_id), headers=RequestComponents.headers, data=payload)
    Config.logger.info(f'response code - {response.status_code}')
    Config.logger.info(f'response body - {response.json()}')
    assert response.status_code == 200
    assert response.json() == \
           {"id": user_id,
            "name": "Changed Name",
            "email": "changed_mail@15ce.com",
            "gender": "female",
            "status": "inactive"}

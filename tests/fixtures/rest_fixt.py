import pytest
import requests
import json
import logging
import os
from tests.api_suite.rest_test import RequestComponents
from tests.test_data.rest_data import Users
from tests.test_data.endpoints import gorest_users_url
from tests.helpers import get_url_userid
from tests.test_data.rest_data import Config


@pytest.fixture(scope="module", autouse=True)
def create_users(request):
    """create users for tests test_get_user and test_update_user as precondition and delete as teardown.
    Because of absent normal test env
    Users.users[0] - user for test test_get_user (id)
    Users.users[1] - user for test test_update_user (id)"""
    logger_fixt('fixture `create_users`. setup')
    Config.logger.info('==========Setup fixture starts============')
    payload = [
        json.dumps({"name": "User for test_get_user",
                    "gender": "male",
                    "email": "user_for_test_get_user@15ce.com",
                    "status": "active"}),
        json.dumps({"name": "Changed Name",
                    "email": "changed_mail@15ce.com",
                    "gender": "female",
                    "status": "inactive"})
                ]
    for i in range(2):
        response = requests.request(
            'POST', gorest_users_url, headers=RequestComponents.headers, data=payload[i])
        Config.logger.info(f'Created user - response code - {response.status_code}')
        Config.logger.info(f'Created user {response.json()["id"]} - response body - {response.json()}')
        Users.users.append(response.json()['id'])

    def fin():
        logger_fixt('fixture `create_users`. teardown')
        Config.logger.info('==========fixture teardown starts============')
        for i in range(len(Users.users)):
            requests.delete(get_url_userid(gorest_users_url, Users.users[i]), headers=RequestComponents.headers)
            Config.logger.info(f'Deleted user id = {Users.users[i]} - response code - {response.status_code}')
        Config.logger.info('==========fixture ended============')

    request.addfinalizer(fin)


@pytest.fixture(scope="function", autouse=True)
def logger(request):
    os.makedirs(os.path.join('content', 'log'), exist_ok=True)
    log_file = logging.FileHandler(os.path.join('content', 'log', 'test_case.log'))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file.setFormatter(formatter)
    Config.logger = logging.getLogger(request.function.__name__ if type(request) is not str else request)
    Config.logger.setLevel(logging.DEBUG)
    for hdlr in Config.logger.handlers[:]:  # remove all old handlers
        Config.logger.removeHandler(hdlr)
    Config.logger.addHandler(log_file)


# need to think how to combine both logger funcs (logger and logger_fixt) in one func
def logger_fixt(obj):
    os.makedirs(os.path.join('content', 'log'), exist_ok=True)
    log_file = logging.FileHandler(os.path.join('content', 'log', 'test_case.log'))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file.setFormatter(formatter)
    Config.logger = logging.getLogger(obj)
    Config.logger.setLevel(logging.DEBUG)
    for hdlr in Config.logger.handlers[:]:  # remove all old handlers
        Config.logger.removeHandler(hdlr)
    Config.logger.addHandler(log_file)

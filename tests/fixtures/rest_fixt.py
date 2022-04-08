import pytest
import requests
import json
from tests.api_suite.rest_test import RequestComponents
from tests.test_data.rest_data import Users
from tests.test_data.endpoints import gorest_users_url
from tests.helpers import get_url_userid


# create users for tests test_get_user and test_update_user as precondition and delete as teardown. Because of absent
# normal test env
# Users.users[0] - user for test test_get_user (id)
# Users.users[1] - user for test test_update_user (id)
@pytest.fixture(scope="module")
def create_users(request):
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
        Users.users[f'{i}'] = response.json()['id']

    def fin():
        for i in range(2):
            requests.delete(get_url_userid(gorest_users_url, Users.users[f'{i}']), headers=RequestComponents.headers)

    request.addfinalizer(fin)

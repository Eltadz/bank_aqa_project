import requests
import pytest
import random
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateUser:
    def test_create_user(self):

        username = f'Vika{(random.randint(1, 10000))}'
        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd', role='ROLE_USER')
        response = CreateUserRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            ResponseSpecs.request_ok()
        ).post(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role



    # Тест на не валидного пользователя
    @pytest.mark.parametrize(
        'username, password',
        [
            ('qi', 'Pas!sw0rd2'),
            ('Weridwirrfwehf9whfwwwqww', 'Pas!sw0rd1'),
            ('Qer!1', 'Pas!sw0rdd'),
            ('Qer?', 'pas!sw0rdd'),
            ('Qer44', 'PASSWORD!0'),
            ('Q443', 'Passw0rdd'),
            ('Qer2!', 'Passw0rdd1'),
        ]
    )


    def test_create_user_invalid(self, username, password):


        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd', role='ROLE_USER')
        response = CreateUserRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            ResponseSpecs.request_bad()
        ).post(create_user_request)
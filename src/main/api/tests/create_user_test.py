import requests
import pytest
import random
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest



@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        'username, password',
        [
            ('qew454', 'Pas!sw0rd2'),
            ('ppep43w4r', 'Pas!sw0rd1'),
            ('qw1234r4e', 'Pas!sw0rdd'),

        ]
    )
    # ЗАХОДИМ ПОД КРЕДАМИ АДМИНА
    def test_create_user_valid(self, username, password):
        login_user_request = LoginUserRequest(username='admin', password='123456')
        login_admin_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        assert login_admin_response.status_code == 200
        admin_token = login_admin_response.json().get('token')


        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd', role='ROLE_USER')
        response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json=create_user_request.model_dump(), #ЗАПАКОВЫВАЕМ В json
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )
        assert response.status_code == 200
        create_user_response = CreateUserResponse(**response.json()) #РАСПАКОВЫВАЕМ ОТВЕТ
        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role

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
    # ЗАХОДИМ ПОД КРЕДАМИ АДМИНА
    # Тест на не валидного пользователя]
    def test_create_user_invalid(self, username, password):
        login_user_request = LoginUserRequest(username='admin', password='123456')
        login_admin_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        assert login_admin_response.status_code == 200
        admin_token = login_admin_response.json().get('token')

        # СОЗДАЕМ НА АДМИНЕ ЮСЕРА
        create_user_request = CreateUserRequest(username=username, password=password, role='ROLE_USER')
        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json=create_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )
        assert create_user_response.status_code == 400
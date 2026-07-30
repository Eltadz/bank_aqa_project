import requests
import pytest
import random

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


@pytest.mark.api
class TestLoginUser:
    def test_login_user(self):
        # ЗАХОДИМ ПОД КРЕДАМИ АДМИНА
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



        # СОЗДАЕМ НА ЮСЕРЕ ЕМУ АККАУНТ В БАНКЕ
        username = f'Vikos{random.randint(0,1000)}'
        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd', role='ROLE_USER')
        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json=create_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )
        assert create_user_response.status_code == 200


        # ЛОГИНИМСЯ ЮСЕРОМ ПОД СОЗДАННЫМИ КРЕДАМИ НА АДМИНЕ
        login_user_request = LoginUserRequest(username=username, password='Pas!sw0rd')
        response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        assert response.status_code == 200
        login_user_response = LoginUserResponse(**response.json())
        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == 'ROLE_USER'





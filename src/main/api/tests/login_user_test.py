import requests
import pytest
import random

class TestLoginUser:
    def test_login_user(self):
        # ЗАХОДИМ ПОД КРЕДАМИ АДМИНА
        login_admin_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json={
                'username': 'admin',
                'password': '123456'
            },
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        assert login_admin_response.status_code == 200
        admin_token = login_admin_response.json().get('token')

        # СОЗДАЕМ НА ЮСЕРЕ ЕМУ АККАУНТ В БАНКЕ
        username = f'Vikos{random.randint(0,1000)}'
        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json={
                'username':username,
                'password': 'Pas!sw0rd',
                'role': 'ROLE_USER'
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )
        assert create_user_response.status_code == 200


        # ЛОГИНИМСЯ ЮСЕРОМ ПОД СОЗДАННЫМИ КРЕДАМИ НА АДМИНЕ
        login_user_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json={
                'username': username,
                'password': 'Pas!sw0rd'
            },
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        assert login_user_response.status_code == 200
        assert login_user_response.json().get('username') == username
        assert login_user_response.json().get('password') == 'Pas!sw0rd'





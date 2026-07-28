import requests
import pytest
import random


class TestCreateAccount:
    # логин админом
    def test_create_account(self):
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


        # СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ НА АДМИНЕ
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
        assert create_user_response.json().get('username') == username
        assert create_user_response.json().get('role') == 'ROLE_USER'   


        # ЗАХОДИМ ЛОГИЕНИМСЯ ЮСЕРОМ
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
        user_token = login_user_response.json().get('token')


        # СОЗДАЕМ НА ЮСЕРЕ ЕМУ АККАУНТ В БАНКЕ
        create_bank_account_response = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert create_bank_account_response.status_code == 201
        assert create_bank_account_response.json().get('balance') == 0
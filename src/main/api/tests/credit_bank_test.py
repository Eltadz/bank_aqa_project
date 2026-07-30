import requests
import pytest
import random

@pytest.mark.api
class TestCreditBank:
    @pytest.mark.parametrize(
        'credit_amount',
        [
            5000,
            15000,
            10000,
            7000
        ]
    )
    def test_deposit_credit_bank_valid(self, credit_amount):
        # аунтификация как админ с данными кредами
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



        # создание на токене админа юзера с ролью кредит
        username = f'Vikos{random.randint(0, 1000)}'
        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json={
                'username': username,
                'password': 'Pas!sw0rd',
                'role': 'ROLE_CREDIT_SECRET'
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )
        assert create_user_response.status_code == 200

        # регистрация юзером чтобы взять его токен и создать счет
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



        # создание счета в банке чтобы на него взять кредит
        create_bank_account_response = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert create_bank_account_response.status_code == 201
        account_id = create_bank_account_response.json().get('id')

        # взял кредит на созданный аккаунт
        create_credit_account_response = requests.post(
            url='http://localhost:4111/api/credit/request',
            json={
                "accountId": account_id,
                "amount": credit_amount,
                "termMonths": 12
            },
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert create_credit_account_response.status_code == 201
        assert create_credit_account_response.json().get('balance') == credit_amount
        assert create_credit_account_response.json().get('termMonths') == 12
        # credit_id = create_credit_account_response.json()['creditId']

    @pytest.mark.parametrize(
        'credit_amount',
        [
            4999,
            15001,
            500,
            19000
        ]
    )
    def test_deposit_credit_bank_invalid(self, credit_amount):
        # аунтификация как админ с данными кредами
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

        # создание на токене админа юзера с ролью кредит
        username = f'Vikos{random.randint(0, 1000)}'
        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json={
                'username': username,
                'password': 'Pas!sw0rd',
                'role': 'ROLE_CREDIT_SECRET'
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )
        assert create_user_response.status_code == 200

        # регистрация юзером чтобы взять его токен и создать счет
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

        # создание счета в банке чтобы на него взять кредит
        create_bank_account_response = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert create_bank_account_response.status_code == 201
        account_id = create_bank_account_response.json().get('id')

        # взял кредит на созданный аккаунт
        create_credit_account_response = requests.post(
            url='http://localhost:4111/api/credit/request',
            json={
                "accountId": account_id,
                "amount": credit_amount,
                "termMonths": 12
            },
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert create_credit_account_response.status_code == 400



    @pytest.mark.parametrize(
        'credit_amount, repayment_amount',
        [
            (5000,5000),
            (15000,15000),
        ]
    )

    # ТЕСТ НА ПОГАШЕНИЕ КРЕДИТА ВАЛИДНЫЙ
    def test_repayment_credit_bank_valid(self, credit_amount, repayment_amount):
        # аунтификация как админ с данными кредами
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

        #создание на токене админа юзера с ролью кредит
        username = f'Vikos{random.randint(0, 1000)}'
        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json={
                'username': username,
                'password': 'Pas!sw0rd',
                'role': 'ROLE_CREDIT_SECRET'
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )
        assert create_user_response.status_code == 200

        # регистрация юзером чтобы взять его токен и создать счет
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

        # создание счета в банке чтобы на него взять кредит
        create_bank_account_response = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert create_bank_account_response.status_code == 201
        account_id = create_bank_account_response.json().get('id')

        # взял кредит на созданный аккаунт
        deposit_credit_account_response = requests.post(
            url='http://localhost:4111/api/credit/request',
            json={
                "accountId": account_id,
                "amount": credit_amount,
                "termMonths": 12
            },
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert deposit_credit_account_response.status_code == 201
        credit_id = deposit_credit_account_response.json().get('creditId')

        #погашение кредита
        repayment_credit_account_response = requests.post(
            url='http://localhost:4111/api/credit/repay',
            json={
                "creditId": credit_id,
                "accountId": account_id,
                "amount": repayment_amount
            },
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert repayment_credit_account_response.status_code == 200
        assert repayment_credit_account_response.json().get('amountDeposited') == repayment_amount

    @pytest.mark.parametrize(
        'credit_amount, repayment_amount',
        [
            (10000, 5000),
            (7000, 6000),
        ]
    )
    # ТЕСТ НА ПОГАШЕНИЕ КРЕДИТА НЕ ВАЛИДНЫЙ
    def test_repayment_credit_bank_invalid(self, credit_amount, repayment_amount):
        # аунтификация как админ с данными кредами
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

        # создание на токене админа юзера с ролью кредит
        username = f'Vikos{random.randint(0, 1000)}'
        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json={
                'username': username,
                'password': 'Pas!sw0rd',
                'role': 'ROLE_CREDIT_SECRET'
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )
        assert create_user_response.status_code == 200

        # регистрация юзером чтобы взять его токен и создать счет
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

        # создание счета в банке чтобы на него взять кредит
        create_bank_account_response = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert create_bank_account_response.status_code == 201
        account_id = create_bank_account_response.json().get('id')

        # взял кредит на созданный аккаунт
        deposit_credit_account_response = requests.post(
            url='http://localhost:4111/api/credit/request',
            json={
                "accountId": account_id,
                "amount": credit_amount,
                "termMonths": 12
            },
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert deposit_credit_account_response.status_code == 201
        credit_id = deposit_credit_account_response.json().get('creditId')

        # погашение кредита
        repayment_credit_account_response = requests.post(
            url='http://localhost:4111/api/credit/repay',
            json={
                "creditId": credit_id,
                "accountId": account_id,
                "amount": repayment_amount
            },
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert repayment_credit_account_response.status_code == 422














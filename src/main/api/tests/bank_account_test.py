import requests
import pytest
import random


from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_bank_account_request import DepositBankAccountRequest
from src.main.api.models.deposit_bank_account_response import DepositBankAccountResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.transfer_bank_account_request import TransferBankAccountRequest
from src.main.api.models.transfer_bank_account_response import TransferBankAccountResponse


@pytest.mark.api
class TestBankAccount:
    @pytest.mark.parametrize(
        'amount',
        [
            1000,
            9000,
            8000
        ]

    )
    def test_deposit_account_valid(self,amount):
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



        username = f'Vikos{random.randint(0,1000)}'
        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd',role='ROLE_USER')
        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json=create_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )
        assert create_user_response.status_code == 200

        login_user_request = LoginUserRequest(username=username, password='Pas!sw0rd')
        login_user_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        assert login_user_response.status_code == 200
        user_token = login_user_response.json().get('token')



        create_bank_account_response = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert create_bank_account_response.status_code == 201
        account_id = create_bank_account_response.json().get('id')

        deposit_bank_account_request = DepositBankAccountRequest(accountId=account_id, amount=amount)
        response = requests.post(
            url='http://localhost:4111/api/account/deposit',
            json=deposit_bank_account_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert response.status_code == 200
        deposit_bank_account_response = DepositBankAccountResponse(**response.json())
        assert deposit_bank_account_response.balance == amount





    # Негативный тест на депозит
    @pytest.mark.parametrize(
        'amount',
        [
            999,
            9001,
            500,
            10000
        ]

    )
    def test_deposit_account_invalid(self, amount):
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

        username = f'Vikos{random.randint(0, 1000)}'
        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd',role='ROLE_USER')
        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json=create_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )
        assert create_user_response.status_code == 200


        login_user_request = LoginUserRequest(username=username, password='Pas!sw0rd')
        login_user_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        assert login_user_response.status_code == 200
        user_token = login_user_response.json().get('token')


        create_bank_account_response = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert create_bank_account_response.status_code == 201
        account_id = create_bank_account_response.json().get('id')


        deposit_bank_account_request = DepositBankAccountRequest(accountId=account_id, amount=amount)
        deposit_account_response = requests.post(
            url='http://localhost:4111/api/account/deposit',
            json=deposit_bank_account_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert deposit_account_response.status_code == 400











    # Тест на трансфер

    @pytest.mark.parametrize(
        'amount',
        [
            10000,
            500,
            5000,
            7000
        ]
    )
    def test_transfer_account_valid(self, amount):
        # логинюсь админом чтобы создать юзера
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


        # создаю юзера на админе
        username = f'Vikos{random.randint(0,100000)}'
        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd',role='ROLE_USER')
        create_user_response = requests.post(
            url='http://localhost:4111/api/admin/create',
            json=create_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {admin_token}'
            }
        )
        assert create_user_response.status_code == 200


        # логинюсь юсером
        login_user_request = LoginUserRequest(username=username, password='Pas!sw0rd')
        login_user_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        assert login_user_response.status_code == 200
        user_token = login_user_response.json().get('token')



        #создание первого аккаунта
        create_account_one = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert create_account_one.status_code == 201
        account_id_one = create_account_one.json().get('id')

        #создание второго аккаунта
        create_account_two = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert create_account_two.status_code == 201
        account_id_two = create_account_two.json().get('id')


        # пополнение счета аккаунта первый раз
        deposit_bank_account_request = DepositBankAccountRequest(accountId=account_id_one, amount=9000)
        deposit_account_response_one = requests.post(
            url='http://localhost:4111/api/account/deposit',
            json=deposit_bank_account_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert deposit_account_response_one.status_code == 200

        # пополнение счета аккаунта второй раз
        deposit_bank_account_request = DepositBankAccountRequest(accountId=account_id_one, amount=9000)
        deposit_account_response_one = requests.post(
            url='http://localhost:4111/api/account/deposit',
            json={
                "accountId": account_id_one,
                "amount": 9000
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert deposit_account_response_one.status_code == 200
        deposit_account = deposit_account_response_one.json().get('balance')



        #перевод между счетами с одного аккаунта на другой
        transfer_bank_account_request = TransferBankAccountRequest(fromAccountId=account_id_one, toAccountId=account_id_two, amount=amount)
        response = requests.post(
            url='http://localhost:4111/api/account/transfer',
            json=transfer_bank_account_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert response.status_code == 200
        transfer_account_response = TransferBankAccountResponse(**response.json())
        assert transfer_account_response.fromAccountIdBalance == deposit_account - amount



















    # негативный тест
    @pytest.mark.parametrize(
        'amount',
        [
            10001,
            499,
            17000,
            201
        ]
    )
    def test_transfer_account_invalid(self, amount):
        # логинюсь админом чтобы создать юзера
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

        # создаю юзера на админе
        username = f'Vikos{random.randint(0, 100000)}'
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
        assert create_user_response.json().get('username') == username
        assert create_user_response.json().get('role') == 'ROLE_USER'

        # логинюсь юсером
        login_user_request = LoginUserRequest(username=username, password='Pas!sw0rd')
        login_user_response = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=login_user_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        assert login_user_response.status_code == 200
        user_token = login_user_response.json().get('token')


        # создание первого счета у аккаунта
        create_account_one = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )

        assert create_account_one.status_code == 201
        account_id_one = create_account_one.json()['id']

        # создание второго счета у аккаунта
        create_account_two = requests.post(
            url='http://localhost:4111/api/account/create',
            headers={
                'accept': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert create_account_two.status_code == 201
        account_id_two = create_account_two.json()['id']

        # пополнение счета аккаунта первый раз
        deposit_bank_account_request = DepositBankAccountRequest(accountId=account_id_one, amount=9000)
        deposit_account_response_one = requests.post(
            url='http://localhost:4111/api/account/deposit',
            json=deposit_bank_account_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert deposit_account_response_one.status_code == 200

        # пополнение счета аккаунта второй раз
        deposit_bank_account_request = DepositBankAccountRequest(accountId=account_id_one, amount=9000)
        deposit_account_response_one = requests.post(
            url='http://localhost:4111/api/account/deposit',
            json=deposit_bank_account_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert deposit_account_response_one.status_code == 200
        deposit_account = deposit_account_response_one.json()['balance']

        # перевод между счетами с одного аккаунта на другой
        transfer_account_request = TransferBankAccountRequest(fromAccountId=account_id_two, toAccountId=account_id_one, amount=amount)
        transfer_account_response = requests.post(
            url='http://localhost:4111/api/account/transfer',
            json=transfer_account_request.model_dump(),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {user_token}'
            }
        )
        assert transfer_account_response.status_code == 400







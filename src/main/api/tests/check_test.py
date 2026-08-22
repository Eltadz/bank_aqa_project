
import requests
import pytest
import random

from src.main.api.models.create_account_response import CreateAccountResponse

from src.main.api.models.deposit_bank_account_request import DepositBankAccountRequest
from src.main.api.models.deposit_bank_account_response import DepositBankAccountResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.transfer_bank_account_request import TransferBankAccountRequest
from src.main.api.models.transfer_bank_account_response import TransferBankAccountResponse

from uuid import uuid4

from src.main.api.models.create_user_request import CreateUserRequest

from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_bank_account_requester import DepositBankAccountRequester
from src.main.api.requests.transfer_account_requester import TransferBankAccountRequester

from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.creat_account_requester import CreateAccountRequester







@pytest.mark.api
class TestBankAccount:

    #                                             ПОЗИТИВНЫЙ ТЕСТ НА ТРАНСФЕР


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
        # создание юсера
        username = f'Vika{uuid4().hex[:10]}'
        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd', role='ROLE_USER')
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # создаем аккаунт первый
        response_create_account_one = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id_one = response_create_account_one.id

        # создаем второй аккаунт
        response_create_account_two = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id_two = response_create_account_two.id

        # ПОПОЛНЕНИЕ СЧЕТА первый раз
        deposit_bank_account_request = DepositBankAccountRequest(accountId=account_id_one, amount=9000)
        deposit_response_one = DepositBankAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_bank_account_request)

        # ПОПОЛНЕНИЕ СЧЕТА второй раз
        deposit_bank_account_request = DepositBankAccountRequest(accountId=account_id_one, amount=9000)
        deposit_response_two = DepositBankAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_bank_account_request)
        deposit_account_response = deposit_response_two.balance


        # перевод между счетами
        transfer_bank_account_request = TransferBankAccountRequest(fromAccountId=account_id_one, toAccountId=account_id_two, amount=amount)
        response = TransferBankAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_bank_account_request)

        assert response.fromAccountIdBalance == deposit_account_response - amount









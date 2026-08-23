
from uuid import uuid4
import pytest


from src.main.api.requests.repayment_credit_requester import RepaymentCreditRequester
from src.main.api.models.repayment_credit_request import RepaymentCreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.creat_account_requester import CreateAccountRequester
from src.main.api.models.deposit_credit_account_request import DepositCreditAccountRequest
from src.main.api.requests.deposit_credit_account_requester import DepositCreditAccountRequester


@pytest.mark.api
class TestCreditBank:


    #                                     ВАЛИДНЫЙ ТЕСТ НА ПОЛУЧЕНИЕ КРЕДИТА


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
        # создание юсера
        username = f'Vika{uuid4().hex[:10]}'
        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # создаем аккаунт
        response_create_account = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = response_create_account.id


        # взял кредит на созданный аккаунт
        deposit_credit_account_request = DepositCreditAccountRequest(accountId=account_id, amount=credit_amount, termMonths=12)
        response = DepositCreditAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(deposit_credit_account_request)

        assert deposit_credit_account_request.amount == response.balance
        assert deposit_credit_account_request.termMonths == response.termMonths











    #                                НЕВАЛИДНЫЙ ТЕСТ НА ПОЛУЧЕНИЕ КРЕДИТА


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

        # создание юсера
        username = f'Vika{uuid4().hex[:10]}'
        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # создаем аккаунт
        response_create_account = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = response_create_account.id


        # взял кредит на созданный аккаунт
        deposit_credit_account_request = DepositCreditAccountRequest(accountId=account_id, amount=credit_amount, termMonths=12)
        response = DepositCreditAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_bad()
        ).post(deposit_credit_account_request)
















    #                                           ТЕСТ НА ПОГАШЕНИЕ КРЕДИТА ВАЛИДНЫЙ
    @pytest.mark.parametrize(
        'credit_amount, repayment_amount',
        [
            (5000,5000),
            (15000,15000),
        ]
    )


    def test_repayment_credit_bank_valid(self, credit_amount, repayment_amount):
        # создание юсера
        username = f'Vika{uuid4().hex[:10]}'
        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # создаем аккаунт
        response_create_account = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = response_create_account.id

        # взял кредит на созданный аккаунт
        deposit_credit_account_request = DepositCreditAccountRequest(accountId=account_id, amount=credit_amount, termMonths=12)
        response_deposit = DepositCreditAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(deposit_credit_account_request)
        credit_id = response_deposit.creditId



        #погашение кредита
        repayment_credit_request = RepaymentCreditRequest(creditId=credit_id, accountId=account_id, amount=repayment_amount)
        response = RepaymentCreditRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_ok()
        ).post(repayment_credit_request)


        assert repayment_credit_request.amount == response.amountDeposited










    #                                           НЕВАЛИДНЫЙ ТЕСТ НА ПОГАШЕНИЕ КРЕДИТА
    @pytest.mark.parametrize(
        'credit_amount, repayment_amount',
        [
            (10000, 5000),
            (7000, 6000),
        ]
    )

    def test_repayment_credit_bank_invalid(self, credit_amount, repayment_amount):
        # создание юсера
        username = f'Vika{uuid4().hex[:10]}'
        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd', role='ROLE_CREDIT_SECRET')
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # создаем аккаунт
        response_create_account = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = response_create_account.id

        # взял кредит на созданный аккаунт
        deposit_credit_account_request = DepositCreditAccountRequest(accountId=account_id, amount=credit_amount, termMonths=12)
        response_deposit = DepositCreditAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post(deposit_credit_account_request)
        credit_id = response_deposit.creditId

        # погашение кредита
        repayment_credit_request = RepaymentCreditRequest(creditId=credit_id, accountId=account_id, amount=repayment_amount)
        response = RepaymentCreditRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_422()
        ).post(repayment_credit_request)














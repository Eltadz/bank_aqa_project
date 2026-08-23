import pytest
from uuid import uuid4


from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.requests.creat_account_requester import CreateAccountRequester


@pytest.mark.api
class TestCreateBankAccount:
    def test_create_bank_account(self):

       # создание юсера
        username = f'Vika{uuid4().hex[:10]}'
        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd', role='ROLE_USER')
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)


        
       # создаем аккаунт
        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password='Pas!sw0rd'),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0
        id_account = response.id

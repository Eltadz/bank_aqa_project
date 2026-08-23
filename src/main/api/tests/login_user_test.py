import pytest
from uuid import uuid4


from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs




@pytest.mark.api
class TestLoginUser:
    def test_login_user(self):
        username = f'Vika{uuid4().hex[:10]}'
        create_user_request = CreateUserRequest(username=username, password='Pas!sw0rd', role='ROLE_USER')
        CreateUserRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            ResponseSpecs.request_ok()
        ).post(create_user_request)


        login_user_request = LoginUserRequest(username=username, password='Pas!sw0rd')
        response = LoginUserRequester(
            RequestSpecs.unauthorized_headers(),
            ResponseSpecs.request_ok()
        ).post(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == 'ROLE_USER'
















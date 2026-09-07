from foundation import endpoint
from foundation.endpoint import Endpoint
from foundation.requesters.crud_requester import CrudRequester
from foundation.requesters.validate_crud_requester import ValidateCrudRequester
from models.create_user_request import CreateUserRequest
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs








class AdminSteps(BaseSteps):
    def create_user_valid(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        ).post(create_user_request)


        self.created_obj.append(response)
        return response


    def delete_user(self, user_id: int):
        CrudRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_ok()
        ).delete(user_id)



from models.create_user_request import CreateUserRequest
from foundation.requesters.validate_crud_requester import ValidateCrudRequester
from specs.request_specs import RequestSpecs
from specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps






class AdminSteps(BaseSteps):

    def create_user(self,create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username='admin', password='123456'),
            endpoint=create_user_request.endpoint,
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)




        self.created_obj.append(response)
        return response
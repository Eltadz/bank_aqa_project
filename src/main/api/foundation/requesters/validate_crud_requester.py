from models.base_model import BaseModel
from src.main.api.foundation.http_requester import HTTPRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester












# супер вообще тут не нужен, он нужен для того если мы хотим взять и добавить свои данные
class ValidateCrudRequester(HTTPRequester):
    def __init_(self,request_spec, endpoint, response_spec): # берем общую настройку родителя
        super().__init__(request_spec, endpoint, response_spec)# можем добавить что то свое
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )

    def post(self, model: BaseModel) -> BaseModel:
        response = self.crud_requester.post(model)
        self.response_spec(response)
        return self.endpoint.value.response_model.validate(response.json())

    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

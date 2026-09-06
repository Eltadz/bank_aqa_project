from src.main.api.configs.config import Config
from typing import Optional
from requests import Response
from foundation.http_requester import HTTPRequester
from models.base_model import BaseModel
import requests









# для негативных сценариев где нужен сырой ответ


class CrudRequester(HTTPRequester):
    def post(self,  model: Optional[BaseModel]) -> Response:
        body = model.model_dump() if model is not None else ''

        response = requests.post(
            url=f'{Config.fetch('backendUrl')}{self.endpoint.value.url}',
            json=body,
            headers=self.request_spec
        )
        self.response_spec(response)
        return response


    def delete(self, user_id: int) -> Response:
        response = requests.delete(
            url=f'{Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id}',
            headers=self.request_spec
        )
        self.response_spec(response)
        return response
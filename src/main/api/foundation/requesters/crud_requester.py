from src.main.api.configs.config import Config
from typing import Optional
from requests import Response
from foundation.http_requester import HTTPRequester
from models.base_model import BaseModel
import requests







# у каждого класса должна быть своя зона ответственности, важное разделение
# CrudRequester отвечает за HTTP-действие: собрать запрос, отправить его, получить Response, проверить ожидаемый status code
# для негативных сценариев где нужен сырой ответ

# транспортный HTTP уровень, все проходит через crud потом ток в validate если есть данные для валидации через пайдентик модели
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
from http import HTTPStatus

from requests import Response
import requests

from src.main.api.requests.requester import Requester
from src.main.api.models.deposit_credit_account_request import DepositCreditAccountRequest
from src.main.api.models.deposit_credit_account_response import DepositCreditAccountResponse

class DepositCreditAccountRequester(Requester):
    def post(self, deposit_credit_account_request: DepositCreditAccountRequest) -> DepositCreditAccountResponse | Response:
        url = f'{self.base_url}/credit/request'
        response = requests.post(
            url=url,
            json = deposit_credit_account_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return DepositCreditAccountResponse(**response.json())
        return response
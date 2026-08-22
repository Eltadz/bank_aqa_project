from http import HTTPStatus

import requests
from requests import Response

from src.main.api.models.deposit_bank_account_request import DepositBankAccountRequest
from src.main.api.models.deposit_bank_account_response import DepositBankAccountResponse
from src.main.api.requests.requester import Requester


class DepositBankAccountRequester(Requester):
    def post(self, deposit_bank_account_request: DepositBankAccountRequest) -> DepositBankAccountResponse | Response:
        url=f'{self.base_url}/account/deposit'
        response = requests.post(
            url=url,
            json=deposit_bank_account_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code == HTTPStatus.OK:
            return DepositBankAccountResponse(**response.json())
        return response

from http import HTTPStatus

import requests
from requests import Response

from src.main.api.models.transfer_bank_account_request import TransferBankAccountRequest
from src.main.api.models.transfer_bank_account_response import TransferBankAccountResponse
from src.main.api.requests.requester import Requester


class TransferBankAccountRequester(Requester):
    def post(self, transfer_bank_account_request: TransferBankAccountRequest) -> TransferBankAccountResponse | Response:
        url=f'{self.base_url}/account/transfer'
        response = requests.post(
            url=url,
            json=transfer_bank_account_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code == HTTPStatus.OK:
            return TransferBankAccountResponse(**response.json())
        return response.text
from http import HTTPStatus
import requests
from requests import Response

from src.main.api.requests.requester import Requester
from src.main.api.models.repayment_credit_request import RepaymentCreditRequest
from src.main.api.models.repayment_credit_response import RepaymentCreditResponse




class RepaymentCreditRequester(Requester):
    def post(self, repayment_credit_request: RepaymentCreditRequest) -> RepaymentCreditResponse | Response:
        url = f'{self.base_url}/credit/repay'
        response = requests.post(
            url=url,
            json=repayment_credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return RepaymentCreditResponse(**response.json())
        return response.text


from requests import Response
from http import HTTPStatus



class ResponseSpecs:
    # 200
    @staticmethod
    def request_ok():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    # 201
    @staticmethod
    def request_created():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text

        return confirm

    # 400
    @staticmethod
    def request_bad():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text

        return confirm



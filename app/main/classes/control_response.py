import json
from app.main.utils.constants_messages import ERROR_MESSAGE


class ControlResponse:

    def __init__(self):
        self.status = None
        self.data_response = None
        self.code = None

    def success_request(self, response, dumps_json=False) -> dict():
        self.status = True
        self.code = response.status_code
        if dumps_json:
            self.data_response = json.dumps(response.json())
        else:
            self.data_response = response.json()
        return self.return_response()

    def success_data(self, data: dict) -> dict():
        self.status = True
        self.data_response = data
        self.code = 200
        return self.return_response()

    def false_status(self, message: str, code: str) -> dict():
        self.status = False
        data = dict(
            status=self.status,
            code=code,
            message=message)
        self.data_response = data
        self.code = 200
        return self.return_response()

    def not_found_data(self, message: str) -> dict():
        self.status = False
        self.data_response = (dict(message=message))
        self.code = 404
        return self.return_response()

    def bad_request(self, message) -> dict():
        self.status = False
        self.data_response = dict(message=message)
        self.code = 400
        return self.return_response()

    def internal_error(self, message=ERROR_MESSAGE['UNEXPECTED_ERROR']):
        self.status = False
        self.data_response = dict(message=message)
        self.code = 500
        return self.return_response()

    def return_response(self) -> dict:
        return dict(
            status=self.status,
            message=self.data_response,
            code=self.code)

from flask_restx import Resource
import flask


class IController(Resource):
    @staticmethod
    def _default_response(data: dict, status_code: int):
        print('content', data)

        response = flask.make_response(data)
        response.status_code = status_code
        response.headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
            'content-type': '*'
        }

        return response

    def custom_response(self, data: dict = {}, status_code: int = 200):
        print('content', data)

        try:
            return self._default_response(data, status_code)
        except  Exception as e:
            return e

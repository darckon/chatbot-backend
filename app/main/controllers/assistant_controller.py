from app.main.services.assistant_service import AssistantService
from app.main.utils.constants_messages import ERROR_MESSAGE
from app.main.view_models.model import CreateSchema, PromptSchema
from app.main.infra.dbm import PSQLConnection

from .i_controller import IController
from ..utils.dto import MSAssistant
from flask import request
import logging, json

ms_assistant = MSAssistant.api


# create
@ms_assistant.route("/create")
class CreateController(IController):
    @ms_assistant.doc("create json form")
    def post(self):
        logging.info(f"in -> {request.url}")
        content = request.json
        schema = CreateSchema()
        try:
            data = schema.load(content)
            response = AssistantService.create(data)
            logging.info(f"out -> {request.url} -> {str(response['message'])}")
            return self.custom_response(
                data=response['message'],
                status_code=response['code'])

        except Exception as e:
            logging.exception(e)
            return self.custom_response(
                {'message': ERROR_MESSAGE['UNEXPECTED_ERROR']},
                status_code=400)


# update
@ms_assistant.route("/update/<string:id>")
class UpdateController(IController):
    @ms_assistant.doc("update json form")
    def patch(self, id):
        logging.info(f"in -> {request.url}")
        content = request.json
        schema = CreateSchema()
        try:
            data = schema.load(content)
            response = AssistantService.update(id, data)
            logging.info(f"out -> {request.url} -> {str(response['message'])}")
            return self.custom_response(
                data=response['message'],
                status_code=response['code'])

        except Exception as e:
            logging.exception(e)
            return self.custom_response(
                {'message': ERROR_MESSAGE['UNEXPECTED_ERROR']},
                status_code=400)


# FindForm
@ms_assistant.route("/find-form/<string:user>/<string:institution>")
class FindformController(IController):
    @ms_assistant.doc("find json form")
    def get(self, user, institution):
        logging.info(f"in -> {request.url}")
        try:
            response = AssistantService.find_form(user, institution)
            logging.info(f"out -> {request.url} -> {str(response['message'])}")
            return self.custom_response(
                data=response['message'],
                status_code=response['code'])

        except Exception as e:
            logging.exception(e)
            return self.custom_response(
                {'message': ERROR_MESSAGE['UNEXPECTED_ERROR']},
                status_code=400)

# prompt
@ms_assistant.route("/prompt")
class PromptController(IController):
    @ms_assistant.doc("question some")
    def post(self):
        try:
            logging.info(f"in -> {request.url}")
            content = json.loads(request.data)
            print('content', content)
            
            response = AssistantService().prompt_file(content['promptGpt'])
            logging.info(response)
            logging.info(f"out -> {request.url} -> {str(response['message'])}")
            return self.custom_response(
                data=response['message'],
                status_code=response['code'])

        except Exception as e:
            print(e)
            logging.exception(e)
            return self.custom_response(
                {'message': ERROR_MESSAGE['UNEXPECTED_ERROR']},
                status_code=400)

import logging
import os
import sys
from app.main.collections.assistant_collection import JsonForm
from app.main.classes.control_response import ControlResponse
from app.main.utils.constants_messages import SUCCESS_MESSAGE
from langchain_community.document_loaders import TextLoader
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from flask import current_app as app


class AssistantService:
    def __init__(self):
        self.chat = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))
        pass

    @staticmethod
    def create(data: str):
        logging.info(f"in -> create_json_form({str(data)})")

        try:
            json_form = JsonForm.create(
                user=data['user'],
                institution=data['institution'],
                content=data['content'],
                module=data['module'],
                available=data['available'],
                )
            return ControlResponse().success_data(
                dict(result=json_form.to_json()))
        except Exception as e:
            logging.exception(e)
            return ControlResponse().internal_error()

    def update(id: str, data: str):
        logging.info(f"in -> update_json_form({str(id)}, {str(data)})")

        try:
            JsonForm.update(
                id=id,
                user=data['user'],
                institution=data['institution'],
                content=data['content'],
                module=data['module'],
                available=data['available'],
                )
            return ControlResponse().success_data(
                {'message': SUCCESS_MESSAGE['CREATE_LOG']})
        except Exception as e:
            logging.exception(e)
            return ControlResponse().internal_error()

    def find_form(user: str, institution: str):
        logging.info(f"in -> find_json_form({str(user)}-{str(institution)})")

        try:
            json_form = JsonForm.find_form(user, institution)
            if json_form:
                json_form = json_form.to_json()

            return ControlResponse().success_data(
                dict(result=json_form))
        except Exception as e:
            logging.exception(e)
            return ControlResponse().internal_error()

    def prompt_file(self, data: str, chat_history=None):
        print(f"in -> service_prompt({str(data)})")
        logging.info(f"in -> service_prompt({str(data)})")

        try:
            logging.info(f"in -> service_prompt({str(data)})")

            loader = TextLoader("app/main/utils/data/knowlege.txt")
            iflab_doc = loader.load()[0].page_content
            template = "{chatbot}: {question}. Esta es la fuente de tu conocimiento: {knowledge}. Recuerda tienes que estar en el rol de Orbis un chatbot agradable creado por Iflab:"
            prompt = ChatPromptTemplate.from_messages([
                HumanMessagePromptTemplate.from_template(template)])

            print(prompt)
            formated_prompt = prompt.format_messages(
                chatbot='Responde la siguiente pregunta:',
                question=data,
                knowledge=iflab_doc
            )

            answer = self.chat.invoke(formated_prompt)

            return ControlResponse().success_data(
                {'message': {'answer': answer.content}})

        except Exception as e:
            logging.exception(e)
            return ControlResponse().internal_error()

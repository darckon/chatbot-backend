import openai
import logging
import os
import sys
from app.main.collections.assistant_collection import JsonForm
from app.main.classes.control_response import ControlResponse
from app.main.utils.constants_messages import SUCCESS_MESSAGE
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain.prompts.prompt import PromptTemplate


class AssistantService:
    def __init__(self):
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
            PERSIST = False
            query = None

            if PERSIST and os.path.exists("persist"):
                print("Reusing index...\n")
                vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
                index = VectorStoreIndexWrapper(vectorstore=vectorstore)
            else:
                loader = TextLoader("app/main/utils/data/source.txt") # Use this line if you only need data.txt
                #loader = DirectoryLoader(".", glob="app/main/utils/data/*.txt")
            if PERSIST:
                index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
            else:
                index = VectorstoreIndexCreator().from_loaders([loader])

            chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model="gpt-3.5-turbo"),
            verbose=True,
            retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
            )
            new_chat_history = []
            #for i, item in chat_history:
            #    new_chat_history.append((i, item))
            #query = f"Prompt: 1.- Recuerda siempre añadir esto al prompt, cuando no sepas o no encuentres la información solo di 'VACIO', no intentes crear una respuesta.{data}."
            query = f"Eres un asistente muy util. {data}"
            result = chain({"question": query, "chat_history": new_chat_history})
            answer = result['answer']

            #palabras_buscar = ["lo siento", "no sé", "no tengo", "vacio"]
            #if any(frase.lower() in answer.lower() for frase in palabras_buscar):
                #answer = self.prompt_bd(data)

            #new_chat_history.append((query, answer))
            return ControlResponse().success_data(
                {'message': {'answer': answer, 'chat_history': new_chat_history}})
        except Exception as e:
            logging.exception(e)
            return ControlResponse().internal_error()
    
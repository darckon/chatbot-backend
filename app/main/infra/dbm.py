# -*- coding: utf-8 -*
from flask import current_app as app
import psycopg2
import os



class PSQLConnection:

    def __init__(self):
        self.__handle = None

    def get_db_connection(self):
        conn = psycopg2.connect(
                host="localhost",
                database="develop",
                user='cristianrojas',
                password='794613..')
        
        return conn
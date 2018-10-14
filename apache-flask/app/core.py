import configparser
import os
import sys

from pymongo import MongoClient

from app.routes import api, ui
from app.modules import api_controller

class Core:

    def __init__(self, config_filename):
        self.config_filename = config_filename
        self.init_config()
        self.init_db()
        self.api_controller = api_controller.API_Controller()

    def init_config(self):
        config_filename = self.config_filename
        if not os.path.exists(config_filename):
            print(
                'Config file "{}/{}" does not exist.'.format(os.getcwd(), config_filename))
            sys.exit(1)
        config = configparser.ConfigParser()
        config.read(config_filename)
        self.config = config

    def init_db(self):
        try:
            config = self.config
            address = config.get('db', 'address')
            port = config.getint('db', 'port')
            db_name = config.get('db', 'db_name')
            client = MongoClient(address, port)
            db = client[db_name]
            self.client = client
            self.db = db
        except Exception as e:
            print('Error initializing database.')
            print(e)
            sys.exit(1)

    def setup(self):
        self.api_controller.setup()
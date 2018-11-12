import json

from Utils.LoggerUtil import LoggerUtil
from Utils.ConfigUtil import ConfigUtil
from Utils.DBUtils import DBUtils


class UserRegistration:
    def __init__(self):
        self.log = LoggerUtil(self.__class__.__name__).get()
        self.config = ConfigUtil.get_config_instance()
        self.db_utils = DBUtils()

    def get_client(self):
        address = self.config['mongo']['address']
        port = self.config['mongo']['port']
        auth_db = self.config['mongo']['auth_db']
        is_auth_enabled = self.config['mongo']['is_auth_enabled']
        username = self.config['mongo']['username']
        password = self.config['mongo']['password']

        client = self.db_utils.get_client(address=address, port=port,
                                          username=username, password=password,
                                          auth_db=auth_db, is_auth_enabled=is_auth_enabled)
        return client

    @staticmethod
    def insert_query(name, email, contact, password):
        query = dict()
        query['name'] = name
        query['email'] = email
        query['contact'] = contact
        query['password'] = password
        query['auth'] = True
        return query

    def add_user(self, **kwargs):
        name = kwargs['name']
        email = kwargs['email']
        contact = kwargs['contact']
        password = kwargs['password']

        client = self.get_client()

        users_database_name = self.config['mongo']['users_database']
        add_users_collection_name = self.config['mongo']['add_users_collection']
        database = client[users_database_name]
        add_users_collection = database[add_users_collection_name]

        query = self.insert_query(name, email, contact, password)
        try:
            add_users_collection.insert(query)
            self.log.info("Added user with username : {}".format(email))
        except Exception as e:
            self.log.error("Error : {}".format(e))

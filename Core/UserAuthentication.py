import json

from Utils.LoggerUtil import LoggerUtil
from Utils.DBUtils import DBUtils
from Utils.ConfigUtil import ConfigUtil


class UserAuthentication:
    def __init__(self):
        self.log = LoggerUtil(self.__class__.__name__).get()
        self.db_utils = DBUtils()
        self.config = ConfigUtil.get_config_instance()

    def get_client(self):
        address = self.config['mongo']['address']
        port = self.config['mongo']['port']
        auth_db = self.config['mongo']['auth_db']
        is_auth_enabled = self.config['mongo']['is_auth_enabled']
        username = self.config['username']
        password = self.config['password']

        client = self.db_utils.get_client(address=address, port=port,
                                          username=username, password=password,
                                          auth_db=auth_db, is_auth_enabled=is_auth_enabled)
        return client

    @staticmethod
    def user_auth_query(username, password):
        query = dict()
        query['username'] = username
        query['password'] = password
        return json.dumps(query)

    def check_in_db(self, username, password):
        users_database = self.config['mongo']['users_database']
        login_collection = self.config['mongo']['login_collection']
        client = self.get_client()
        database = client[users_database]
        login_collection = database[login_collection]

        query = self.user_auth_query(username=username, password=password)
        cursor = login_collection.find(query)
        for doc in cursor:
            if 'auth' in doc:
                return True
            else:
                return False

    @staticmethod
    def username_avail_query(username):
        query = dict()
        query['username'] = username
        return json.dumps(query)

    def is_username_available(self, username):
        users_database = self.config['mongo']['users_database']
        client = self.get_client()
        database = client[users_database]
        login_collection = database['login_collection']

        query = self.username_avail_query(username=username)
        cursor = login_collection.find(query)
        for doc in cursor:
            if 'auth' in doc:
                return False
            else:
                return True

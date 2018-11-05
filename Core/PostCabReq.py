from Utils.LoggerUtil import LoggerUtil
from Utils.DBUtils import DBUtils
from Utils.ConfigUtil import ConfigUtil


class PostCabReq:
    def __init__(self):
        self.log = LoggerUtil(self.__class__.__name__).get()
        self.config = ConfigUtil.get_config_instance()
        self.db_utils = DBUtils()

    def post_request(self):
        """
        Check if there is a cab available b/w source and destination
        If there is one, check if there are required number of seats available.
        If yes, then return the cab list.
        :return:
        """
        pass

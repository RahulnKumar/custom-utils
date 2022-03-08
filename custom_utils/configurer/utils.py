"""Module containing log formatter and crendials setup tools"""

import os
import json
import logging
import traceback
from datetime import datetime

logging.basicConfig(format='%(asctime)s  %(levelname)s--> %(message)s',
                    datefmt='%d/%b/%Y %H:%M:%S %p %Z', level=logging.INFO)
logger = logging.getLogger('custom_logger')


class LogFormatter(logging.Formatter):
    """Log Formatter class """

    __date_format = '%d/%b/%Y:%H:%M:%S %Z'

    @staticmethod
    def apply(level=logging.INFO):
        """
        Start logging in json format.
        :return:
        """
        json_log_format = {
            'ts': '%(asctime)s',
            'level': '%(levelname)s',
            'location': '%(pathname)s:%(lineno)d',
            'msg': '%(message)s'
        }
        log_format = json.dumps(json_log_format)
        logging.basicConfig(format=log_format, level=level, datefmt=LogFormatter.__date_format)
        if len(logging.root.handlers) > 0:
            logging.root.handlers[0].setFormatter(LogFormatter(fmt=log_format,
                                                  datefmt=LogFormatter.__date_format))

    def formatException(self, execution_info):
        """
        Handle logging in case of exceptions.
        :param execution_info:
        :return:
        """
        stacktrace = super(LogFormatter, self).formatException(execution_info)
        record = {
            'message': stacktrace,
            'levelname': 'EXCEPTION',
            'pathname': 'stacktrace in msg',
            'lineno': -1
        }
        try:
            record['asctime'] = datetime.now().strftime(LogFormatter.__date_format)
            return self._fmt % record
        except Exception as err:
            return repr(stacktrace)


class Credential:
    """ sets aws access key and secret key as environment variables """

    @staticmethod
    def set(access_key, secret_key):

        """
        sets aws access key and secret key as environment variables
        :param string ACCESS_KEY:  this is aws_access_key_id
        :param string SECRET_KEY: this is aws_secret_access_key
        :return None
        """

        try:
            os.environ["ACCESS_KEY"] = access_key
            os.environ["SECRET_KEY"] = secret_key
            logger.info("----- Environment Variables set successfully -----")
        except:
            logger.error(" Something went wrong while setting environment variables")
            traceback.print_exc()

"""Module containing custom exception classes"""

class BigQueryConnectionError(Exception):
    """Raised when data from bigQuery connection is failed"""

class BigQueryDataFetchError(Exception):
    """Raised when fetching data from bigQuery is failed"""

class BigQueryGenericError(Exception):
    """Raised when there BigQuery API is falied"""

class MysqlConnectionError(Exception):
    """Raised when data from MySQL connection is failed"""

class MysqlDataFetchError(Exception):
    """Raised when fetching data from MySQL is failed"""

class MysqlGenericError(Exception):
    """Raised when there MySQL API is falied"""

class MongodbConnectionError(Exception):
    """Raised when data from MongoDB connection is failed"""

class MongodbDataFetchError(Exception):
    """Raised when fetching data from MongoDB is failed"""

class MongodbGenericError(Exception):
    """Raised when there MongoDB API is falied"""

class SlackError(Exception):
    """Raised when there SLACK_BOT_TOKEN is not passed or invalid"""
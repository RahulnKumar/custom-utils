"""MySQL database utility functions"""

import logging
import sqlalchemy
import pandas as pd
from utilities.exceptions import MysqlConnectionError, MysqlDataFetchError, MysqlGenericError


class MySQL:
    """MySQL database utility functions"""

    def __init__(self, db_string):
        """
        initialisation method for MySQL Connector
        :param string db_string: mysql database connection string
        """

        try:
            self.connection = sqlalchemy.create_engine(db_string)
        except Exception as err:
            raise MysqlConnectionError(err) from err


    def get_data(self, query):

        """
        Fetch data from mysql as a dataframe.
        :param string query: query for fetching data from table
        :return pd.DataFrame data
        """


        try:
            data = pd.read_sql(query + " ;", self.connection)
            logging.debug("data fetched successfully")
            return data
        except Exception as err:
            raise MysqlDataFetchError(err) from err
        finally:
            self.connection.dispose()


    def execute_query(self, query):

        """
        Execute a query in the mysql table
        :param string query: query for execution in the table
        :return :
        """

        try:
            self.connection.execute(query)
            logging.debug("query executed successfully")
        except Exception as err:
            raise MysqlGenericError(err) from err
        finally:
            self.connection.dispose()

    def dump_data(self, data, table_name, mode="append"):

        """
        Execute a query in the mysql table
        :param pd.DataFrame data: dataframe to be appended or replaced
        :param string table_name: name of the the target table
        :param string mode: it can be either replace or append
        :return None
        """


        try:
            connection = self.connection
            data.to_sql(name=table_name, con=connection, if_exists=mode, index=False)
            logging.debug("data dumped successfully")
        except Exception as err:
            raise MysqlGenericError(err) from err
        finally:
            connection.dispose()

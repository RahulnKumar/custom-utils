"""Module containing bigQuery warehouse utility functions"""

import time
import logging
import requests

import pandas_gbq as gbq
from google.cloud import bigquery
from google.oauth2.service_account import Credentials
from utilities.exceptions import (
     BigQueryConnectionError,
     BigQueryDataFetchError,
     BigQueryGenericError
     )

class BigQuery:
    """BigQuery database utility functions"""

    def __init__(self, read_big_query_project ,
                       write_big_query_project ,
                       service_account_file_path):

        """
        initialisation method for BigQuery Connector
        :param str read_big_query_project : project used while reading from BigQuery
        :param str write_big_query_project: project used while writing into BigQuery
        :param str service_account_file_path: project specific BigQuery Credential
        """

        self.read_big_query_project = read_big_query_project
        self.write_big_query_project = write_big_query_project

        try:
            self.credentials = Credentials.from_service_account_file(service_account_file_path)
            self.bq_client = bigquery.Client(credentials=self.credentials,
                                             project=self.credentials.project_id)
        except Exception as err:
            raise BigQueryConnectionError(err) from err


    def get_data(self, query=None, query_config=None, max_retries=0, time_interval=5):

        """
        Fetches data from from BigQuery
        :param string query: query for fetching data from table
        :param string query_cofig: config for parameterised query
        :param string max_retries: maximum retries if data is not fetched
        :param integer time_interval : time interval between retries
        """

        flag = True
        while flag is True:
            try:
                df = gbq.read_gbq(query=query, project_id=self.read_big_query_project,
                                configuration=query_config, credentials=self.credentials)
                logging.debug("Data fetched successfully")
                return df
            except requests.exceptions.Timeout:
                logging.info("readtimeot - - - waiting for {} seconds".format(time_interval))
                max_retries = max_retries - 1
                flag = False if max_retries <= 0 else True
                time.sleep(time_interval)
            except Exception as err:
                flag = False
                raise BigQueryDataFetchError(err) from err

    def execute_query(self, query, query_config=None, max_retries=0, time_interval=5):

        """
        Executes query from from BigQuery table
        :param string query: query for execution
        :param string query_cofig: config for parameterised query
        :param string max_retries: maximum retries if data is not fetched
        :param integer time_interval : time interval between retries
        """


        flag = True
        while flag is True:
            try:
                query_job = self.bq_client.query(query, job_config=query_config)  # API request
                query_job.result(timeout=900)  # Waits for statement to finish
                logging.debug("------- Query Executed successfully ----- ")
                flag = False
            except requests.exceptions.Timeout:
                logging.info(f"readtimeot - - - - - - waiting for {time_interval} seconds")
                max_retries = max_retries - 1
                flag = False if max_retries <= 0 else True
                time.sleep(time_interval)
            except Exception as err:
                flag = False
                raise BigQueryGenericError(err) from err


    def dump_data(self, database=None, table=None, dataframe=None, mode="append"):

        """
        Dumps data into from BigQuery
        :param string database: target bigquery database
        :param string table: target table name
        :param pd.DataFrame dataframe: pandas dataframe for dumping into bigquery
        :param string mode: it can be either append or replace
        """

        try:
            gbq.to_gbq(dataframe,
                       f'{database}.{table}',
                       self.write_big_query_project,
                       credentials=self.credentials, if_exists=mode)
            print("Appending Done")
        except Exception as err:
            raise BigQueryGenericError(err) from err




    def insert_rows_array(self, dataset=None, table=None, rows_to_insert=None):

        """
        Streaming insert into from BigQuery
        :param string dataset: target bigquery database
        :param string table: target table name
        :param list rows_to_insert: list of dictionaries where each dictionary is a
                                    row with keys as column names
        """

        try:
            table = f'{self.write_big_query_project}.{dataset}.{table}'
            errors = self.bq_client.insert_rows_json(table, rows_to_insert)
            assert errors == []
        except Exception as err:
            raise BigQueryGenericError(err) from err


    def insert_rows_in_bigquery(self, dataset=None, table=None, rows_to_insert=None):

        """
        Streaming insert into from BigQuery
        :param string dataset: target bigquery database
        :param string table: target table name
        :param  rows_to_insert: list of dictionaries where each dictionary is a
                                row with keys as column names
        """

        try:
            table_id = f'{self.write_big_query_project}.{dataset}.{table}'
            table = self.bq_client.get_table(table_id)
            errors = self.bq_client.insert_rows(table, rows_to_insert)
            if not errors:
                print("Rows added successfully")
            else:
                print("Failed adding rows", '\n', errors)
        except Exception as err:
            raise BigQueryGenericError(err) from err

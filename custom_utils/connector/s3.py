"""Module containing AWS S3 utility functions"""

import os
import tempfile
import subprocess
from io import BytesIO
import joblib
import boto3
import pandas as pd
from smart_open import smart_open
from custom_utils.configurer.utils import logger

class S3:
    """AWS S3 utility functions"""

    @staticmethod
    def pull_python_object(s3_uri):
        """
        read python object stored in S3 bucket
        :param string s3_uri: s3 uri of the object
        :return python_object : python object stored in the S3
        """

        bucket, key = s3_uri[5:].split('/', 1)
        print(bucket, key)
        try:
            s3 = boto3.resource('s3', aws_access_key_id=os.environ['ACCESS_KEY'],
                                      aws_secret_access_key=os.environ['SECRET_KEY'])
            logger.debug("Connected to S3 via environment credentials")
        except:
            s3 = boto3.resource('s3')
            logger.debug("Connected to S3 via IAM role")
        logger.debug(f"Reading data from S3 path: {bucket}/{key}")
        with BytesIO() as data:
            s3.Bucket(bucket).download_fileobj(key, data)
            data.seek(0)
            python_object = joblib.load(data)
        return python_object

    @staticmethod
    def push_python_object(python_object, s3_uri):
        """
        write python objects/variables etc  into S3 bucket
        :param string bucket: bucket name
        :param string sub_bucket: sub-bucket name
        :param string file_name: name of the file to be written
        :return None
        """

        bucket, key = s3_uri[5:].split('/', 1)
        compress = ('gzip', 3)
        try:
            s3 = boto3.resource('s3', aws_access_key_id=os.environ['ACCESS_KEY'],
                                      aws_secret_access_key=os.environ['SECRET_KEY'])
            logger.debug("Connected to S3 via environment credentials")
        except:
            s3 = boto3.resource('s3')
            logger.debug("Connected to S3 via IAM role")

        logger.info(f"Writing data to S3 path : {bucket}/{key}")
        with tempfile.TemporaryFile() as data:
                    joblib.dump(python_object, data, compress=compress)
                    data.seek(0)
                    s3.Bucket(bucket).upload_fileobj(data, key)

    @staticmethod
    def push_local_data(file_path, s3_uri):

        """
        write data stored in local machine into S3 bucket from
        :param string s3_uri: target s3 uri
        :param string file_path:  local path of the file 
        :return None
        """

        try:
            logger.debug("Pushing data in S3 at {s3_uri}")
            upload_command = f"aws s3 cp  {file_path} {s3_uri}"
            upload_command_array = upload_command.split()
            p = subprocess.Popen(upload_command_array,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
        except Exception as err:
            logger.error(err)

    @staticmethod
    def pull_s3_data(file_path, s3_uri):

        """
        write data stored in local machine into S3 bucket from
        :param string s3_uri: target s3 uri
        :param string file_path:  local path of the file 
        :return None
        """

        try:
            logger.debug("Pushing data in S3 at {s3_uri}")
            download_command = f"aws s3 cp {s3_uri} {file_path}"
            download_command_array = download_command.split()
            p = subprocess.Popen(download_command_array,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
        except Exception as err:
            logger.error(err)

    @staticmethod
    def read_csv(s3_uri):
         """
        write data stored in local machine into S3 bucket from
        :param string s3_uri: csv file S3 URI
        :return df : pandas dataframe
        """
         try:
              df = pd.read_csv(smart_open(s3_uri))
              return df
         except Exception as err:
              logger.error(err)

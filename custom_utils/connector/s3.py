"""Module containing AWS S3 utility functions"""

import os
import tempfile
import subprocess
from io import BytesIO
import joblib
import boto3
from custom_utils.configurer.utils import logger

class S3:
    """AWS S3 utility functions"""

    @staticmethod
    def pull_data(bucket, sub_bucket, file_name):
        """
        read data stored in S3 bucket
        :param string bucket: bucket name
        :param string sub_bucket: sub-bucket name
        :param string file_name: name of the file to be read
        :return old_data : python object stored in the S3
        """

        key = f"{sub_bucket}/{file_name}"
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
            old_data = joblib.load(data)
        return old_data


    @staticmethod
    def push_data(python_data_object, bucket, sub_bucket, file_name):
        """
        write python objects/variables etc  into S3 bucket
        :param string bucket: bucket name
        :param string sub_bucket: sub-bucket name
        :param string file_name: name of the file to be written
        :return None
        """

        key = f'{sub_bucket}{file_name}'
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
                    joblib.dump(python_data_object, data, compress=compress)
                    data.seek(0)
                    s3.Bucket(bucket).upload_fileobj(data, key)


    @staticmethod
    def push_local_data(file_path, bucket, sub_bucket):

        """
        write data stored in local machine into S3 bucket from
        :param string bucket: bucket name
        :param string sub_bucket: sub-bucket name
        :param string file_path: path of the file to be written
        :return None
        """

        try:
            destination_s3_path =  f"s3://{bucket}/{sub_bucket}"
            logger.debug("Pushing data in S3 at {destination_s3_path}")
            upload_command = f"aws s3 cp  {file_path} {destination_s3_path}"
            upload_command_array = upload_command.split()
            p = subprocess.Popen(upload_command_array,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            while True:
                retcode = p.poll()
                line = p.stdout.readline()
                if retcode is not None:
                    os.remove(file_path)
                    logger.debug(f"Removing file name: {file_path}")
                    break
        except Exception as err:
            logger.error(err)

"""Module containing AWS S3 utility functions"""

import os
import logging
import tempfile
import subprocess
from io import BytesIO
import joblib
import boto3



class S3:
    """AWS S3 utility functions"""

    @staticmethod
    def read_from_s3_bucket(bucket, sub_bucket, file_name):
        """
        read data stored in S3 bucket
        :param string bucket: bucket name
        :param string sub_bucket: sub-bucket name
        :param string file_name: name of the file to be read
        :return old_data : python object stored in the S3
        """

        key = sub_bucket + file_name
        s3 = boto3.resource('s3')
        logging.info(f"Reading data from : {bucket}/{key}")
        with BytesIO() as data:
            s3.Bucket(bucket).download_fileobj(key, data)
            data.seek(0)
            old_data = joblib.load(data)
        return old_data

    @staticmethod
    def write_to_s3_bucket(python_data_object, bucket, sub_bucket, file_name):
        """
        write python objects/variables etc  into S3 bucket
        :param string bucket: bucket name
        :param string sub_bucket: sub-bucket name
        :param string file_name: name of the file to be written
        :return None
        """

        key = f'{sub_bucket}{file_name}'
        compress = ('gzip', 3)
        logging.info(f"Writing data to : {bucket}/{key}")
        s3 = boto3.resource('s3')
        with tempfile.TemporaryFile() as data:
            joblib.dump(python_data_object, data, compress=compress)
            data.seek(0)
            s3.Bucket(bucket).upload_fileobj(data, key)

    @staticmethod
    def upload_data_from_local_to_s3(model_file_name, bucket, sub_bucket):

        """
        write data stored in local machine into S3 bucket from
        :param string bucket: bucket name
        :param string sub_bucket: sub-bucket name
        :param string file_name: name of the file to be written
        :return None
        """

        try:
            final_bucket_folder_path =  "s3://"+bucket+"/"+sub_bucket
            final_bucket_folder_path = "s3://data-science-datas/models/"
            print(final_bucket_folder_path)
            upload_command = "aws s3 cp  " + model_file_name+" "+ final_bucket_folder_path
            print(upload_command)
            upload_command_array = upload_command.split()
            p = subprocess.Popen(upload_command_array,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            while True:
                retcode = p.poll()
                line = p.stdout.readline()
                print(line)
                print(retcode)
                if retcode is not None:
                    os.remove(model_file_name)
                    print("Removing file name: ", model_file_name)
                    break
        except Exception as err:
            print(err)

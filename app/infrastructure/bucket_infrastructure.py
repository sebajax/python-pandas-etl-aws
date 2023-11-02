# module import
import io
import logging
from dataclasses import dataclass

import boto3

# config import
from infrastructure.config import get_settings

# get root logger
logger = logging.getLogger(__name__)


@dataclass
class BucketInfrastructure:
    """
    class to represent all the s3 bucket interactions
    """
    file: str

    @classmethod
    def __connect_to_s3(cls):
        # get env variables to connect into the bucket
        aws_id = get_settings().AWS_ACCESS_KEY
        aws_secret = get_settings().AWS_SECRET_KEY
        # connect to aws
        return boto3.client('s3', aws_access_key_id=aws_id, aws_secret_access_key=aws_secret)

    def get_file_from_bucket(self) -> io.BytesIO | None:
        # get env variables to connect into the bucket
        bucket_name = get_settings().AWS_BUCKET_NAME
        object_key = self.file

        # connect to aws
        s3 = self.__connect_to_s3()
        try:
            # get the file from the bucket
            obj = s3.get_object(Bucket=bucket_name, Key=object_key)
            data = obj['Body'].read()
            logger.info("file loaded successfully from bucket %s", object_key)
            # return the file into an array of bytes to transform the data into a dataframe
            return io.BytesIO(data)
        except Exception as e:
            print(e)
            return None

    def write_file_into_bucket(self, xlsx_data: bytes):
        # get env variables to connect into the bucket
        bucket_name = get_settings().AWS_BUCKET_NAME
        object_key = f"{self.file}_Error.xlsx"

        # connect to aws
        s3 = self.__connect_to_s3()
        try:
            # write the bytes into a file to the bucket
            s3.put_object(Bucket=bucket_name, Key=object_key, Body=xlsx_data)
            logger.info("error file written successfully into bucket %s", object_key)
        except Exception as e:
            logger.error("process error %s", e)
            return None

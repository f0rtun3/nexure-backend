"""
AWS Pre signed URL class handler
"""
from flask import current_app as app
from helpers import aws_configs as aws_config
import logging
from botocore.exceptions import ClientError

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """ 
    Generate a presigned url for getting an object
    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = aws_config.get_s3()
    try:
        url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_name},
                ExpiresIn=expiration
        )
    except ClientError as e:
        logging.error(e)
        return None

    return url


def generate_presigned_post(bucket_name, object_name, expiration=3600):
    """ 
    Generate a presigned url to upload a new object
    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    s3 = aws_config.get_s3()
    try:
        url = s3.generate_presigned_post(
            Bucket=app.config['S3_BUCKET'],
            Key=object_name,
            ExpiresIn=expiration
        )
    except ClientError as error_msg:
        logging.error(error_msg)
        return None

    return url
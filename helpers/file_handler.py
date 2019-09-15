"""
AWS Pre signed URL class handler
"""
import logging
from botocore.exceptions import ClientError
from app import application


class S3FileHandler:
    """
    s3 File handler class
    describes the general way to generate pre-signed
    urls for the request needed
    :type method_name string   the s3 client method
    :type method_parameters Object   the specific method parameters
    :type expiration number   the expiration time of the pre-signed url
    :type http_method string   the http method to use for the request
    """

    def __init__(self, method_name, method_parameters=None, expiration=3600,
                 http_method=None):
        self.method_name = method_name
        self.method_parameters = method_parameters
        self.expiration = expiration
        self.http_method = http_method
        self.key = ""
        self.fields = {}
        self.conditions = []

    def set_upload_key(self, key_name):
        """
        set the name of the file to upload to s3
        :type key_name {string}
        """
        self.key = key_name

    def set_upload_fields(self, fields):
        """
        set the fields to be used by client during the uplod
        :type fields Object
        """
        self.fields = fields

    def set_uplods_conditions(self, conditions):
        """
        set the conditions to include in the policy when uploading an object
        :type conditions: object
        """
        self.conditions = conditions

    def create_presigned_url(self):
        """
        actual method to generate the pre-signed url
        :return String
        """
        try:
            response = application.s3.generate_presigned_url(
                ClientMethod=self.method_name,
                Params=self.method_parameters,
                ExpiresIn=self.expiration,
                HttpMethod=self.http_method
            )

        except ClientError as error_msg:
            logging.error(error_msg)
            return None

        return response

    def create_presigned_post(self):
        """
        generate a presigned url to upload a file to s3 bucket
        :return object returns url and fields to pass during upload
        """
        try:
            response = application.s3.generate_presigned_post(
                Bucket=application.app.config['S3_BUCKET'],
                Key=self.key,
                Fields=self.fields,
                Conditions=self.conditions,
                ExpiresIn=self.expiration
            )
        except ClientError as error_msg:
            logging.error(error_msg)
            return None

        return response

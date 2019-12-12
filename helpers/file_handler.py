"""
AWS Pre signed URL class handler
"""
from flask import current_app as app
from helpers import aws_configs as aws_config
import logging
from botocore.exceptions import ClientError


class S3FileHandler():
    def __init__(self, bucket_name, object_name, expiration = 3600):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.expiration = expiration
        self.fields = {}
        self.conditions = []
        self.s3_client = aws_config.get_s3()
    
    def set_field_names(self, field_names):
        self.fields = field_names
    
    def set_conditions(self, conditions):
        self.conditions = conditions
    
    def generate_pre_signed_url(self, client_method="get_object"):
        """
        generate a presigned url to fetch an object from s3 client
        """
        try:
            url = self.s3_client.generate_presigned_url(
                client_method,
                Params={
                    'Bucket': self.bucket_name,
                    'Key': self.object_name},
                ExpiresIn=self.expiration
            )
        except ClientError as e:
            logging.error(e)
            return None
        
        return url
    
    def generate_presigned_post(self):
        """
        generate a presigned post url to upload 
        an object to s3 bucket
        """
        try:
            url = self.s3_client.generate_presigned_post(
                Bucket=app.config['S3_BUCKET'],
                Key=self.object_name,
                Fields=self.fields,
                Conditions=self.conditions,
                ExpiresIn=self.expiration
            )
        except ClientError as e:
            logging.error(e)
            return None

        return url

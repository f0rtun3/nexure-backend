from flask import current_app as app
from flask import make_response
from flask_jwt_extended import jwt_required
from helpers.file_handler import S3FileHandler
from helpers import helpers as helper
from flask_restful import Resource


class AWSPresignedURL(Resource):
    @jwt_required
    def get(self, object_name):
        """
        get the presigned url to fetch file from s3 resource
        :param object_name {String} the name of object to be uploaded
        """
        bucket_name =  app.config['S3_BUCKET']
        s3_handler = S3FileHandler(bucket_name, object_name)
        response = s3_handler.generate_pre_signed_url()
        if response:
            return make_response(helper.make_rest_success_response("Success", response), 200)
        
        return make_response(helper.make_rest_fail_response("Failed"), 500)


class AWSPresignedExtended(Resource):    
    @jwt_required
    def get(self, object_name):
        bucket_name = app.config['S3_BUCKET']
        s3_handler = S3FileHandler(bucket_name, object_name)
        response = s3_handler.generate_presigned_post()
        if response:
            return make_response(helper.make_rest_success_response("Success", response), 200)
        
        return make_response(helper.make_rest_fail_response("Failed"), 500)

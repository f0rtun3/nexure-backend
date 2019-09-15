from flask import Flask, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
import boto3

# automatically set the application's os environment
# variables from the .env file
# to avoid manual and repetitive setting of the same
load_dotenv()


application = Flask(__name__)
# mail=Mail(application)
application.config.from_object(os.environ['APP_SETTINGS'])
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(application, resources={r"/*": {"origins": application.config['ALLOWED_HOSTS']}})
db = SQLAlchemy(application)
migrate = Migrate(application, db)
jwt = JWTManager(application)
ses = boto3.client(
    "ses",
    region_name=application.config['AWS_REGION'],
    aws_access_key_id=application.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=application.config['AWS_SECRET_ACCESS_KEY']
)
s3 = boto3.client(
    's3',
    aws_access_key_id=application.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=application.config['AWS_SECRET_ACCESS_KEY']
)

@jwt.expired_token_loader
def expired_token_handler():
    """token sent has expired"""
    response = {
        'status_message': 'failed',
        'message': 'Your token has expired'
    }
    return make_response(jsonify(response), 401)


@jwt.invalid_token_loader
def invalid_token_handler():
    """token sent deos not match generated token"""
    response = {
        'status_message': 'failed',
        'message': 'Token is invalid'
    }
    return make_response(jsonify(response), 401)


@jwt.unauthorized_loader
def unauthorized_token_handler():
    """unprivileged user"""
    response = {
        'status_message': 'failed',
        'message': 'Unauthorized token'
    }
    return make_response(jsonify(response), 401)


@jwt.needs_fresh_token_loader
def fresh_token_loader_handler():
    """token sent is not fresh"""
    response = {
        'status_message': 'failed',
        'message': 'Needs a fresh token'
    }
    return make_response(jsonify(response), 401)

import api

if __name__ == '__main__':
    application.run(host=application.config['HOST'], port=application.config['PORT'])

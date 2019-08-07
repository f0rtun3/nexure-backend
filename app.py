from flask import Flask, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

import os
import boto3

# automatically set the application's os environment
# variables from the .env file
# to avoid manual and repetitive setting of the same
load_dotenv()


app = Flask(__name__)
mail=Mail(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, resources={r"/*": {"origins": app.config['ALLOWED_HOSTS']}})
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
"""
ses = boto3.client(
    "ses",
    region_name=app.config['AWS_REGION'],
    aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
)
"""

@jwt.expired_token_loader
def expired_token_handler():
    """token sent has expired"""
    response = {
        'status': 'failed',
        'message': 'Your token has expired'
    }
    return make_response(jsonify(response), 401)


@jwt.invalid_token_loader
def invalid_token_handler():
    """token sent deos not match generated token"""
    response = {
        'status': 'failed',
        'message': 'Token is invalid'
    }
    return make_response(jsonify(response), 401)


@jwt.unauthorized_loader
def unauthorized_token_handler():
    """unprivileged user"""
    response = {
        'status': 'failed',
        'message': 'Unauthorized token'
    }
    return make_response(jsonify(response), 401)


@jwt.needs_fresh_token_loader
def fresh_token_loader_handler():
    """token sent is not fresh"""
    response = {
        'status': 'failed',
        'message': 'Needs a fresh token'
    }
    return make_response(jsonify(response), 401)

import api

if __name__ == '__main__':
    app.run()

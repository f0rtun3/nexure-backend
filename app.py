from flask import Flask, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate

import os

# automatically set the application's os environment
# variables from the .env file
# to avoid manual and repetitive setting of the same
load_dotenv()


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, resources={r"/*": {"origins": app.config['ALLOWED_HOSTS']}})
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)
mail = Mail(app)

def create_app():
    from . import models, r

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


from resources.resources import UserRegister
from resources.resources import UserLogin
from resources.resources import UserAccountConfirmation
from resources.resources import CustomerOnBoarding
from resources.resources import OrganizationType
from resources.resources import OrganizationCustomerResource


api.add_resource(UserRegister, '/user')
api.add_resource(UserLogin, '/login')
api.add_resource(CustomerOnBoarding, '/register_customer')
api.add_resource(UserAccountConfirmation, '/confirm')
api.add_resource(OrganizationType, '/get_organization_types')
api.add_resource(OrganizationCustomerResource, '/organization')


if __name__ == '__main__':
    app.run(port=app.config['PORT'], debug=app.config['DEBUG'])

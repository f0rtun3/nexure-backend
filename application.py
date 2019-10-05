from flask import Flask, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_restful import Api
from database.db import db

import os

from models import *
from resources.Users import UserRegister
from resources.Users import UserLogin
from resources.Users import TokenRefresh
from resources.Users import AccountConfirmation
from resources.Users import AccountRecovery
from resources.Users import AccountConfirmationResource
from resources.Customers import CustomerOnBoarding
from resources.Customers import AgencyCustomers
from resources.Customers import CustomerPolicyHandler
from resources.StaffRegistration import StaffRegistration
from resources.Organizations import OrganizationHandler
from resources.Cars import CarHandler
from resources.Extensions import ExtensionHandler
from resources.Loadings import LoadingsHandler
from resources.Benefits import BenefitHandler
from resources.InsuranceCompany import Companies
from resources.CompanyDetails import CompanyDetails
from resources.CompanyDetails import CompanyDetailsHandler
from resources.MPIUnderwriting import MPIUnderwriting
from resources.Location import Location
from resources.CustomerDetails import CustomerDetails
from resources.MasterDetails import MasterDetails
from resources.ChildDetails import ChildDetails

"""
automatically set the application's os environment
variables from the .env file
to avoid manual and repetitive setting of the same
"""
load_dotenv()

application = Flask(__name__)
application.config.from_object(os.environ['APP_SETTINGS'])
db.init_app(application)
CORS(application, resources={
    r"/*": {"origins": application.config['ALLOWED_HOSTS']}})
migrate = Migrate(application, db)
jwt = JWTManager(application)


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
    """token sent does not match generated token"""
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


API = Api(application)

API.add_resource(Companies, '/api/companies/<int:status>')
API.add_resource(CustomerDetails, '/api/customer_details/<string:email>')
API.add_resource(AgencyCustomers, '/api/customer_details')
API.add_resource(CustomerPolicyHandler, '/api/customer_details/<path:customer_number>')
API.add_resource(CompanyDetails, '/api/company_details')
API.add_resource(CompanyDetailsHandler, '/api/company_details/<int:company_id>')
API.add_resource(UserRegister, '/api/user')
API.add_resource(MasterDetails, '/api/master_details/<int:master_id>')
API.add_resource(ChildDetails, '/api/child_details/<int:child_id>')
API.add_resource(UserLogin, '/api/login')
API.add_resource(TokenRefresh, '/api/auth/refresh')
API.add_resource(CustomerOnBoarding, '/api/customer')
API.add_resource(AccountConfirmation, '/api/confirm')
API.add_resource(AccountConfirmationResource, '/api/confirm/<int:user_id>')
API.add_resource(AccountRecovery, '/api/auth/reset')
API.add_resource(StaffRegistration, '/api/staff')
API.add_resource(CarHandler, '/api/vehicles')
API.add_resource(OrganizationHandler, '/api/organizations/all')
API.add_resource(MPIUnderwriting, '/api/transactions')
API.add_resource(BenefitHandler, '/api/benefits')
API.add_resource(LoadingsHandler, '/api/loadings')
API.add_resource(ExtensionHandler, '/api/extensions')
API.add_resource(Location, '/api/locations')

if __name__ == '__main__':
    application.run(
        host=application.config['HOST'], port=application.config['PORT'])

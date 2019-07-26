from flask_restful import Api
from app import app

api = Api(app)

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
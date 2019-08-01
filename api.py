from app import app
from flask_restful import Api
api = Api(app)

from resources.Users import UserRegister
from resources.Users import UserLogin
from resources.Users import AccountConfirmation
from resources.Customers import CustomerOnBoarding
from resources.StaffRegistration import StaffRegistration


api.add_resource(UserRegister, '/api/user')
api.add_resource(UserLogin, '/api/login')
api.add_resource(CustomerOnBoarding, '/api/customer')
api.add_resource(AccountConfirmation, '/api/confirm')
api.add_resource(StaffRegistration, '/api/staff')

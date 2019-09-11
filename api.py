"""
api endpoint definition
"""
from flask_restful import Api

from resources.Users import UserRegister
from resources.Users import UserLogin
from resources.Users import TokenRefresh
from resources.Users import AccountConfirmation
from resources.Users import AccountRecovery
from resources.Users import AccountConfirmationResource
from resources.Customers import CustomerOnBoarding
from resources.StaffRegistration import StaffRegistration
from resources.Organizations import OrganizationHandler
from resources.Cars import CarHandler
from resources.Extensions import ExtensionHandler
from resources.Loadings import LoadingsHandler
from resources.Benefits import BenefitHandler
from resources.InsuranceCompany import Companies
from resources.CompanyDetails import CompanyDetails
from resources.MPIUnderwriting import MPIUnderwriting
from resources.Location import Location
from resources.InsuranceProducts import InsuranceProducts
from resources.CustomerDetails import CustomerDetails
from resources.MasterDetails import MasterDetails
from resources.ChildDetails import ChildDetails
from resources.policy_handler import PolicyHandler
from resources.policy_handler import BenefitsHandler

from app import app

API = Api(app)

API.add_resource(Companies, '/api/companies/all')
API.add_resource(CustomerDetails, '/api/customer_details/<email>')
API.add_resource(CompanyDetails, '/api/company_details/<company_id>')
API.add_resource(UserRegister, '/api/user')
API.add_resource(MasterDetails, '/api/master_details/<master_id>')
API.add_resource(ChildDetails, '/api/child_details/<child_id>')
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
API.add_resource(InsuranceProducts, '/api/products')

#   test api endpoints
API.add_resource(PolicyHandler, '/api/policy_handler/<int:policy_id>')
API.add_resource(BenefitsHandler, '/api/benefits/<int:policy_id>')

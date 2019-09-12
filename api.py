from resources.ChildDetails import ChildDetails
from resources.MasterDetails import MasterDetails
from resources.CustomerDetails import CustomerDetails
from resources.Location import Location
from resources.MPIUnderwriting import MPIUnderwriting
from resources.CompanyDetails import CompanyDetails, CompanyDetailsHandler
from resources.InsuranceCompany import Companies
from resources.Benefits import BenefitHandler
from resources.Loadings import LoadingsHandler
from resources.Extensions import ExtensionHandler
from resources.Cars import CarHandler
from resources.Organizations import OrganizationHandler
from resources.StaffRegistration import StaffRegistration
from resources.Customers import CustomerOnBoarding
from resources.Users import AccountConfirmationResource
from resources.Users import AccountRecovery
from resources.Users import AccountConfirmation
from resources.Users import TokenRefresh
from resources.Users import UserLogin
from resources.Users import UserRegister
from app import app
from flask_restful import Api
api = Api(app)


api.add_resource(Companies, '/api/companies/all')
api.add_resource(CustomerDetails, '/api/customer_details/<email>')
api.add_resource(CompanyDetails, '/api/company_details')
api.add_resource(CompanyDetailsHandler, '/api/company_details/<int:company_id>')
api.add_resource(UserRegister, '/api/user')
api.add_resource(MasterDetails, '/api/master_details/<master_id>')
api.add_resource(ChildDetails, '/api/child_details/<child_id>')
api.add_resource(UserLogin, '/api/login')
api.add_resource(TokenRefresh, '/api/auth/refresh')
api.add_resource(CustomerOnBoarding, '/api/customer')
api.add_resource(AccountConfirmation, '/api/confirm')
api.add_resource(AccountConfirmationResource, '/api/confirm/<int:user_id>')
api.add_resource(AccountRecovery, '/api/auth/reset')
api.add_resource(StaffRegistration, '/api/staff')
api.add_resource(CarHandler, '/api/vehicles')
api.add_resource(OrganizationHandler, '/api/organizations/all')
api.add_resource(MPIUnderwriting, '/api/transactions')
api.add_resource(BenefitHandler, '/api/benefits')
api.add_resource(LoadingsHandler, '/api/loadings')
api.add_resource(ExtensionHandler, '/api/extensions')
api.add_resource(Location, '/api/locations')

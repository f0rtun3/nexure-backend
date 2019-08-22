from app import app
from flask_restful import Api
api = Api(app)

from resources.Users import UserRegister
from resources.Users import UserLogin
from resources.Users import AccountConfirmation
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


api.add_resource(Companies, '/api/companies/all')
api.add_resource(CompanyDetails, '/api/company_details')
api.add_resource(UserRegister, '/api/user')
api.add_resource(UserLogin, '/api/login')
api.add_resource(CustomerOnBoarding, '/api/customer')
api.add_resource(AccountConfirmation, '/api/confirm')
api.add_resource(StaffRegistration, '/api/staff')
api.add_resource(CarHandler, '/api/vehicles')
api.add_resource(OrganizationHandler, '/api/organizations/all')
api.add_resource(MPIUnderwriting, '/api/transactions')
api.add_resource(BenefitHandler, '/api/benefits')
api.add_resource(LoadingsHandler, '/api/loadings')
api.add_resource(ExtensionHandler, '/api/extensions')




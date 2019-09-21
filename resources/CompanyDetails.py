"""
Resource for fetching all company details, including it's benefits, extensions, loadings and levies, given the ID.
"""
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.Loadings import Loadings
from models.ICLoadings import ICLoadings
from models.Benefits import Benefit
from models.Levies import Levies
from models.Extensions import Extension
from models.ICExtensions import ICExtensions
from models.ICBenefits import ICBenefits
from models.ICProducts import ICProducts
from models.Broker import Broker
from models.IndependentAgent import IndependentAgent
from models.TiedAgent import TiedAgents
from models.InsuranceCompany import InsuranceCompany
from models.UserRolePlacement import UserRolePlacement
from helpers import helpers as helper
from helpers.parsers import policy_parser
from helpers.CustomerNumber import CustomerNumber
from helpers.PolicyNumber import PolicyNoGenerator
import helpers.tokens as token_handler
import uuid


class CompanyDetails(Resource):
    @jwt_required
    def post(self):
        # get the insurance company details
        uid = get_jwt_identity()

        # get user role so that you can use it to get the agency_id,
        claims = get_jwt_claims()
        role = claims['role']

        # get company_id
        company = self.get_agency_id(role, uid)

        policy_details = policy_parser.parse_args()

        # store the products affiliated with a particular company, one insurance class has many subclasses
        insurance_class = policy_details['insurance_class']
        subclass = policy_details["sub_class"]
        if insurance_class and subclass:
            for i in subclass:
                new_product = ICProducts(
                    company.id, insurance_class, i)
                new_product.save()

        if policy_details['rate']:
            # set the insurance_company's rate
            data = {
                "rate": policy_details['rate']
            }
            company.update(data)

        if policy_details["ncd_rate"]:
            data = {
                "ncd_rate": policy_details["ncd_rate"]
            }
            company.update(data)

        response = helper.make_rest_success_response(
            "Success")
        return make_response(response, 200)

    @staticmethod
    def get_agency_id(role, uid):
        """
        Fetch the agent id depending the active user's role. Could be an independent agency, brokerage or tied agent
        """
        if role == "BR":
            # get brokerage by contact person
            broker = Broker.get_broker_by_contact_id(uid)
            return broker.broker_id

        elif role == "IC":
            insurance = InsuranceCompany.get_company_by_contact_person(uid)
            return insurance

        elif role == "TA":
            # get tied agency
            tied_agent = TiedAgents.get_tied_agent_by_user_id(uid)
            return tied_agent.id

        elif role == "IA":
            # get Independent agency by contact person
            ind_agent = IndependentAgent.get_agency_by_contact_person(uid)
            return ind_agent.id


class CompanyDetailsHandler(Resource):
    """
    Gets the company details given the company
    """
    @jwt_required
    def get(self, company_id):
        company_data = {}
        # get the company benefits
        benefits = ICBenefits.get_benefits_by_company_id(company_id)
        benefits_list = []
        if benefits:
            for i in benefits:
                # first get the benefit name since ICBenefits model only returns the benefit id
                benefit_name = Benefit.get_name_by_id(i.benefit)
                data = {
                    "id": i.id,
                    "name": benefit_name,
                    "free_limit": i.free_limit,
                    "max_limit": i.max_limit,
                    "rate": i.rate
                }
                benefits_list.append(data)
        # append benefits data to the company details list
        company_data.update({"benefits": benefits_list})

        # get the company loadings
        loadings_list = []
        loadings = ICLoadings.get_loadings_by_company_id(company_id)
        if loadings:
            for i in loadings:
                # first get the extension name since ICExtension model only returns the benefit id
                loading_name = Loadings.get_name_by_id(i.loading)
                data = {
                    "id": i.id,
                    "name": loading_name,
                    "rate": i.rate
                }
                loadings_list.append(data)
            # append loadings data to the company details list
            company_data.update({"loadings": loadings_list})

        # get the company extensions
        extensions_list = []
        extensions = ICExtensions.get_extensions_by_company_id(company_id)
        if extensions:
            for i in extensions:
                # first get the extension name since ICExtension model only returns the benefit id
                extension_name = Extension.get_name_by_id(i.extension)
                data = {
                    "id": i.id,
                    "name": extension_name,
                    "free_limit": i.free_limit,
                    "max_limit": i.max_limit,
                    "rate": i.rate
                }
                extensions_list.append(data)
            company_data.update({"extensions": extensions_list})
        response_msg = helper.make_rest_success_response(
            "Success", company_data)
        return make_response(response_msg, 200)

from app import application, db
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.Role import Role
from models.CompanyDetails import CompanyDetails
from models.LicencedClasses import LicencedClasses
from models.UserRolePlacement import UserRolePlacement
import helpers.helpers as helper
from helpers.parsers import customer_parser
from helpers.CustomerNumber import CustomerNumber
from helpers.parsers import user_parser
import helpers.tokens as token_handler
import uuid


class Companies(Resource):
    def post(self):
        pass

    def get(self):
        """
        Get all insurance companies, together with the company details"""   
        # fetch all companies, then their details.
        companies_list = CompanyDetails.get_companies()
        if companies_list:
            # get company details
            list_of_companies = []
            for company in companies_list:
                policies = LicencedClasses.get_company_classes(company.id)
                data = {
                    "id": company.id,
                    "name": company.company_name,
                    "products": policies
                }
                list_of_companies.append(data)

            response = helper.make_rest_success_response(
                "Success", list_of_companies)
            return make_response(response, 200)
        else:
            response = helper.make_rest_success_response(
                "No company registered yet")
            return make_response(response, 404)

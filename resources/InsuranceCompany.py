from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.Role import Role
from models.CompanyDetails import CompanyDetails
from models.LicencedClasses import LicencedClasses
from models.UserRolePlacement import UserRolePlacement
from helpers import helpers as helper
from helpers.parsers import customer_parser
from helpers.CustomerNumber import CustomerNumber
from helpers.parsers import user_parser
import helpers.tokens as token_handler
import uuid
import random


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

                list_of_products = company['products']
                licenced_classes = [1, 2, 3, 4, 5,
                                    6, 7, 8, 9, 10, 11, 12, 13, 14]

                # Only return companies that sell general insurance policies
                if len(company['products']) != 0:
                    if random.choice(company['products']) in licenced_classes:
                        list_of_companies.append(company)

            response = helper.make_rest_success_response(
                "Success", list_of_companies)
            return make_response(response, 200)
        else:
            response = helper.make_rest_success_response(
                "No company registered yet")
            return make_response(response, 404)

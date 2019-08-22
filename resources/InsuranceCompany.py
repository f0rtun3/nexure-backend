from app import app, db
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.User import User
from models.UserProfile import UserProfile
from models.UserPermissions import UserPermissions
from models.IndependentAgent import IndependentAgent
from models.TiedAgent import TiedAgents
from models.Broker import Broker
from models.BRStaff import BRStaff
from models.TAStaff import TAStaff
from models.IAStaff import IAStaff
from models.Role import Role
from models.InsuranceCompany import InsuranceCompany
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
        Get all insurance companies, together with the company details
        """
        # fetch all companies, then their details.

        companies_list = InsuranceCompany.get_all_companies()
        if companies_list:
            # get company details
            list_of_companies = []
            for company in companies_list:
                data = {
                    "id": company.id,
                    "name": company.company_details.company_name,
                    "email": company.company_details.company_email,
                    "company_number": company.company_phone,
                    "rate": company.rate
                }
                list_of_companies.append(data)

            response = helper.make_rest_success_response(
                "Success", {"insurance_companies": companies_list})
            return make_response(response, 200)
        else:
            response = helper.make_rest_success_response(
                "No company registered yet")
            return make_response(response, 404)
            return
            

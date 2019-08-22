"""
Resource for fetching customer details. This is necessary so that an agent or broker can pull the customer details 
using one of their attributes such as an email.
"""
from app import app
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.User import User
from models.Broker import Broker
from models.IndependentAgent import IndependentAgent
from models.UserRolePlacement import UserRolePlacement
from models.OrganizationCustomer import OrganizationCustomer
from models.IndividualCustomer import IndividualCustomer
from models.Role import Role
from models.TiedAgent import TiedAgents
from models.BRCustomer import BRCustomer
from models.TACustomer import TACustomer
from models.IACustomer import IACustomer
from models.Driver import Driver
from models.UserProfile import UserProfile
import helpers.helpers as helper
from helpers.parsers import underwriting_parser
import helpers.tokens as token_handler
import uuid
import json

class CustomerDetails(Resource):
    def post(self):
        pass

    def get(self, email):
        """
        Get customer details using an attribute such as email
        """
        # object to store user details
        data = {}
        # get the agency id of the organization requesting for customer details
        contact_id = get_jwt_identity()
        # get user role
        claims = get_jwt_claims()
        role = claims['role']
        company_id = self.get_agency_id(role, contact_id)
        # get user id from customer email
        customer = User.get_user_by_email(email)
        # get customer details
        customer_details = self.get_customer_details_by_user_id(customer.id)
        
        response_msg = helper.make_rest_success_response("Success", customer_details)
        return make_response(response_msg, 200)

    @staticmethod
    def get_customer_details_by_user_id(user_id):
        # use the user id to determine the customer's role, whether IND or ORG
        role_id = UserRolePlacement.fetch_role_by_user_id(user_id)
        # get role name using role_id
        role = Role.fetch_role_by_id(role_id)
        if role == 'IND':
            customer_no = IndividualCustomer.get_customer_number(user_id)
            if customer_no:
                user_profile = UserProfile.get_profile_by_user_id(user_id)
                data = {
                    "customer_number": customer_no,
                    "first_name": user_profile.first_name,
                    "last_name": user_profile.last_name,
                    "phone_number": user_profile.phone,
                    "kra_pin": user_profile.kra_pin,
                    "id_passport": user_profile.id_passport
                }
                return data
            else:
                response_msg = helper.make_rest_fail_response(
                    "Customer does not exist")
                return make_response(response_msg, 404)

        elif role == 'ORG':
            # When the customer is an organization, their details are stored directly in the organization model
            # (not linked with the user profile)
            customer = OrganizationCustomer.get_customer_by_contact(user_id)
            if customer:
                # get customer details
                data = {}
                # TODO: Confirm from Tony whether to fetch organization details or contact person
                pass

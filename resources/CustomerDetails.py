"""
Resource for fetching customer details. This is necessary so that an agent or broker can pull the customer details 
using one of their attributes such as an email.
"""
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.User import User
from models.Broker import Broker
from models.CompanyDetails import CompanyDetails
from models.IndependentAgent import IndependentAgent
from models.UserRolePlacement import UserRolePlacement
from models.ChildPolicy import ChildPolicy
from models.MasterPolicy import MasterPolicy
from models.OrganizationCustomer import OrganizationCustomer
from models.IndividualCustomer import IndividualCustomer
from models.Role import Role
from models.CarModel import CarModel
from models.VehicleDetails import VehicleDetails
from models.Benefits import Benefit
from models.Extensions import Extension
from models.TiedAgent import TiedAgents
from models.ICBenefits import ICBenefits
from models.ICExtensions import ICExtensions
from models.Driver import Driver
from models.UserProfile import UserProfile
from helpers import helpers as helper
from helpers.parsers import underwriting_parser
import helpers.tokens as token_handler
import uuid
import json


class CustomerDetails(Resource):
    def post(self):
        pass

    @jwt_required
    def get(self, email):
        """
        Get customer details using an attribute such as email
        """
        # object to store all user data
        data = {}
        # get the agency id of the organization requesting for customer details
        contact_id = get_jwt_identity()
        # get user role
        claims = get_jwt_claims()
        role = claims['role']
        # company_id = self.get_agency_id(role, contact_id)
        # get user id from customer email
        customer = User.get_user_by_email(email)

        # get customer details using the user_id
        customer_details = self.get_customer_details(customer.id)
        data.update({"customer": customer_details})

        # get the cover data using the customer number in customer details
        cust_no = customer_details["customer_number"]
        cover_details = self.get_cover_details(cust_no)
        data.update({"cover_details": cover_details})

        response_msg = helper.make_rest_success_response(
            "Success", data)
        return make_response(response_msg, 200)

    def get_customer_details(self, user_id):
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
                    "id_passport": user_profile.id_passport,
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

    def get_cover_details(self, customer_number):
        """
        Get customer details: The master policy under which
        the customer has been enrolled and the child polices under it.
        """
        data = []
        # get master policies with this customer number
        ms_policies = MasterPolicy.get_policy_by_customer_no(customer_number)
        for master in ms_policies:
            master_details = {
                "id": master.id,
                "mp_number": master.mp_number,
                "date_created": master.date_created,
                'active': master.status,
                "expiry_date": master.date_expiry
            }
            data.append(master_details)
        return data

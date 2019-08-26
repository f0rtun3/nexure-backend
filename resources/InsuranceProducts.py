from app import app
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.User import User
from models.MasterPolicy import MasterPolicy
from models.UserProfile import UserProfile
from models.ChildPolicy import ChildPolicy
from models.VehicleDetails import VehicleDetails
from models.Broker import Broker
from models.IndependentAgent import IndependentAgent
from models.TiedAgent import TiedAgents
from models.BRCustomer import BRCustomer
from models.TACustomer import TACustomer
from models.IACustomer import IACustomer
from models.ICProducts import ICProducts
from models.Role import Role
from models.InsuranceClass import InsuranceClass
from models.InsuranceSubclass import InsuranceSubclass
from models.InsuranceCompany import InsuranceCompany
from models.Driver import Driver
import helpers.helpers as helper
from helpers.parsers import policy_parser
from helpers.CustomerNumber import CustomerNumber
from helpers.PolicyNumber import PolicyNoGenerator
import helpers.tokens as token_handler
import uuid
import json


class InsuranceProducts(Resource):
    """
    Every insurance company has to add the products they offer,
    The post request recieves the product id, which represents the insurance class, and the products children,
    which represents the insurance subclasses
    """
    @jwt_required
    def post(self):
        # get the insurance company details
        uid = get_jwt_identity()

        # get user role so that you can use it to get the agency_id,
        claims = get_jwt_claims()
        role = claims['role']

        # get company_id
        company_id = self.get_agency_id(role, uid)

        policy_details = policy_parser.parse_args()

        # store the products affiliated with a particular company
        new_product = ICProducts(
            company_id, policy_details['insurance_class'], policy_details['sub_class'])
        new_product.save()
        response = helper.make_rest_success_response(
            "Product added successfully")
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
            return insurance.id

        elif role == "TA":
            # get tied agency
            tied_agent = TiedAgents.get_tied_agent_by_user_id(uid)
            return tied_agent.id

        elif role == "IA":
            # get Independent agency by contact person
            ind_agent = IndependentAgent.get_agency_by_contact_person(uid)
            return ind_agent.id

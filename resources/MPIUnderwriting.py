"""
Resource for policy underwriting
"""
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
from models.BRStaff import BRStaff
from models.TAStaff import TAStaff
from models.IAStaff import IAStaff
from models.Role import Role
from models.InsuranceClass import InsuranceClass
from models.InsuranceSubClass import InsuranceSubClass
from models.InsuranceCompany import InsuranceCompany
from models.OrganizationCustomer import OrganizationCustomer
from models.Driver import Driver
import helpers.helpers as helper
from helpers.parsers import underwriting_parser
from helpers.CustomerNumber import CustomerNumber
from helpers.PolicyNumber import PolicyNoGenerator
import helpers.tokens as token_handler
import uuid
import json


class MPIUnderwriting(Resource):
    def post(self):
        # get the current agency details
        uid = get_jwt_identity()

        # get user role so that you can use it to get the agency_id,
        claims = get_jwt_claims()
        role = claims['role']

        # get company_id
        company_id = self.get_agency_id(role, uid)

        policy_details = underwriting_parser.parse_args()
        # get the transaction type i.e could be a new policy, renewal or endorsement or extension
        transaction_type = policy_details['transaction_type']
        # if it's a new transaction (customer had not been enrolled into this kind of policy before)
        if transaction_type == 'NEW':
            # Get user details from customer number
            customer_number = policy_details['customer_number']

            # get the driver details
            driver = policy_details['driver_details']
            new_driver = Driver(
                driver.first_name,
                driver.last_name,
                driver.gender,
                driver.phone,
                driver.birth_date
            )
            new_driver.save()
            # store vehicle details
            vehicle = policy_details['vehicle_details']
            new_vehicle = VehicleDetails(
                vehicle.reg_number,
                vehicle.model,
                vehicle.color,
                vehicle.body_type,
                vehicle.origin,
                vehicle.sum_insured,
                new_driver.id
            )
            new_vehicle.save()

            # create master policy
            # first generate mp number
            new_policy = PolicyNoGenerator('MS')
            # get class details after receiving the class name from the front end e.g if name is Motor Private
            class_details = InsuranceClass.get_class_by_name('Motor Private')
            # generate master policy number using the code
            new_policy.set_mpi(class_details.acronym)
            ms_policy_number = new_policy.generate_policy_no()
            master_policy = MasterPolicy(
                ms_policy_number, customer_number, policy_details['expiry_date'])
            master_policy.save()

            # create child policy
            # first generate the child policy number
            new_child_policy = PolicyNoGenerator('CH')
            # get sub class details e.g if comprehensive
            subclass_details = InsuranceSubClass.get_class_by_name(
                'Comprehensive')
            # generate child policy
            # TODO: Generate acronym for child policies for this instance we use PCI for test purposes
            new_child_policy.set_pci('PCI')
            ch_policy_number = new_child_policy.generate_policy_no()
            # Finally create the child policy
            child_policy = ChildPolicy(
                new_vehicle.id,
                customer_number,
                policy_details['rate'],
                policy_details['expiry_date'],
                policy_details['premium_amount'],
                policy_details['expiry_date'],
                policy_details['transaction_type'],
                master_policy.id
            )
            child_policy.save()
            """
            Add benefits from the list of benefits sent in the post request
            """
            for i in policy_details['benefits']:
                child_policy.add_benefit(i.benefit_id, i.amount)
                child_policy.save()
            """
            Add loadings from the list of loadings sent in the post request
            """
            for i in policy_details['loadings']:
                child_policy.add_loading(i.loading_id, i.amount)
                child_policy.save()
            """
            Add extensions from the list of extensions sent in the post request
            """
            for i in policy_details['extensions']:
                child_policy.add_extension(i.extension_id, i.amount)
                child_policy.save()

            """
            Send response if successfully onboarded
            """
            response = helper.make_rest_success_response(
                "Congratulations! The customer was enrolled successfully ")
            return make_response(response, 200)

        # if it's an endorsement i.e the customer wants to add an item under the master policy
        elif transaction_type == 'ENDORSEMENT':
            pass

            # if the policy has expired and customer wants to renew it
        elif transaction_type == 'RENEWAL':
            pass
            # if the customer want's to extend the cover to cater for extra losses
        elif transaction_type == 'EXTENSION':
            pass
            # if the customer decided to cancel the entire or part of his cover, before it expires, then they are entitled for a refund
        elif transaction_type == 'REFUND':
            pass
            # If the customer decides to cancel their cover midway
        elif transaction_type == 'CANCELLATION':
            pass

    def get(self):
        # fetch list of child policies associated with a particular user, using their email
        pass

    def update(self):
        # use policy with a particular master and child policy number
        pass

    @staticmethod
    def get_agency_id(role, uid):
        """
        Fetch the agent id depending the active user's role. Could be an independent agency, brokerage or tied agent
        """
        if role == "BR":
            # get brokerage by contact person
            broker = Broker.get_broker_by_contact_id(uid)
            return broker.broker_id
        elif role == "TA":
            # get tied agency
            tied_agent = TiedAgents.get_tied_agent_by_user_id(uid)
            return tied_agent.id

        elif role == "IA":
            # get Independent agency by contact person
            ind_agent = IndependentAgent.get_agency_by_contact_person(uid)
            return ind_agent.id
    
    @staticmethod
    

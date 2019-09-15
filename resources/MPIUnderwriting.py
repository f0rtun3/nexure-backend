"""
Resource for policy underwriting
"""
from app import application
from flask import make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.User import User
from models.MasterPolicy import MasterPolicy
from models.UserProfile import UserProfile
from models.ChildPolicy import ChildPolicy
from models.Broker import Broker
from models.IndependentAgent import IndependentAgent
from models.TiedAgent import TiedAgents
from models.Role import Role
from models.CompanyDetails import CompanyDetails
from models.InsuranceClass import InsuranceClass
from models.InsuranceSubclass import InsuranceSubclass
from models.InsuranceCompany import InsuranceCompany
from models.OrganizationCustomer import OrganizationCustomer
from Controllers.ChildController import ChildController
from Controllers.MasterController import MasterController
import helpers.helpers as helper
from helpers.parsers import underwriting_parser
from helpers.CustomerNumber import CustomerNumber
from helpers.PolicyNumber import PolicyNoGenerator
import helpers.tokens as token_handler
import uuid
import json
from datetime import datetime


class MPIUnderwriting(Resource):
    @jwt_required
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
        if policy_details:
            transaction_type = policy_details['transaction_type']
            # if it's a new transaction (customer had not been enrolled into this kind of policy before)
            if transaction_type == 'NET':
                # Create master policy, first generate master policy number
                index = MasterPolicy.query.all()
                new_policy = PolicyNoGenerator('MS', len(index))
                # Get class details after receiving the class id from the front end e.g if name is Motor Private
                class_details = InsuranceClass.get_class_by_id(
                    policy_details['class_id'])
                # generate master policy number using the acronym from the class details
                new_policy.set_mpi(class_details.acronym)
                ms_policy_number = new_policy.generate_policy_no()

                master_policy = MasterController.create_master_policy(
                    ms_policy_number,
                    policy_details['customer_number'],
                    policy_details['date_expiry'],
                    policy_details['insurance_company']
                )

                # create child policy with details
                child_policy_id = self.create_child(
                    policy_details, company_id, master_policy)
                # Send response if successfully onboarded with the onboarded data
                # data = self.get_cover_data(child_policy_id)
                response = helper.make_rest_success_response(
                    "Congratulations! The customer was enrolled successfully. Cover will be"
                    " activated after payment is made", child_policy_id)
                return make_response(response, 200)

            # if it's an endorsement i.e the customer wants to add an item under the master policy
            elif transaction_type == 'END':
                # get the master policy by master number
                master_number = policy_details["master_policy"]
                endorsed_policy = MasterPolicy.get_policy_by_mp_number(
                    master_number)
                # check whether the policy has expired.
                time_difference = endorsed_policy.date_expiry - datetime.now()
                if time_difference.days > 1:
                    # Then endorse it with the child policy details:
                    child_policy_id = self.create_child(
                        policy_details, company_id, endorsed_policy)
                    # endorsement successful
                    response = helper.make_rest_success_response(
                        "Endorsement successfull", child_policy_id)
                    return make_response(response, 200)

                else:
                    response = helper.make_rest_fail_response(
                        "Failed! Master policy expired. Kindly wait for renew it the endorse.")
                    return make_response(response, 500)

            elif transaction_type == 'RET':
                #   renew the transaction
                if MasterController.renew_transaction(policy_details['master_policy_id'],
                                                      policy_details['expiry_date'],
                                                      transaction_type):
                    return make_response(helper.make_rest_success_response("Policy renewed successfully"),
                                         200)
                else:
                    return make_response(helper.make_rest_success_response("Failed to renew Policy"))
                # if the customer want's to extend the cover to cater for extra losses
            elif transaction_type == 'EXTENSION':
                pass
                # if the customer decided to cancel the entire or part
                # of his cover, before it expires, then they are entitled for a refund
            elif transaction_type == 'REFUND':
                pass
                # If the customer decides to cancel their cover midway
            elif transaction_type == 'CANCELLATION':
                pass
        else:
            response = helper.make_rest_fail_response("Failed")
            return make_response(response, 500)

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

        elif role == "IC":
            insurance = InsuranceCompany.get_company_by_contact_person(uid)
            return insurance.id

    @staticmethod
    def create_child(policy_details, company_id, master_policy):
        # Create child policy, first generate the child policy number
        count = ChildPolicy.query.all()
        new_child_policy = PolicyNoGenerator('CH', len(count))
        # Get sub class details e.g if comprehensive
        subclass_details = InsuranceSubclass.get_class_by_id(
            policy_details['subclass_id'])
        # Generate child policy
        new_child_policy.set_pci(subclass_details.acronym)
        ch_policy_number = new_child_policy.generate_policy_no()

        # Initialize the child controller
        child_controller = ChildController()

        # Get the driver details
        driver = policy_details['driver_details']
        # add driver details to the child controller
        child_controller.add_driver_details(
            driver["first_name"],
            driver["last_name"],
            driver["gender"],
            driver["phone"],
            driver["birth_date"]
        )
        # store vehicle details
        vehicle = policy_details['vehicle_details']
        child_controller.add_vehicle_details(
            vehicle["reg_number"],
            vehicle["model"],
            vehicle["color"],
            vehicle["body_type"],
            vehicle["origin"],
            vehicle["sum_insured"],
            vehicle["no_of_seats"],
            vehicle["manufacture_year"],
            vehicle["engine"]
        )
        # Add modifications
        modifications = policy_details['modifications']
        if modifications:
            for i in modifications:
                child_controller.add_modifications(
                    i["accessory_name"],
                    i["make"],
                    i["estimated_value"],
                    i["serial_no"]
                )
        # Finally create the child policy
        child_policy_id = child_controller.create_child_policy(
            ch_policy_number,
            policy_details["customer_number"],
            policy_details['rate'],
            # Set date expiry as the expiry date of the endorsed master policy
            master_policy.date_expiry,
            policy_details['premium_amount'],
            policy_details['transaction_type'],
            # id of the underwriting agency
            company_id,
            policy_details['insurance_company'],
            policy_details['pricing_module'],
            # id of the endorsed policy id
            master_policy.id,
            # subclass name
            subclass_details.name
        )

        # Add benefits from the list of benefits sent in the post request
        if policy_details['benefits']:
            ChildController.add_benefits(
                policy_details['benefits'], child_policy_id)

        # Add extensions from the list of extensions sent in the post request
        if policy_details['extensions']:
            ChildController.add_extensions(
                policy_details["extensions"], child_policy_id)

        return child_policy_id

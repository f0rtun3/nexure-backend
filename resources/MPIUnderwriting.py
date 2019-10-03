"""
Resource for policy underwriting
"""
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
from models.VehicleDetails import VehicleDetails
from models.OrganizationCustomer import OrganizationCustomer
from Controllers.ChildController import ChildController
from Controllers.MasterController import MasterController
from helpers import helpers as helper
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
                # create child policy number
                child_policy_no = self.create_child_policy_number(
                    policy_details)
                # Create child policy with details
                child_policy_id = self.create_child(
                    policy_details, child_policy_no, company_id, master_policy)
                # Send response if successfully onboarded with the onboarded data
                # data = self.get_cover_data(child_policy_id)
                response = helper.make_rest_success_response(
                    "Congratulations! The customer was enrolled successfully. Cover will be"
                    " activated after payment is made", child_policy_id)
                return make_response(response, 200)

            # if it's an endorsement i.e the customer wants to add an item under the master policy
            elif transaction_type == 'END':
                # In this case, you could be endorsing the child policy or master policy
                # get the master policy by master policy id
                if policy_details["master_policy_id"]:
                    endorsed_policy = MasterPolicy.get_policy_by_id(
                        policy_details["master_policy_id"])

                    # check whether the policy has expired.
                    time_difference = (
                        endorsed_policy.date_expiry - datetime.now()).days
                    if time_difference > 1:
                        # create child policy number
                        child_policy_no = self.create_child_policy_number(
                            policy_details)
                        # Then endorse it with the child policy details:
                        child_policy_id = self.create_child(
                            policy_details, child_policy_no, company_id, endorsed_policy)
                        # endorsement successful
                        response = helper.make_rest_success_response(
                            "Endorsement successful", child_policy_id)
                        return make_response(response, 200)

                    else:
                        response = helper.make_rest_fail_response(
                            "Failed! Policy expired. Kindly renew it then endorse.")
                        return make_response(response, 500)

                if policy_details["child_policy_id"]:
                    
                    # In this case we add a benefit to the child policy
                    endorsed_policy = ChildPolicy.get_child_by_id(
                        policy_details["child_policy_id"])
                    
                    # Check whether the policy has expired.
                    time_difference = (
                        endorsed_policy.date_expiry - datetime.now()).days
                    if time_difference > 1:
                        # revise the child policy with the a new premium amount
                        revised_policy = self.revise_child_policy(
                            "END", endorsed_policy, policy_details)

                        # append the new benefit to revised policy
                        child_controller = ChildController()
                        child_controller.add_benefits(
                            revised_policy, policy_details['benefits'])
                        
                        # endorsement successful
                        response = helper.make_rest_success_response(
                            "Endorsement successful", revised_policy)
                        return make_response(response, 200)
                    
                    else:
                        response = helper.make_rest_fail_response(
                            "Failed! Policy expired. Kindly renew it then endorse.")
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
            elif transaction_type == 'EXT':
                # get child policy
                extended_policy = ChildPolicy.get_child_by_id(
                    policy_details['child_policy_id'])
                # check whether policy is less than one year old (365) days
                time_difference = (
                    datetime.now() - extended_policy.date_activated).days
                if time_difference < 365:
                    # revise the child policy with the a new premium amount
                    revised_policy = self.revise_child_policy(
                        "EXT", extended_policy, policy_details)

                    # append the new extension to revised policy
                    child_controller = ChildController()
                    child_controller.add_benefits(
                        revised_policy, policy_details["extensions"])
                    
                    return make_response(helper.make_rest_success_response("Policy extended successfully", revised_policy),
                                         200)
                else:
                    return make_response(helper.make_rest_success_response("Failed to extend policy"))

            elif transaction_type == 'REF':
                refund_type = policy_details["refund_type"]
                # fetch the child policy to be refunded or updated
                child_policy = ChildPolicy.get_child_by_id(
                    policy_details['child_policy_id'], True)

                # get premium amount
                premium_amount = child_policy.premium_amount
                refund_amount = None

                # TODO: create model that stores transactions, the amount paid below is dummy data
                amount_paid = 800
                if refund_type == "sold":
                    # deactivate the previous child policy so that we can create a new one
                    child_policy.deactivate()

                    # initialize child controller
                    child_controller = ChildController()
                    child_controller.create_child_policy(
                        child_policy.cp_number,
                        child_policy.customer_number,
                        child_policy.rate,
                        child_policy.date_expiry,
                        # Zero premium amount
                        0,
                        "REF",
                        child_policy.agency_id,
                        child_policy.company,
                        child_policy.pricing_model,
                        child_policy.master_policy,
                        child_policy.subclass,
                        child_policy.vehicle,
                        "sold"                        
                    )

                    # if the policy has lasted for less than thirty days refund full amount paid
                    period_lasted = (datetime.now() -
                                     child_policy.date_activated).days
                    if period_lasted <= 30:
                        refund_amount = amount_paid

                    # if more than 30 days, deduct the cost incured for the period the cover has run
                    else:
                        cost_incurred = (premium_amount / 365) * period_lasted
                        if amount_paid >= cost_incurred:
                            refund_amount = amount_paid - cost_incurred
                        # TODO: Create a clause for handling amount paid

                elif refund_type == "benefit":
                    # deactivate previous policy
                    child_policy.deactivate()

                    # create new transaction with the same child policy number and vehicle details
                    revised_policy = self.revise_child_policy("REF", child_policy, policy_details, "benefit_removed")

                    # Append any remaining benefits
                    # first get the id of the cancelled benefit
                    cancelled_benefit = policy_details["benefit_id"]
                    # get remaining
                    remaining_benefits = [i.serialize() for i in child_policy.benefits if i.id != cancelled_benefit]

                    # append them to the revised policy
                    ChildController.add_benefits(remaining_benefits, revised_policy)

                    # get refund amount based on the new recalculated premium amount
                    new_premium_amount = policy_details["premium_amount"]
                    previous_premium = child_policy.premium_amount

                    # difference
                    premium_change = previous_premium - new_premium_amount

                    # If the policy has run for 30 days, refund full difference
                    period_lasted = (datetime.now() -
                                     child_policy.date_activated).days
                    amount_to_revise = (period_lasted / 365) * premium_change
                    refund_amount = amount_paid

                    # TODO: Revise transaction table and update date due using the amount to revise

                elif refund_type == "sum_insured":
                    # create new child policy based on new details after downward revision of sum insured
                    # deactivate previous policy
                    child_policy.deactivate()

                    # create transaction with new details
                    new_child = self.create_child(
                        policy_details, child_policy.cp_number, company_id, child_policy.master_policy)

                    # TODO: update with new dates
                    new_child.activate()

                    # get refund amount based on the new recalculated premium amount
                    new_premium_amount = policy_details["premium_amount"]
                    previous_premium = child_policy.premium_amount

                    # difference
                    premium_change = previous_premium - new_premium_amount

                    # If the policy has run for 30 days, refund full difference
                    period_lasted = (datetime.now() -
                                     child_policy.date_activated).days
                    amount_to_revise = (period_lasted / 365) * premium_change
                    refund_amount = amount_to_revise

                    # TODO: Revise transaction table and update date due using the amount to revise

                return make_response(helper.make_rest_success_response("Refund successful", refund_amount),
                                     200)

            elif transaction_type == 'CNC':
                # To cancel a transaction
                child_controller = ChildController()
                child_controller.cancel(policy_details['child_policy_id'])
                return make_response(helper.make_rest_success_response("Policy cancelled successfully"),
                                     200)

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
    def create_child(policy_details, child_policy_no, company_id, master_policy):

        # get subclass details
        subclass_details = InsuranceSubclass.get_class_by_id(
            policy_details['subclass_id'])

        # Initialize the child controller
        child_controller = ChildController()

        # Get the driver details
        driver = policy_details['driver_details']
        # add driver details to the child controller
        if driver:
            child_controller.add_driver_details(
                driver["first_name"],
                driver["last_name"],
                driver["gender"],
                driver["phone"],
                driver["birth_date"]
            )
        # store vehicle details
        vehicle = policy_details['vehicle_details']

        # add child details
        if vehicle:
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
            child_policy_no,
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

    @staticmethod
    def create_child_policy_number(policy_details):
        # Create child policy, first generate the child policy number
        count = ChildPolicy.query.all()
        new_child_policy = PolicyNoGenerator('CH', len(count))
        # Get sub class details e.g if comprehensive
        subclass_details = InsuranceSubclass.get_class_by_id(
            policy_details['subclass_id'])
        # Generate child policy
        new_child_policy.set_pci(subclass_details.acronym)
        ch_policy_number = new_child_policy.generate_policy_no()
        return ch_policy_number

    @staticmethod
    def revise_child_policy(transaction_type, previous_policy, policy_details, reason=None):
        # deactivate old policy
        previous_policy.deactivate()

        # Create an update of the old policy, to accomodate the changes made
        child_controller = ChildController()
        revised_policy = child_controller.create_child_policy(
            previous_policy.cp_number,
            previous_policy.customer_number,
            previous_policy.rate,
            previous_policy.date_expiry,
            # new premium amount
            policy_details["premium_amount"],
            transaction_type,
            previous_policy.agency_id,
            previous_policy.company,
            previous_policy.pricing_model,
            previous_policy.master_policy,
            previous_policy.subclass,
            previous_policy.vehicle,
            reason,
            
        )
        # TODO: Look at the dates in all policies and change them appropriately
        # activate the updated policy
        revised_policy.activate()
        return revised_policy

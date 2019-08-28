"""
Resource for policy underwriting
"""
from app import app
from flask import make_response, jsonify
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
from models.ICBenefits import ICBenefits
from models.ICExtensions import ICExtensions
from models.PolicyBenefits import PolicyBenefits
from models.Benefits import Benefit
from models.Extensions import Extension
from models.PolicyExtensions import PolicyExtensions
from models.InsuranceClass import InsuranceClass
from models.InsuranceSubclass import InsuranceSubclass
from models.InsuranceCompany import InsuranceCompany
from models.OrganizationCustomer import OrganizationCustomer
from models.VehicleModifications import VehicleModifications
from models.Driver import Driver
import helpers.helpers as helper
from helpers.parsers import underwriting_parser
from helpers.CustomerNumber import CustomerNumber
from helpers.PolicyNumber import PolicyNoGenerator
import helpers.tokens as token_handler
import uuid
import json


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
                # Get user details from customer number
                customer_number = policy_details['customer_number']

                # get the driver details
                driver = policy_details['driver_details']

                new_driver = Driver(
                    driver["first_name"],
                    driver["last_name"],
                    driver["gender"],
                    driver["phone"],
                    driver["birth_date"]
                )
                new_driver.save()
                # store vehicle details
                vehicle = policy_details['vehicle_details']
                new_vehicle = VehicleDetails(
                    vehicle["reg_number"],
                    vehicle["model"],
                    vehicle["color"],
                    vehicle["body_type"],
                    vehicle["origin"],
                    vehicle["sum_insured"],
                    new_driver.id,
                    vehicle["no_of_seats"],
                    vehicle["manufacture_year"],
                    vehicle["engine"]
                )
                new_vehicle.save()

                # store modifications
                modifications = policy_details['modifications']
                if modifications:
                    for i in modifications:
                        new_accessory = VehicleModifications(
                            i["accessory_name"], i["make"], i["estimated_value"], i["serial_no"], new_vehicle.id)
                        new_accessory.save()

                # create master policy
                # first generate mp number
                new_policy = PolicyNoGenerator('MS')
                # get class details after receiving the class name from the front end e.g if name is Motor Private
                class_details = InsuranceClass.get_class_by_id(
                    policy_details['class_id'])
                # generate master policy number using the code
                new_policy.set_mpi(class_details.acronym)
                ms_policy_number = new_policy.generate_policy_no()
                master_policy = MasterPolicy(
                    ms_policy_number, customer_number, policy_details['date_expiry'], policy_details['insurance_company'])
                master_policy.save()

                # create child policy
                # first generate the child policy number
                new_child_policy = PolicyNoGenerator('CH')
                # get sub class details e.g if comprehensive
                subclass_details = InsuranceSubclass.get_class_by_id(
                    policy_details['subclass_id'])
                # generate child policy
                # TODO: Generate acronym for child policies for this instance we use PCI for test purposes
                new_child_policy.set_pci('PCI')
                ch_policy_number = new_child_policy.generate_policy_no()
                # Finally create the child policy
                child_policy = ChildPolicy(
                    ch_policy_number,
                    new_vehicle.id,
                    policy_details["customer_number"],
                    # change rate and replace with company rate when set
                    policy_details['rate'],
                    policy_details['date_expiry'],
                    policy_details['premium_amount'],
                    policy_details['transaction_type'],
                    4,
                    policy_details['insurance_company'],
                    policy_details['pricing_module'],
                    master_policy.id,
                )
                child_policy.save()
                """
                Add benefits from the list of benefits sent in the post request
                """
                if policy_details['benefits']:
                    for i in policy_details['benefits']:
                        benefit = Benefit.get_benefit_by_name("Windscreen and Staff")
                        ic_benefit = ICBenefits.get_ic_benefit(benefit.id)
                        policy_benefit = PolicyBenefits(child_policy.id, ic_benefit.id, i["value"])
                        policy_benefit.save()

                """
                Add extensions from the list of extensions sent in the post request
                """
                if policy_details['extensions']:
                    for i in policy_details['extensions']:
                        extension = Extension.get_extension_id_by_name(i["name"])
                        ic_extension = ICExtensions.get_ic_extension(extension.id)
                        policy_extension = PolicyExtensions(child_policy.id, ic_extension, i["value"])
                        policy_extension.save()
                """
                Add loadings from the list of loadings sent in the post request
                """
                if policy_details['loadings']:
                    for i in policy_details['loadings']:
                        child_policy.add_loading(i.loading_id, i.amount)
                        child_policy.save()
                
                """
                Send response if successfully onboarded with the onboarded data
                """
                # data = self.get_cover_data(child_policy.id)
                response = helper.make_rest_success_response(
                    "Congratulations! The customer was enrolled successfully. Cover will be activated after payment is made.")
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
        else:
            response = helper.make_rest_fail_response("Failed")
            return make_response(response, 500)

    def get(self, ):
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

        elif role == "IC":
            insurance = InsuranceCompany.get_company_by_contact_person(uid)
            return insurance.id

    @staticmethod
    def get_cover_data(self, child_id):
        """
        Get all cover data
        """
        cover_data = {}
        child_policy = ChildPolicy.get_child_by_id(child_id)

        cover_data.update({'transaction_type': child_policy.transaction_type})
        cover_data.update({'child_policy_no': child_policy.cp_number})
        cover_data.update({'customer_number': child_policy.customer_number})
        cover_data.update({'company': child_policy.company})
        cover_data.update({'rate': child_policy.rate})
        cover_data.update({'premium_amount': child_policy.premium_amount})
        cover_data.update({'date_registered': child_policy.date_registered})

        # get master policy id
        master = child_policy.master_policy
        master_details = {
            "mp_number": master.mp_number,
            "company": master.company,
            "date_created": master.date_created
        }
        cover_data.update({"master_policy": master_details})
        # get_benefits
        benefits = []
        for i in child_policy.benefits:
            data = {
                "id": i.ic_benefit_id,
                "amount": i.amount
            }
            benefits.append(data)
        cover_data.update({"benefits": benefits})

        # get_loadings
        loadings = []
        for i in child_policy.loadings:
            data = {
                "id": i.ic_loadings_id,
                "amount": i.amount
            }
            loadings.append(data)
        cover_data.update({"loadings": loadings})

        # get_extensions
        extensions = []
        for i in child_policy.extensions:
            data = {
                "id": i.ic_loadings_id,
                "amount": i.amount
            }
            extensions.append(data)
        cover_data.update({"loadings": extensions})

        # return all data
        return cover_data

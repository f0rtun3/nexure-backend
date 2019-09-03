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
import helpers.helpers as helper
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
        data.update({"cover details": cover_details})

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
            comp = CompanyDetails.get_company_by_id(master.company)
            master_details = {
                "mp_number": master.mp_number,
                "company": comp.company_name,
                "date_created": master.date_created,
                'status': master.status
            }

            child_policies = []
            for i in master.child_policy:
                # Use child policy id
                child_id = i.id
                child_data = self.get_child_policy_data(child_id)
                child_policies.append(child_data)

            master_details.update({"children": child_policies})
            data.append({"master_policy": master_details})
        return data

    # get all child policies related to that master and their details
    def get_child_policy_data(self, child_id):
        """
        Get all child data
        """
        child_data = {}
        child_policy = ChildPolicy.get_child_by_id(child_id)
        child_data.update({'transaction_type': child_policy.transaction_type})
        child_data.update({'child_policy_no': child_policy.cp_number})
        child_data.update({'customer_number': child_policy.customer_number})
        child_data.update({'rate': child_policy.rate})
        child_data.update({'premium_amount': child_policy.premium_amount})
        child_data.update({'date_registered': child_policy.date_registered})

        # get_benefits
        benefits = []
        if child_policy.benefits:
            for i in child_policy.benefits:
                b_name = self.get_benefit_name(i.ic_benefit)
                data = {
                    "name": b_name,
                    "amount": i.amount
                }
                benefits.append(data)
            child_data.update({"benefits": benefits})

        # get_extensions
        extensions = []
        if child_policy.extensions:
            for i in child_policy.extensions:
                e_name = self.get_extension_name(i.ic_extension)
                data = {
                    "name": e_name,
                    "amount": i.amount
                }
                extensions.append(data)
            child_data.update({"extensions": extensions})
        # get vehicle data
        vehicle_data = self.get_vehicle_data(child_policy.vehicle)
        child_data.update({"vehicle_data": vehicle_data})
        return child_data

    def get_benefit_name(self, ic_benefit_id):
        # fetch the benefit given the ic_benefit ID
        ic_benefit = ICBenefits.get_ic_benefit(ic_benefit_id)
        benefit_id = ic_benefit.benefit
        # get the benefit name
        benefit_name = Benefit.get_name_by_id(benefit_id)
        return benefit_name

    def get_extension_name(self, ic_extension_id):
        # fetch the IC extension name
        ic_extension = ICExtensions.get_extension_id(ic_extension_id)
        extension_id = ic_extension.extension
        extension_name = Extension.get_name_by_id(extension_id)
        return extension_name

    def get_vehicle_data(self, vehicle_id):
        """
        Get the vehicle details plus the driver and any modifications made
        """
        all_data = {}
        # get vehicle details
        vehicle = VehicleDetails.get_details(vehicle_id)
        if vehicle:
            vehicle_details = {
                "reg_no": vehicle.reg_number,
                "color": vehicle.color,
                "body_type": vehicle.body_type,
                "origin": vehicle.origin,
                "sum_insured": vehicle.sum_insured,
                "no_of_seats": vehicle.no_of_seats,
                "manufacture_year": vehicle.manufacture_year,
                "engine_capacity": vehicle.engine_capacity
            }

        # get model details
        model = CarModel.get_model_name_by_id(vehicle.model)
        vehicle_details.update({"model": model})

        # get driver details
        driver = Driver.get_driver_by_id(vehicle.driver)
        driver_data = {
            "first_name": driver.first_name,
            "last_name": driver.last_name,
            "gender": driver.gender,
            "phone": driver.phone,
            "birthdate": driver.birth_date,
        }
        # get modifications
        modifications = []
        if vehicle.modifications:
            for i in vehicle.modifications:
                data = {
                    "accessory_name": i.accessory_name,
                    "make": i.make,
                    "estimated_value": i.estimated_value,
                    "serial_no": i.serial_no
                }
                modifications.append(data)

        # combine all data
        all_data.update({"vehicle_details": vehicle_details})
        all_data.update({"driver_detail": driver_data})
        all_data.update({"modifications": modifications})

        # return all data
        return all_data

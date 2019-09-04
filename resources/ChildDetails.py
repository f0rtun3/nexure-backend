"""
Resource for fetching child details
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


class ChildDetails(Resource):
    """
    Contains get request for fetching child details using child id
    """
    # @jwt_required
    def get(self, child_id):
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
        response = helper.make_rest_success_response(
            "Success.", child_data)
        return make_response(response, 200)

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

"""
Resource for fetching customer details
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
from models.ICBenefits import ICBenefits
from models.ICExtensions import ICExtensions
from models.PolicyBenefits import PolicyBenefits
from models.Benefits import Benefit
from models.Extensions import Extension
from models.CompanyDetails import CompanyDetails
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


class MasterDetails(Resource):
    """
    Returns master policy details with the child's details
    """
    @jwt_required
    def get(self, master_id):
        """
        Uses the master policy number to get the policy details
        """
        master = MasterPolicy.get_policy_by_id(master_id)
        child_policies = []
        for i in master.child_policy:
            # Use child policy id
            child_id = i.id
            child_data = ChildPolicy.get_child_by_id(child_id)
            comp = CompanyDetails.get_company_by_id(child_data.company)
            data = {
                "id": child_data.id,
                "policy_name": child_data.subclass,
                "child_no": child_data.cp_number,
                "company": comp.company_name,
                "date_activated": child_data.date_activated,
                "premium_paid": child_data.premium_amount
            }
            child_policies.append(data)

        response = helper.make_rest_success_response(
            "Success.", child_policies)
        return make_response(response, 200)

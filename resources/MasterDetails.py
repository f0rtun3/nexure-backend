"""
Resource for fetching customer details
"""
from flask import make_response
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
from helpers import helpers as helper
from helpers.parsers import underwriting_parser
from helpers.CustomerNumber import CustomerNumber
from helpers.PolicyNumber import PolicyNoGenerator
import helpers.tokens as token_handler
import uuid
import json
from Controllers.master_policy import MasterController


class MasterDetails(Resource):
    """
    Returns master policy details with the child's details
    """
    @jwt_required
    def get(self, master_id):
        """
        get the master policy and associated child policies
        :return:
        """
        result = MasterController.fetch_master_policy(master_id)
        if result:
            return make_response(helper.make_rest_success_response("Successfully fetched",
                                                                   result), 200)

        return make_response(helper.make_rest_fail_response("Policy was not found"), 404)

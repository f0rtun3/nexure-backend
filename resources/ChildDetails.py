"""
Resource for fetching child details
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
from Controllers.child_policy import ChildController


class ChildDetails(Resource):
    @jwt_required
    def get(self, child_id):
        """
        Process request to get all unselected benefits and extensions
        of a policy holder, and the rest of the policy details
        :param policy_id:
        :return:
        """
        child = ChildPolicy.get_child_by_id(child_id).serialize()
        result = ChildController.get_unselected_benefits_extensions(child_id)
        if child:
            if result:
                child.update({"unselected_benefits": result})

            return make_response(helper.make_rest_success_response("Success",
                                                                   child), 200)

        else:
            return make_response(helper.make_rest_fail_response("Policy does not exist"), 404)

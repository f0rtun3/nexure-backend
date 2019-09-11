"""
policy handler resources
"""

from flask import make_response, jsonify
from flask_restful import Resource
import helpers.helpers as helper
import services.master_policy_service as mp_service


class PolicyHandler(Resource):
    """
    handles the master policy rest requests
    """
    def get(self, policy_id):
        """
        get the master policy and associated child policies
        :param policy_id:
        :return:
        """
        result = mp_service.get_single_policy_details(policy_id)
        if result:
            return make_response(helper.make_rest_success_response("Successfully fetched",
                                                                   result), 200)

        return make_response(helper.make_rest_fail_response("Policy was not found"), 404)


class BenefitsHandler(Resource):
    """
    Policy holder benefits handler.
    Handles all associated tasks relating to policy benefits
    """
    def get(self, policy_id):
        """
        Process request to get all unselected benefits and extensions
        of a policy holder
        :param policy_id:
        :return:
        """
        result = mp_service.get_unselected_benefits_extensions(policy_id)
        if result:
            return make_response(helper.make_rest_success_response("Success",
                                                                   result), 200)

        return make_response(helper.make_rest_fail_response("Failed to fetch unselected"
                                                            "benefits and extensions"), 404)

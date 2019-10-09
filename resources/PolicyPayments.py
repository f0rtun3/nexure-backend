"""
Resource for policy payments
"""
from flask import make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims

class PolicyPayments(Resource):
    """
    Handles all the payments made for one child policy
    """

    @jwt_required
    def post(self):
        """
        Request made for when an agency receives payment from a customer
        """
        pass

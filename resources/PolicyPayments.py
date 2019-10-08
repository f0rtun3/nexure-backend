"""
Resource for policy payments
"""
from flask import make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.PolicyPayments import PolicyPayments

class PolicyPayments(Resource):
    """
    Handles all the payments made by a customer for one child policy
    """

    @jwt_required
    def post(self):
        """
        Request made for when a customer makes a payment
        """

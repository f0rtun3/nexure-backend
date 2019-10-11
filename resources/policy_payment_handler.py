from models.PolicyPayments import PolicyPayments
from flask_restful import Resource
from flask import make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from helpers import helpers as helper
from helpers.parsers import payments_parser


class PolicyPaymentsResource(Resource):
    @jwt_required
    def post(self):
        """
        make a new policy payment to the database
        """
        payment_details = payments_parser.parse_args()
        new_installment = PolicyPayments(payment_details['transaction_type'],
                                         payment_details['amount'],
                                         payment_details['customer_no'],
                                         payment_details['child_policy_id'],
                                         payment_details['next_date'],
                                         payment_details['amount_due'],
                                         payment_details['transaction_code'])
        if new_installment.add():
            response_message = "Successfully made new installment"
            return make_response(helper.make_rest_success_response(response_message), 200)

        response_message = "Failed to make new payment installmnet"
        return make_response(helper.make_rest_fail_response(response_message), 500)


class PolicyPaymentsHandler(Resource):
    @jwt_required
    def get(self, child_policy_id):
        """
        get the transaction history of a particular policy
        :return:
        """
        transaction_history = PolicyPayments.get_payments_history(child_policy_id)
        if transaction_history:
            response_message = "Success"
            return make_response(helper.make_rest_success_response(response_message, transaction_history), 200)

        response_message = "No data was found"
        return make_response(helper.make_rest_success_response(response_message),404)

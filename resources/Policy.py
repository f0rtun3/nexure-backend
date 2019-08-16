from flask import make_response
from flask_restful import Resource
# from flask_jwt_extended import jwt_required
import helpers.helpers as helper


class PolicyHandler(Resource):
    def post(self):
        # enrol customer to a policy

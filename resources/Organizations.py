from flask import make_response
from flask_restful import Resource
# from flask_jwt_extended import jwt_required
import helpers.helpers as helper
from models.OrganizationTypes import OrganizationTypes


class OrganizationHandler(Resource):
    # @jwt_required
    def get(self):
        """
        get all the organization types for organization customer onboard
        :return:
        """
        org_types = OrganizationTypes.get_organization_customer_types()
        msg = "Request was successful"
        response = helper.make_rest_success_response(msg, {"organizations": org_types})
        return make_response(response, 200)

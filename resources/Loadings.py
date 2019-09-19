from flask import make_response
from flask_restful import Resource
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.InsuranceCompany import InsuranceCompany
from models.Loadings import Loadings
from models.ICLoadings import ICLoadings

from helpers.parsers import policy_parser
from helpers import helpers as helper


class LoadingsHandler(Resource):
    """
    Add policy enrolment loadings related to a particular company
    """
    @jwt_required
    def post(self):
        details = policy_parser.parse_args()
        # get the current agency details
        uid = get_jwt_identity()
        # use the uid to get company through the company contact_id
        company = InsuranceCompany.get_company_by_contact_person(uid)

        """
        First add the loading to the loadingss table, regardless of insurance company
        """
        existing_loadings = Loadings.get_all_loadings()
        loading_name = details['name']

        # check whether the benefits to be added already exist
        if loading_name not in existing_loadings:
            new_loading = Loadings(loading_name)
            new_loading.save()

        """
        Store loadings offered by a particular company together with limit
        """
        # get the extension_id
        loading_id = Loadings.get_loading_id_by_name(loading_name)

        company_loading = ICLoadings(company.id, loading_id, details['rate'])
        company_loading.save()

        """
        Send success response
        """
        response_msg = helper.make_rest_success_response(
            "Loading added successfully")
        return make_response(response_msg, 200)

    def put(self):
        """Update loading, change rate etc."""
        pass

    def get(self):
        """
        Get all loadings
        """
        loadings = Loadings.get_all_loadings()
        if loadings:
            response_msg = helper.make_rest_success_response(
                "Loadings", loadings)
            return make_response(response_msg, 200)

        return make_response(helper.make_rest_fail_response(
            "No data was found"), 404)

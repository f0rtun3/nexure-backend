from flask import make_response
from flask_restful import Resource
from app import app
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.InsuranceCompany import InsuranceCompany
from models.Loadings import Loadings
from models.ICLoadings import ICLoadings

from helpers.parsers import policy_parser
import helpers.helpers as helper


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
        loading_id = Loadings.get_extension_id_by_name(loading_name)

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

    @jwt_required
    def get(self, company_id):
        """Get list of loadings associated with a particular company"""
        loadings_list = {}

        loadings = ICLoadings.get_loadings_by_company_id(company_id)

        if loadings:
            for i in loadings:
                # first get the extension name since ICExtension model only returns the benefit id
                loading_name = Loadings.get_name_by_id(i.loading_id)
                data = {
                    "id": i.id,
                    "loading_name": loading_name,
                    "rate": i.rate
                }
                loadings_list.update(data)

            message = "Request successful"
            response = helper.make_rest_success_response(
                message, loadings_list)
            return make_response(response, 200)

        else:
            message = "No data was found"
            response = helper.make_rest_fail_response(message)
            return make_response(response, 404)

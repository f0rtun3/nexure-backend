from flask import make_response
from flask_restful import Resource
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.InsuranceCompany import InsuranceCompany
from models.Extensions import Extension
from models.ICExtensions import ICExtensions

from helpers.parsers import policy_parser
from helpers import helpers as helper


class ExtensionHandler(Resource):
    """
    Add policy enrolment extensions related to a particular company
    """
    @jwt_required
    def post(self):
        details = policy_parser.parse_args()
        # get the current agency details
        uid = get_jwt_identity()
        # use the uid to get company through the company contact_id
        company = InsuranceCompany.get_company_by_contact_person(uid)

        """
        First add the extension to the extensions table, regardless of insurance company
        """
        exisiting_extensions = Extension.get_all_extensions()
        extension_name = details['name']

        # check whether the benefits to be added already exist
        if extension_name not in exisiting_extensions:
            new_extension = Extension(extension_name)
            new_extension.save()

        """
        Store benefits offered by a particular company together with limit
        """
        # get the extension_id
        extension_id = Extension.get_extension_id_by_name(extension_name)

        company_extension = ICExtensions(
            company.id, extension_id, details['free_limit'], details['max_limit'], details['rate'])
        company_extension.save()

        """
        Send success response
        """
        response_msg = helper.make_rest_success_response(
            "Extension added successfully")
        return make_response(response_msg, 200)

    def put(self):
        # ToDo:Update benefit, change the free limit, or max limit, change rate etc.
        pass

    def get(self):
        """
        Get all extensions
        """
        extensions = Extension.get_all_extensions()
        if extensions:
            response = helper.make_rest_success_response(
                "Extensions", extensions)
            return make_response(response, 200)

        return make_response(helper.make_rest_fail_response(
            "No data was found"), 404)

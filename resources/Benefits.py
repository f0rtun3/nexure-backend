from models.ICExtensions import ICExtensions
from models.Extensions import Extension
from flask import make_response
from flask_restful import Resource
from app import app
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.InsuranceSubclass import InsuranceSubclass
from models.InsuranceCompany import InsuranceCompany
from models.Benefits import Benefit
from models.ICBenefits import ICBenefits

from helpers.parsers import policy_parser
import helpers.helpers as helper
from flask import make_response


class BenefitHandler(Resource):
    """
    Add policy enrolment benefits related to a particular company
    """
    @jwt_required
    def post(self):
        # benefits handler
        details = policy_parser.parse_args()
        # get the current agency details
        uid = get_jwt_identity()
        # use the uid to get company through the company contact_id
        company = InsuranceCompany.get_company_by_contact_person(uid)

        """
        First add the benefit to the benefits table, regardless of insurance company
        """
        exisiting_benefits = Benefit.get_all_benefits()
        benefit_name = details['name']

        # check whether the benefits to be added already exist
        if benefit_name not in exisiting_benefits:
            new_benefit = Benefit(benefit_name)
            new_benefit.save()

        """
        Store benefits offered by a particular company together with limit
        """
        # get the benefit_id
        benefit_id = Benefit.get_benefit_by_name(benefit_name)

        company_benefit = ICBenefits(
            company.id, benefit_id, details['free_limit'], details['max_limit'], details['rate'])
        company_benefit.save()

        """
        Send success response
        """
        response_msg = helper.make_rest_success_response(
            "Benefit added successfully")
        return make_response(response_msg, 200)

    def put(self):
        """Update benefit, change the free limit, or max limit, change rate etc."""
        pass
    
    def get(self):
        """
        Get all benefits
        """
        benefits_list = []
        benefits = Benefit.get_all_benefits()
        if benefits:
            for i in benefits:
                data = {
                    "id": i.id,
                    "name": i.name
                }
                benefits_list.append(data)

        response_msg = helper.make_rest_success_response(
            "Benefits", benefits_list)
        return make_response(response_msg, 200)

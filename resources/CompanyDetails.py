"""
Resource for fetching all company details, including it's benefits, extensions, loadings and levies, given the ID.
"""
from app import app, db
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.Loadings import Loadings
from models.ICLoadings import ICLoadings
from models.Benefits import Benefit
from models.Levies import Levies
from models.Extensions import Extension
from models.ICExtensions import ICExtensions
from models.ICBenefits import ICBenefits
from models.InsuranceCompany import InsuranceCompany
from models.UserRolePlacement import UserRolePlacement
import helpers.helpers as helper
import helpers.tokens as token_handler
import uuid


class CompanyDetails(Resource):
    def get(self, company_id):
        company_data = {}
        # get the company benefits
        benefits = ICBenefits.get_benefits_by_company_id(company_id)
        benefits_list = []
        if benefits:
            for i in benefits:
                # first get the benefit name since ICBenefits model only returns the benefit id
                benefit_name = Benefit.get_name_by_id(i.benefit_id)
                data = {
                    "id": i.id,
                    "name": benefit_name,
                    "free_limit": i.free_limit,
                    "max_limit": i.max_limit,
                    "rate": i.rate
                }
                benefits_list.append(data)
        # append benefits data to the company details list
        company_data.update({"benefits": benefits_list})

        # get the company loadings
        loadings_list = []
        loadings = ICLoadings.get_loadings_by_company_id(company_id)
        if loadings:
            for i in loadings:
                # first get the extension name since ICExtension model only returns the benefit id
                loading_name = Loadings.get_name_by_id(i.loading_id)
                data = {
                    "id": i.id,
                    "name": loading_name,
                    "rate": i.rate
                }
                loadings_list.append(data)
            # append loadings data to the company details list
            company_data.update({"loadings": loadings_list})

        # get the company extensions
        extensions_list = []
        extensions = ICExtensions.get_extensions_by_company_id(company_id)
        if extensions:
            for i in extensions:
                # first get the extension name since ICExtension model only returns the benefit id
                extension_name = Extension.get_name_by_id(i.benefit_id)
                data = {
                    "id": i.id,
                    "name": extension_name,
                    "free_limit": i.free_limit,
                    "max_limit": i.max_limit,
                    "rate": i.rate
                }
                extensions_list.update(data)

            company_data.append({"extensions": extensions_list})

        # get the levies
        levies = Levies.get_all_levies()
        levies_list = []
        for i in levies:
            data = {
                "id": i.id,
                "name": i.name,
                "rate": i.rate
            }
            levies_list.append(data)

        company_data.update({"levies": levies_list})
        company_data.update({"company_id": company_id})

        # return results
        response_msg = helper.make_rest_success_response(
            "Success", {"data": company_data})
        return make_response(response_msg, 200)

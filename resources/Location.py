from flask import make_response
from flask_restful import Resource
from models.Constituency import Constituency
from models.County import County
from models.Ward import Ward
from helpers import helpers as helper


class Location(Resource):
    def get(self):
        counties = County.get_all_counties()
        constituencies = Constituency.get_all_constituencies()
        wards = Ward.get_all_wards()
        response = {
            "counties": counties,
            "constituencies": constituencies,
            "wards": wards
        }
        response = helper.make_rest_success_response("Success", response)
        return make_response(response, 200)

from flask import make_response
from flask_restful import Resource
from models.Constituency import Constituency
from models.County import County
from models.Ward import Ward
from helpers import helpers as helper


class Location(Resource):
    def get(self):

        counties = County.get_all_counties()
        if counties:
            response = helper.make_rest_success_response("Success", counties)
            return make_response(response, 200)

        return make_response(helper.make_rest_fail_response(
                            "No data was found"), 404)

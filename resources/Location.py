from flask import make_response
from flask_restful import Resource
from models.Constituency import Constituency
from models.County import County
from models.Ward import Ward
from helpers import helpers as helper


class Location(Resource):
    def get(self):
        all_data = []
        # get all counties
        counties = County.get_all_counties()
        # get details for every county
        for i in counties:

            # get constituencies data
            constituencies_list = []
            constituencies = i.constituency
            for x in constituencies:
                name = x.name
                wards = [{"id": ward.id, "name": ward.name} for ward in x.ward]

                # constituency data
                c_data = {
                    "name": name,
                    "wards": wards
                }
                constituencies_list.append(c_data)
            # append county data now including all the constituencies and their respective wards
            data = {
                "name": i.county_name,
                "constituencies": constituencies_list
            }
            all_data.append(data)
        response = helper.make_rest_success_response("Success", all_data)
        return make_response(response, 200)
        

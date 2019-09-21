from flask import make_response
from flask_restful import Resource
from models.CarMake import CarMake
from models.CarModel import CarModel
from helpers import helpers as helper


class CarHandler(Resource):
    def get(self):
        """
        Get all cars classified under a particular car make
        """
        # get car makes
        cars = CarMake.get_all_car_makes()
        if cars:
            response = helper.make_rest_success_response(
                "Success", {"cars": cars})
            return make_response(response, 200)

        return make_response(helper.make_rest_fail_response(
            "No data was found"), 404)

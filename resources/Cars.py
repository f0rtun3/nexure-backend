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
        all_data = []
        for i in cars:
            # get all cars under each car make
            data = {}
            data.update({"make_id": i.make_id})
            data.update({"make_name": i.make_name})
            models = self.get_car_by_model(i.make_id, i.make_name)
            data.update({"models": models})

            all_data.append(data)

        response = helper.make_rest_success_response(
            "Success", {"cars": all_data})
        return make_response(response, 200)

    @staticmethod
    def get_car_by_model(make_id, make_name):
        models = []
        car_models = CarModel.get_models_by_make_id(make_id)
        for i in car_models:
            data = {}
            data.update({"model_id": i.model_id})
            data.update({"model_name": make_name + " " + i.model_name})
            data.update({"series": i.series})

            models.append(data)
        return models

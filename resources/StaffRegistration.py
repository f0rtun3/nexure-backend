from app import app
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.User import User
from models.UserProfile import UserProfile
from models.IndependentAgent import IndependentAgent
from models.TiedAgent import TiedAgents
from models.Broker import Broker
from models.BRStaff import BRStaff
from models.TAStaff import TAStaff
from models.IAStaff import IAStaff
from models.Role import Role

import helpers.helpers as helper
from helpers.parsers import customer_parser
from helpers.CustomerNumber import CustomerNumber
import helpers.tokens as token_handler

class StaffRegistration(Resource):
    """A broker, tied agent or independent agent can add a staff to their team.
         They can then grant them permissions depending on the kind of tasks assigned to the staff"""
    @jwt_required
    def post(self):
        # create a new user with the staff email
        pass

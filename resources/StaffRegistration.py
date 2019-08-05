from app import app, db
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from models.User import User
from models.UserProfile import UserProfile
from models.UserPermissions import UserPermissions
from models.IndependentAgent import IndependentAgent
from models.TiedAgent import TiedAgents
from models.Broker import Broker
from models.BRStaff import BRStaff
from models.TAStaff import TAStaff
from models.IAStaff import IAStaff
from models.Role import Role
from models.UserRolePlacement import UserRolePlacement
import helpers.helpers as helper
from helpers.parsers import customer_parser
from helpers.CustomerNumber import CustomerNumber
from helpers.parsers import user_parser
import helpers.tokens as token_handler
import uuid


class StaffRegistration(Resource):
    """A broker, tied agent or independent agent can add a staff to their team.
         They can then grant them permissions depending on the kind of tasks assigned to the staff"""
    @jwt_required
    def post(self):
        # get the staff details from the request sent by the client
        user_details = user_parser.parse_args()
        # check if the staff exists before registering them
        user_db_row = User.get_user_by_email(user_details['email'])
        if user_db_row:
            err_msg = f"{user_details['first_name']} {user_details['last_name']} already exists"
            response_msg = helper.make_rest_fail_response(err_msg)
            return make_response(response_msg, 409)

        # create user account
        user_uuid = uuid.uuid4()
        new_user = User(
            user_uuid, user_details['email'], "password")
        new_user.save()

        # create user profile
        new_user_profile = UserProfile(
            new_user.id,
            user_details['first_name'],
            user_details['last_name'],
            user_details['mob']
        )
        new_user_profile.save()

        # get organization details from JWT, such as the role of the client enrolling the staff, and their UID
        uid = get_jwt_identity()

        # get user role
        claims = get_jwt_claims()
        role = claims['role']

        # get agency_id
        agency_id = self.get_agency_id(role, uid)

        # Add staff to the appropriate table: i.e BRStaff, TRStaff, IAStaff
        # We also assign the staff roles at this stage,
        # depending on the entities they operate under, i.e BRSTF, IASTF, TASTF
        self.add_staff(role, agency_id, new_user.id)

        # store staff permissions
        self.set_permissions(user_details['permissions'], new_user.id)

        # send email to with the activation details for the staff
        response = helper.make_rest_success_response(
            "Registration successful. Please check the staff email to activate your account.")
            
        return make_response(response, 200)

    @staticmethod
    def get_agency_id(role, uid):
        """
        Fetch the agent id depending the active user's role. Could be an independent agency, brokerage or tied agent
        """
        if role == "BR":
            # get brokerage by contact person
            broker = Broker.get_broker_by_contact_id(uid)
            return broker.broker_id
        elif role == "TA":
            # get tied agency
            tied_agent = TiedAgents.get_tied_agent_by_user_id(uid)
            return tied_agent.id

        elif role == "IA":
            # get Independent agency by contact person
            ind_agent = IndependentAgent.get_agency_by_contact_person(uid)
            return ind_agent.id

    @staticmethod
    def add_staff(role, agency_id, staff_id):
        if role == "BR":
            new_broker_staff = BRStaff(staff_id, agency_id)
            new_broker_staff.save()
            # Assign staff role
            staff_role = "BRSTF"
            new_user_role = UserRolePlacement(
                staff_id,
                Role.fetch_role_by_name(staff_role))

        elif role == "TA":
            new_ta_staff = TAStaff(staff_id, agency_id)
            new_ta_staff.save()
            # assign staff role
            staff_role = "TASTF"
            new_user_role = UserRolePlacement(
                staff_id,
                Role.fetch_role_by_name(staff_role))

        elif role == "IA":
            new_ia_staff = IAStaff(staff_id, agency_id)
            new_ia_staff.save()

            # assign staff role
            staff_role = "IASTF"
            new_user_role = UserRolePlacement(
                staff_id,
                Role.fetch_role_by_name(staff_role))

    @staticmethod
    def set_permissions(permissions, user_id):
        # Split the permissions string and store in an array
        permissions = [int(i) for i in list(permissions)]
        # map the permissions to the user id and store them in UserPermissions table
        for i in permissions:
            user_permissions = UserPermissions(user_id, i)
            user_permissions.save()

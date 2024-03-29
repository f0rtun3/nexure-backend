from flask import current_app as application
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
from helpers import helpers as helper
from helpers.parsers import customer_parser
from helpers.CustomerNumber import CustomerNumber
from helpers.parsers import user_parser
import helpers.tokens as token_handler
import Controllers.staff as staff_handler
from Controllers import user_update
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
        # Create temporary seven digit password
        temporary_pass = helper.create_user_password()
        new_user = User(
            user_uuid, user_details['email'], temporary_pass)
        new_user.save()

        # create user profile
        new_user_profile = UserProfile(
            new_user.id,
            user_details['first_name'],
            user_details['last_name'],
            user_details['phone']
        )
        new_user_profile.save()

        # get organization details from JWT, such as the role of the client enrolling the staff, and their UID
        uid = get_jwt_identity()

        # get user role
        claims = get_jwt_claims()
        role = claims['role']

        # role = 'BR'

        # get agency_id
        agency_id = staff_handler.get_agency_id(role, uid)

        # Add staff to the appropriate table: i.e BRStaff, TRStaff, IAStaff
        # We also assign the staff roles at this stage,
        # depending on the entities they operate under, i.e BRSTF, IASTF, TASTF
        self.add_staff(role, agency_id, new_user.id)

        # store staff permissions
        self.set_permissions(user_details['permissions'], new_user.id)

        # send email to with the activation details for the staff
        # Temporary password email
        email_template = helper.generate_temporary_password_template(application.config['LOGIN_ENDPOINT'],
                                                               temporary_pass)
        subject = "Nexure Temporary Password"
        email_text = f"Follow {application.config['LOGIN_ENDPOINT']} to login and use {temporary_pass} as your temporary password"
        helper.send_email(user_details['email'],
                          subject, email_template, email_text)

        #  Generate a user account activation email
        confirmation_code = token_handler.user_account_confirmation_token(
            new_user.id)
        email_template = helper.generate_confirmation_template(application.config['CONFIRMATION_ENDPOINT'],
                                                               confirmation_code)
        subject = "Please confirm your account"
        email_text = f"Use this link {application.config['CONFIRMATION_ENDPOINT']}/{confirmation_code}" \
                     f" to confirm your account"
        helper.send_email(
            user_details['email'], subject, email_template, email_text)
        response = helper.make_rest_success_response(
            "Registration successful. Please check the staff email to activate your account.")
        return make_response(response, 200)

    @jwt_required
    def put(self):
        """
        update staff details
        may be user permissions or to block staff member account
        """
        staff_details = user_parser.parse_args()
        staff = User.get_user_by_email(staff_details['email'])

        if staff_details['email'] and not staff:
            response_msg = helper.make_rest_fail_response(
                "User does not exist")
            return make_response(response_msg, 404)

        if staff_details['permissions']:
            if user_update.update_staff_permissions(staff.id, staff_details['permissions']):
                response_msg = helper.make_rest_success_response(
                    "Update successful!")
                return make_response(response_msg, 200)
            else:
                response_msg = helper.make_rest_success_response(
                    "Failed to update staff permissions")
                return make_response(response_msg, 500)

        if type(staff_details['is_active']) == bool:
            # de/activate staff account
            claims = get_jwt_claims()
            role = claims['role']
            if staff_handler.update_account_status(role, staff_details['staff_id'], staff_details['is_active']):
                return make_response(helper.make_rest_success_response("Update successful"), 200)
            else:
                return make_response(helper.make_rest_fail_response(staff_details['is_active']), 500)
            


    @jwt_required
    def get(self):
        # get list of staff associated with a particular agency
        # first get agent_id
        uid = get_jwt_identity()

        # get user role so that you can use it to get the agency_id
        claims = get_jwt_claims()
        role = claims['role']
        # get company_id
        company_id = staff_handler.get_agency_id(role, uid)
        # get list of staff associated with company
        company_staff = self.get_agency_staff(role, company_id)

        response = helper.make_rest_success_response(
            "Success", {"staff_list": company_staff})
        return make_response(response, 200)

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
            new_user_role.save()

        elif role == "TA":
            new_ta_staff = TAStaff(staff_id, agency_id)
            new_ta_staff.save()
            # assign staff role
            staff_role = "TASTF"
            new_user_role = UserRolePlacement(
                staff_id,
                Role.fetch_role_by_name(staff_role))
            new_user_role.save()

        elif role == "IA":
            new_ia_staff = IAStaff(staff_id, agency_id)
            new_ia_staff.save()

            # assign staff role
            staff_role = "IASTF"
            new_user_role = UserRolePlacement(
                staff_id,
                Role.fetch_role_by_name(staff_role))
            new_user_role.save()

    @staticmethod
    def set_permissions(permissions, user_id):
        # Split the permissions string and store in an array
        permissions = [int(i) for i in list(permissions)]
        # map the permissions to the user id and store them in UserPermissions table
        for i in permissions:
            user_permissions = UserPermissions(user_id, i)
            user_permissions.save()

    def get_agency_staff(self, role, agency_id):
        # get list depending on role i.e either BRSTF, TASTF, IASTF
        if role == "BR":
            return BRStaff.fetch_staff_by_agency_id(agency_id)

        elif role == "TA":
            return TAStaff.fetch_staff_by_agency_id(agency_id)

        elif role == "IA":
            return IAStaff.fetch_staff_by_agency_id(agency_id)
    
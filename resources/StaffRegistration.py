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
            user_details['mob']
        )
        new_user_profile.save()

        # get organization details from JWT, such as the role of the client enrolling the staff, and their UID
        uid = get_jwt_identity()

        # get user role
        claims = get_jwt_claims()
        role = claims['role']

        # role = 'BR'

        # get agency_id
        agency_id = self.get_agency_id(role, uid)

        # Add staff to the appropriate table: i.e BRStaff, TRStaff, IAStaff
        # We also assign the staff roles at this stage,
        # depending on the entities they operate under, i.e BRSTF, IASTF, TASTF
        self.add_staff(role, agency_id, new_user.id)

        # store staff permissions
        self.set_permissions(user_details['permissions'], new_user.id)

        # send email to with the activation details for the staff
        # Temporary password email
        email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
                                                               temporary_pass)
        subject = "Nexure Temporary Password"
        helper.send_email(user_details['email'], subject, email_template)

        #  Generate a user account activation email
        confirmation_code = token_handler.user_account_confirmation_token(
            new_user.id)
        email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
                                                               confirmation_code)
        subject = "Please confirm your account"
        helper.send_email(
            user_details['email'], subject, email_template)
        response = helper.make_rest_success_response(
            "Registration successful. Please check the staff email to activate your account.")
        return make_response(response, 200)

    @jwt_required
    def put(self):
        """Update staff details, mostly permissions."""
        staff_details = user_parser.parse_args()
        # check if staff exists
        staff = User.get_user_by_email(staff_details['email'])
        staff_id = staff.id

        if staff:
            if staff_details['permissions']:
                # get current permissions
                current_permissions = list(UserPermissions.get_permission_by_user_id(
                    staff_id))
                received_permissions = list(staff_details['permissions'])
                # get permissions to update
                new_permissions = [
                    x for x in received_permissions if x not in current_permissions]
                old_permissions = [
                    x for x in current_permissions if x not in received_permissions]
                # delete old permissions and update with new ones
                for i in old_permissions:
                    permissions = UserPermissions.get_specific_permission(
                        i, staff_id)
                    permissions.delete()
                # update with new ones
                for i in new_permissions:
                    user_permissions = UserPermissions(staff_id, i)
                    user_permissions.save()

            # update other details
            # get user profile
            profile = UserProfile.get_profile_by_user_id(staff_id)
            data = {
                "first_name": staff_details['first_name'],
                "last_name": staff_details['last_name'],
                "phone": staff_details['mob']
            }
            if data:
                profile.update(data)
            # if update is successful

            if staff_details['password']:
                # set new password
                new_password = staff.generate_password_hash(
                    staff_details['password'])
                staff.update_password(new_password)

            response_msg = helper.make_rest_success_response(
                f"Update successful.")
            return make_response(response_msg, 200)
        else:
            # if staff does not exist
            response_msg = helper.make_rest_fail_response(
                "User does not exist")
            return make_response(response_msg, 404)

    @jwt_required
    def get(self):
        # get list of staff associated with a particular agency
        # first get agent_id
        uid = get_jwt_identity()

        # get user role so that you can use it to get the agency_id
        claims = get_jwt_claims()
        role = claims['role']
        # role = 'BR'
        # get company_id
        company_id = self.get_agency_id(role, uid)
        # get list of staff associated with company
        company_staff = self.get_agency_staff(role, company_id)

        response = helper.make_rest_success_response(
            "Success", {"staff_list": company_staff})
        return make_response(response, 200)

    @jwt_required
    def delete(self):
        staff_details = user_parser.parse_args()
        # remove staff from agency
        # deactivate the staff's affiliation
        # get agent id and role so as to fetch the staff's affiliation
        uid = get_jwt_identity()

        # get user role so that you can use it to get the agency_id
        claims = get_jwt_claims()
        role = claims['role']
        # role = 'BR'
        # get company_id
        company_id = self.get_agency_id(role, uid)

        # deactivate staff instead of deleting
        if role == "BR":
            BRStaff.deactivate_staff(company_id, staff_details['staff_id'])
        elif role == "TA":
            TAStaff.deactivate_staff(company_id, staff_details['staff_id'])
        elif role == "IA":
            IAStaff.deactivate_staff(company_id, staff_details['staff_id'])

        response = helper.make_rest_success_response(
            "Staff deleted successfully")
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
            staff_ids = BRStaff.fetch_all_staff_ids(agency_id)
            # Get all staff properties
            staff_list = []
            for i in staff_ids:
                staff = self.get_staff_details(i)
                staff_list.append(staff)
            return staff_list

        elif role == "TA":
            staff_ids = TAStaff.fetch_all_staff_ids(agency_id)
            # get all staff details
            staff_list = []
            for i in staff_ids:
                staff = self.get_staff_details(i)
                staff_list.append(staff)
            return staff_list

        elif role == "IA":
            # get staff details
            staff_ids = IAStaff.fetch_all_staff_ids(agency_id)
            # dictionary to store staff details
            staff_list = []
            for i in staff_ids:
                staff = self.get_staff_details(i)
                staff_list.append(staff)
            return staff_list

    @staticmethod
    def get_staff_details(user_id):
        # We want to fetch staff details based on their user id: first_name, last_name, phone, email, permissions
        data = {}
        user = User.get_user_by_id(user_id)
        data.update({'id': user_id})
        # get email
        data.update({'email': user.email})
        # get profile details
        user_profile = UserProfile.get_profile_by_user_id(user_id)
        data.update({'first_name': user_profile.first_name})
        data.update({"last_name": user_profile.last_name})
        data.update({"phone": user_profile.phone})
        # get permissions
        user_permissions = UserPermissions.get_permission_by_user_id(user_id)
        data.update({"permissions": user_permissions})
        # return dict containing all data for a particular staff member
        return data

"""
User resource
Handles user related actions
"""
from models import User
from models import UserProfile
from models import Roles
from models import UserRolePlacement
from flask import make_response
from flask_restful import Resource, reqparse
# get the utility file
import helpers.helpers as helper
import helpers.tokens as token_handler

import uuid

user_parser = reqparse.RequestParser()
user_parser.add_argument(
    "first_name",
    type=str
)
user_parser.add_argument(
    "last_name",
    type=str
)
user_parser.add_argument(
    "password",
    type=str
)
user_parser.add_argument(
    "mob",
    type=int
)
user_parser.add_argument(
    "email",
    type=str
)
user_parser.add_argument(
    "role",
    type=str
)


class UserRegister(Resource):
    def post(self):
        # get the user details from the request sent by the client
        user_details = user_parser.parse_args()
        # check if the user exists before registering them
        user_db_row = User.get_user_by_email(user_details['email'])
        if user_db_row:
            err_msg = f"{user_details['first_name']} {user_details['last_name']} already exists"
            response = helper.make_rest_fail_response(err_msg)
            return make_response(response, 409)

        # save the user authentication details and profile details
        # in their respective database tables
        user_id = uuid.uuid4()
        new_user_authentication = User(
            user_id,
            user_details['email'],
            user_details['password']
        )
        new_user_authentication.save()

        new_user_profile = UserProfile(
            new_user_authentication.id,
            user_details['first_name'],
            user_details['last_name'],
            user_details['mob']
        )
        new_user_profile.save()

        new_user_role = UserRolePlacement(
            new_user_authentication.id,
            Roles.fetch_role_by_name(user_details['role'])
        )
        new_user_role.save()
        """
        Account confirmation email generation
        #   we need to generate a code for user to use for confirmation code
        #   confirmation_code = token_handler.user_account_confirmation_token(new_user_authentication.id)
        #   email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
        #                                                          confirmation_code)
        #   subject = "Please confirm your account"
        #   helper.send_email(user_details['email'], subject, email_template)
        """
        #   ToDo: Configure email server and uncomment the above section
        success_msg = "You have been registered. Kindly check your email to confirm account"
        response = helper.make_rest_success_response(success_msg)

        return make_response(response, 200)

    def get(self):
        """
        get user profile details

        user_profile_row = UserProfile.get_all_profiles()
        if not user_profile_row:
            response = helper.make_rest_fail_response("No user was found")
            return make_response(response, 404)

        response = helper.make_rest_success_response(None, user_profile_row)
        return make_response(response, 200)
        """


class UserAccountConfirmation:
    pass


class UserLogin(Resource):
    def post(self):
        user_details = user_parser.parse_args()
        # check whether the user exists before confirming
        user_db_row = User.get_user_by_email(user_details['email'])

        if not user_db_row:
            response = helper.make_rest_fail_response("User email does not exist")
            return make_response(response, 404)

        # user exists, let's go ahead and authenticate the user
        # we also need to check whether the user account is verified or not
        if user_db_row.check_password_hash(user_details['password']):
            if user_db_row.is_active:
                # generate an access token for the user
                auth_tokens = token_handler.create_user_token(user_db_row.id)
                response = helper.make_rest_success_response("Successfully logged in", auth_tokens)
                return make_response(response, 200)
            else:
                response = helper.make_rest_fail_response("Please confirm your account before signing in.")
                return make_response(response, 401)
        else:
            response = helper.make_rest_fail_response("Wrong credentials passed, please try again")
            return make_response(response, 401)

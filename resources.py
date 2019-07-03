"""
User resource
Handles user related actions
"""
from models import User
from models import UserProfile, IndependentAgent, TiedAgents, Broker
from models import Roles
from models import UserRolePlacement
from models import InsuranceCompany
from models import IndividualCustomer
from flask import make_response
from flask_restful import Resource, reqparse
# get the utility file
import helpers.helpers as helper
import helpers.tokens as token_handler
#jwt token authentication library
from flask_jwt_extended import jwt_required, get_jwt_identity

# from app import app
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
user_parser.add_argument(
    "agency_name",
    type=str
)
user_parser.add_argument(
    "agency_email",
    type=str
)
user_parser.add_argument(
    "agency_phone",
    type=int
)

customer_parser = reqparse.RequestParser()
customer_parser.add_argument(
    # Individual or organization
    "type",
    type=str
)
customer_parser.add_argument(
    # If organization
    "org_type",
    type=str
)
# For individuals
customer_parser.add_argument(
    "first_name",
    type=str
)
customer_parser.add_argument(
    "last_name",
    type=str
)
customer_parser.add_argument(
    "phone",
    type=int
)
customer_parser.add_argument(
    "email",
    type=str
)
customer_parser.add_argument(
    "birth_date",
    type=str
)
customer_parser.add_argument(
    "gender",
    type=str
)
customer_parser.add_argument(
    "address_line_1",
    type=str
)
customer_parser.add_argument(
    "address_line_2",
    type=str
)
customer_parser.add_argument(
    "postal_code",
    type=str
)
customer_parser.add_argument(
    "postal_town",
    type=str
)
customer_parser.add_argument(
    "county",
    type=str
)
customer_parser.add_argument(
    "constituency",
    type=str
)
customer_parser.add_argument(
    "ward",
    type=str
)
customer_parser.add_argument(
    "id_passport",
    type=str
)
customer_parser.add_argument(
    "kra_pin",
    type=str
)
customer_parser.add_argument(
    "occupation",
    type=str
)
customer_parser.add_argument(
    "facebook",
    type=str
)
customer_parser.add_argument(
    "twitter",
    type=str
)
customer_parser.add_argument(
    "instagram",
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
        confirmation_code = token_handler.user_account_confirmation_token(new_user_authentication.id)
        # Account confirmation email generation
        #   we need to generate a code for user to use for confirmation code
        """
        email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
                                                                  confirmation_code)
        subject = "Please confirm your account"
        helper.send_email(user_details['email'], subject, email_template)
        """
        #   ToDo: Configure email server and uncomment the above section

        success_msg = "You have been registered. Kindly check your email to confirm account"
        response = helper.make_rest_success_response(success_msg, {"confirmation_token": confirmation_code})

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

    def onboard_client(self, role, user_id, user_details):
        # Use user's role to determine where the details will be stored
        if role == "IA":
            # If it's an independent agency
            new_independent_agency = IndependentAgent(
                user_details["agency_name"],
                user_details["agency_phone"],
                user_details["agency_email"],
                user_id,
                user_details["first_name"],
                user_details["last_name"],
                user_details["mob"]
            )
            new_independent_agency.save()

        elif role == "IC":
            # if it's an insurance company
            new_insurance_company = InsuranceCompany(
                user_details["company_phone"],
                user_details["company_name"],
                user_details["company_email"],
                user_id,
                user_details["contact_first_name"],
                user_details["contact_last_name"],
                user_details["contact_phone"]
            )
            new_insurance_company.save()

        elif role == "TA":
            # If it's a tied agent
            # You only need a user_id to create a Tied agent object.
            new_tied_agent = TiedAgents(user_id)
            new_tied_agent.save()

        elif role == "IN":
            # If it's an individual/direct customer
            new_individual_customer = IndividualCustomer(user_id)
            new_individual_customer.save()

        elif role == "BR":
            # if it's a broker
            new_broker = Broker(
                user_details["broker_name"],
                # Broker contact person(Foreign Key)
                user_id,
                user_details["broker_phone_number"],
                user_details["broker_email"],
                user_details["agency_name"]
            )
            new_broker.save()


class UserAccountConfirmation(Resource):
    @jwt_required
    def put(self):
        """
        authenticaiton token is sent here for confirmation
        token must be valid for account to be activated
        """
        # the user id is needed to needed to know the user whose account we are activating
        user_id =  get_jwt_identity()
        user_row = User.get_user_by_id(user_id)
        if user_row:
            if user_row.is_active:
                response = helper.make_rest_success_response("Your account is already active, please login")
                return make_response(response, 200)    
            data = {'is_active': True}
            user_row.update(data)
            response = helper.make_rest_success_response("Your account has been activated, you can now log in")
            return make_response(response, 200)

        # the user has not been found in the database
        response = helper.make_rest_fail_response("User does not exist")
        return make_response(response, 404)

    def get(self, user_id):
        """
        If the jwt token has expired
        a user can request for another token here simple by passing in the user_id
        """
        """
        user_row = User.get_user_by_id(user_id)
        if user_row:
            confirmation_code = token_handler.user_account_confirmation_token(user_id)
            email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
                                                                  confirmation_code)
            subject = "Please confirm your account"
            helper.send_email(user_row.email, subject, email_template)
            response = helper.make_rest_success_response("Please check your email to confirm your account")
            return make_response(response, 200)

        response = helper.make_rest_fail_response("User was not found, please try again or register a new account")
        return make_response(response, 404)
        """
        pass


class UserLogin(Resource):
    def post(self):
        user_details = user_parser.parse_args()
        # check whether the user exists before confirming
        user_db_row = User.get_user_by_email(user_details['email'])

        if not user_db_row:
            response = helper.make_rest_fail_response(
                "User email does not exist")
            return make_response(response, 404)

        # user exists, let's go ahead and authenticate the user
        # we also need to check whether the user account is verified or not
        if user_db_row.check_password_hash(user_details['password']):
            if user_db_row.is_active:
                # generate an access token for the user
                auth_tokens = token_handler.create_user_token(user_db_row.id)
                response = helper.make_rest_success_response(
                    "Successfully logged in", auth_tokens)
                return make_response(response, 200)
            else:
                response = helper.make_rest_fail_response(
                    "Please confirm your account before signing in.")
                return make_response(response, 401)
        else:
            response = helper.make_rest_fail_response(
                "Wrong credentials passed, please try again")
            return make_response(response, 401)


class CustomerOnboarding(Resource):
    def post(self):
        customer_details = customer_parser.parse_args()
        # check whether customer exists
        customer_row = User.get_user_by_email(customer_details['email'])
        # If customer or organization contact person already created an account
        if customer_row:
            if customer_details["type"] == "Individual":
                # Add his id to individual customers
                new_individual_cust = IndividualCustomer(customer_row.id)
                response = helper.make_rest_success_response(
                    f"The customer had been onboarded successfully using details from an existing account.
                    Kindly check profile information for account {customer_details['email']}")
                return make_response(response, 200)
            if customer_details["type"] == "Organization":
                # create a new "organization" customer account


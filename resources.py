"""
User resource
Handles user related actions
"""
from models import User
from models import UserProfile, IndependentAgent, TiedAgents, Broker
from models import Roles
from models import UserRolePlacement
from models import InsuranceCompany
from models import IndividualCustomer, OrganizationCustomer
from flask import make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
# get the utility file
import helpers.helpers as helper
import helpers.tokens as token_handler
from helpers.parsers import user_parser, customer_parser
# jwt token authentication library
from flask_jwt_extended import jwt_required, get_jwt_identity

# from app import app
import uuid
import string
import random


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
        confirmation_code = token_handler.user_account_confirmation_token(
            new_user_authentication.id)
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
        response = helper.make_rest_success_response(
            success_msg)

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

    @jwt_required
    def put(self):
        # get user id
        user_id = get_jwt_identity()
        # get the user details from the request sent by the client
        user_details = user_parser.parse_args()
        # check if the user exists
        user = User.get_user_by_id(user_id)
        # if user exists, then update their details
        if user:
            # get their role
            role = UserRolePlacement.fetch_role_by_user_id(user_id)
            # update their profile
            self.update_profile(
                user_id,
                data={
                    "gender": user_details['gender'],
                    "occupation": user_details['occupation'],
                    "id_passport": user_details['id_passport'],
                    "kra_pin": user_details['kra_pin'],
                    "birth_date": user_details['birth_date'],
                    "physical_address": user_details['physical_address'],
                    "postal_code": user_details['postal_code'],
                    "postal_town": user_details['postal_town'],
                    "county": user_details['county'],
                    "constituency": user_details['constituency'],
                    "ward": user_details['ward'],
                    "facebook": user_details['facebook'],
                    "twitter": user_details['twitter'],
                    "instagram": user_details['instagram']
                }
            )
            """
            update the client account depending on their role: 
            Note: that for tied agents, we only update their profiles
            """
            # for brokers
            if role == 'BR':
                # get broker by id
                broker = Broker.get_broker_by_contact_id(user_id)
                # update their account
                data = {
                    "broker_name": user_details['org_name'],
                    "broker_phone_number": user_details['org_phone_number'],
                    "broker_email": user_details['org_email'],
                    "ira_registration_number": user_details['ira_reg_no'],
                    "ira_license_number": user_details['ira_license_no'],
                    "kra_pin": user_details['kra_pin'],
                    "website": user_details['website'],
                    "facebook": user_details['facebook'],
                    "instagram": user_details['twitter'],
                    "twitter": user_details['instagram']
                }
                broker.update(data)
            # for insurance companies
            elif role == 'IC':
                # get insurance company
                company = InsuranceCompany.get_company_by_contact_person(
                    user_id)
                # update their account
                data = {
                    "company_name": user_details['org_name'],
                    "company_number": user_details['org_phone_number'],
                    "company_email": user_details['org_email'],
                    "bank_account": user_details['bank_account'],
                    "mpesa_paybill": user_details['mpesa_paybill'],
                    "ira_registration_number": user_details['ira_reg_no'],
                    "ira_license_number": user_details['ira_license_no'],
                    "kra_pin": user_details['kra_pin'],
                    "website": user_details['website'],
                    "facebook": user_details['facebook'],
                    "instagram": user_details['instagram'],
                    "twitter": user_details['twitter']
                }
                company.update(data)

            # for independent agents
            elif role == 'IA':
                """One contact person only represents one entity. So, we fetch the agency using the contact person's id """
                agency = IndependentAgent.get_agency_by_contact_person(user_id)
                data = {
                    "agency_name": user_details['org_name'],
                    "agency_phone": user_details['org_phone_number'],
                    "agency_email": user_details['org_email'],
                    "ira_registration_number": user_details['ira_reg_no'],
                    "ira_license_number": user_details['ira_license_no'],
                    "kra_pin": user_details['kra_pin'],
                    "website": user_details['website'],
                    "facebook": user_details['facebook'],
                    "instagram": user_details['instagram'],
                    "twitter": user_details['twitter']
                }
                agency.update(data)
        else:
            # if user does not exist
            response = helper.make_rest_fail_response(
                "User does not exist")
            return make_response(response, 404)

        # change password
        if user_details['new_password']:
            user = User.get_user_by_id(get_jwt_identity())
            password = user.generate_password_hash(user_details['new_password'])
            user.update_password(password)

        # if update is successful
        response = helper.make_rest_success_response(
            f"Update successful.")
        return make_response(response, 200)

    def update_profile(self, id, data):
        profile = UserProfile.get_profile_by_user_id(id)
        profile.update(data)

    def onboard_client(self, role, user_id, user_details):
        # Use user's role to determine where the details will be stored
        if role == "IA":
            # If it's an independent agency
            new_independent_agency = IndependentAgent(
                user_details["org_name"],
                user_details["org_phone"],
                user_details["org_email"],
                user_id
            )
            new_independent_agency.save()

        elif role == "IC":
            # if it's an insurance company
            new_insurance_company = InsuranceCompany(
                user_details["org_name"],
                user_details["org_email"],
                user_details["org_phone"],
                user_id
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
                user_details["org_name"],
                user_details["org_phone"],
                user_details["org_email"],
                user_id
            )
            new_broker.save()


class UserAccountConfirmation(Resource):
    @jwt_required
    def put(self):
        """
        authentication token is sent here for confirmation
        token must be valid for account to be activated
        """
        # the user id is needed to needed to know the user whose account we are activating
        user_id = get_jwt_identity()
        user_row = User.get_user_by_id(user_id)
        if user_row:
            if user_row.is_active:
                response = helper.make_rest_success_response(
                    "Your account is already active, please login")
                return make_response(response, 200)
            data = {'is_active': True}
            user_row.update(data)
            response = helper.make_rest_success_response(
                "Your account has been activated, you can now log in")
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
                # generate an access token for the user, and also return the user role
                # to redirect them to the correct page after logging in
                role = self.get_user_role(user_db_row.id)
                auth_tokens = token_handler.create_user_token(user_db_row.id)
                response = helper.make_rest_success_response(
                    "Successfully logged in", {"tokens": auth_tokens, "role": role})
                return make_response(response, 200)
            else:
                response = helper.make_rest_fail_response(
                    "Please confirm your account before signing in.")
                return make_response(response, 401)
        else:
            response = helper.make_rest_fail_response(
                "Wrong credentials passed, please try again")
            return make_response(response, 401)

    def get_user_role(self, user_id):
        role = UserRolePlacement.fetch_role_by_user_id(user_id)
        role_name = Roles.fetch_role_by_id(role.role_id)
        return role_name


class CustomerOnboarding(Resource):

    def post(self):
        # check whether customer exists
        customer_details = customer_parser.parse_args()
        customer_row = User.get_user_by_email(customer_details['email'])
        # If individual customer already created an account
        if customer_details["type"] == "Individual":
            if customer_row:
                # Create an individual customer
                self.create_individual_customer(customer_row.id)

                # assign role
                self.role_placement(customer_row.id, "IND")

            # if the individual cust. doesn't have an account, create a new one
            else:

                user_id = uuid.uuid4()
                # Create temporary seven digit password
                temporary_pass = self.create_user_password()
                # create new user
                new_individual_cust = User(
                    user_id,
                    customer_details['email'],
                    temporary_pass
                )
                new_individual_cust.save()

                # create individual customer's profile
                new_individual_profile = UserProfile(
                    new_individual_cust.id,
                    customer_details["first_name"],
                    customer_details["last_name"],
                    customer_details["phone"],
                    customer_details['physical_address'],
                    customer_details['postal_code'],
                    customer_details['postal_town'],
                    customer_details['county'],
                    customer_details['constituency'],
                    customer_details['ward'],
                    customer_details['facebook'],
                    customer_details['instagram'],
                    customer_details['twitter']
                )
                new_individual_profile.save()

                # assign role
                self.role_placement(new_individual_cust.id, "IND")

                # Create individual cust
                self.create_individual_customer(new_individual_cust.id)

        # Customer onboarding for organizations
        if customer_details["type"] == "Organization":
            # create a new user account using the organization email
            user_id = uuid.uuid4()
            # Create temporary seven digit password
            temporary_pass = self.create_user_password()
            # create new user
            new_account = User(
                user_id,
                customer_details['org_email'],
                temporary_pass
            )
            new_account.save()

            # assign role
            self.role_placement(new_account.id, "ORG")

            # create a new "organization" customer account
            new_org_cust = OrganizationCustomer(
                customer_details["org_name"],
                customer_details['org_phone'],
                customer_details['org_email'],
                customer_details['org_reg_number'],
                customer_details['physical_address'],
                customer_details['postal_code'],
                customer_details['postal_town'],
                customer_details['county'],
                customer_details['constituency'],
                customer_details['ward'],
                customer_details['facebook'],
                customer_details['instagram'],
                customer_details['twitter'],
                customer_details["first_name"],
                customer_details["last_name"],
                customer_details["phone"],
                customer_details["email"],
            )
            new_org_cust.save()

        # Send the user an email confirmation with their temporary password. Advice them to change it.
        response = helper.make_rest_success_response(
            f"Customer has been onboarded successfully. Please check your email for further instructions")
        return make_response(response, 200)

    def create_individual_customer(self, cust_id):
        new_individual_cust = IndividualCustomer(cust_id)
        new_individual_cust.save()

    def create_user_password(self):
        stringLength = 7
        password = string.ascii_letters + string.digits
        return ''.join(random.choice(password) for i in range(stringLength))

    def role_placement(self, id, role):
        new_user_role = UserRolePlacement(
            id,
            Roles.fetch_role_by_name(role)
        )
        new_user_role.save()

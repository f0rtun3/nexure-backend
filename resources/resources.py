"""
User resource
Handles user related actions
"""

from models.User import User
from models.UserProfile import UserProfile
from models.IndependentAgent import IndependentAgent
from models.TiedAgent import TiedAgents
from models.Broker import Broker
from models.Role import Role
from models.UserRolePlacement import UserRolePlacement
from models.InsuranceCompany import InsuranceCompany
from models.IndividualCustomer import IndividualCustomer
from models.OrganizationCustomer import OrganizationCustomer
from models.OrganizationTypes import OrganizationTypes
from models.CustomerAffiliation import CustomerAffiliation

from models import User
from models import UserProfile, IndependentAgent, TiedAgents, Broker
from models import Roles
from models import UserRolePlacement
from models import InsuranceCompany
from models import IndividualCustomer, OrganizationCustomer, OrganizationTypes
from models import CustomerAffiliation
from models import Staff
from flask import make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
# get the utility file
import helpers.helpers as helper
import helpers.tokens as token_handler
from helpers.CustomerNumber import CustomerNumber
from helpers.parsers import user_parser, customer_parser
# jwt token authentication library
from flask_jwt_extended import jwt_required, get_jwt_identity

# from app import app
import uuid


class UserRegister(Resource):
    def post(self):
        # get the user details from the request sent by the client
        user_details = user_parser.parse_args()
        # check if the user exists before registering them
        user_db_row = User.get_user_by_email(user_details['email'])
        if user_db_row:
            err_msg = f"{user_details['first_name']} {user_details['last_name']} already exists"
            response_msg = helper.make_rest_fail_response(err_msg)
            return make_response(response_msg, 409)

        # save the user authentication details and profile details
        # in their respective database tables
        user_uuid = uuid.uuid4()
        new_user_authentication = User(
            user_uuid,
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
            Role.fetch_role_by_name(user_details['role'])
        )
        new_user_role.save()

        confirmation_code = token_handler.user_account_confirmation_token(new_user_authentication.id)
        # Account confirmation email generation
        # Save extra user details depending on their role
        role = user_details["role"]
        self.onboard_client(role, new_user_authentication.id, user_details)

        """
        Send a confirmation link to the user for account confirmation
        confirmation_code = token_handler.user_account_confirmation_token(
            new_user_authentication.id)

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
                """
                One contact person only represents one entity. So, we fetch the agency using the contact person's id 
                """
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
            response_msg = helper.make_rest_fail_response(
                "User does not exist")
            return make_response(response_msg, 404)

        # change password
        if user_details['new_password']:
            user = User.get_user_by_id(get_jwt_identity())
            password = user.generate_password_hash(user_details['new_password'])
            user.update_password(password)

        # if update is successful
        response_msg = helper.make_rest_success_response(
            f"Update successful.")
        return make_response(response_msg, 200)

    def update_profile(self, id, data):
        profile = UserProfile.get_profile_by_user_id(id)
        profile.update(data)

    def onboard_client(self, role, user_id, user_details):
        # Use user's role to determine where the details will be stored
        if role == "IA":
            # If it's an independent agency
            new_independent_agency = IndependentAgent(
                user_details["agency_name"],
                user_details["agency_email"],
                user_details["agency_phone"],
                user_id
            )
            new_independent_agency.save()

        elif role == "IC":
            # if it's an insurance company
            new_insurance_company = InsuranceCompany(
                user_details["company_name"],
                user_details["company_email"],
                user_details["company_phone"],
                user_id
            )
            new_insurance_company.save()

        elif role == "TA":
            # If it's a tied agent
            # You only need a user_id to create a Tied agent object.
            new_tied_agent = TiedAgents(user_id)
            new_tied_agent.save()

        elif role == "BR":
            # if it's a broker
            new_broker = Broker(
                user_details["broker_name"],
                user_details["broker_email"],
                user_details["broker_phone_number"],
                user_id
            )
            new_broker.save()
        else:
            return


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
            response_msg = helper.make_rest_fail_response(
                "User email does not exist")
            return make_response(response_msg, 404)

        # user exists, let's go ahead and authenticate the user
        # we also need to check whether the user account is verified or not
        if user_db_row.check_password_hash(user_details['password']):
            if user_db_row.is_active:
                # generate an access and refresh token for the user, and also return the user role
                # to redirect them to the correct page after logging in
                role = self.get_user_role(user_db_row.id)
                auth_tokens = token_handler.create_user_token(user_db_row.id)
                response_msg = helper.make_rest_success_response(
                    "Successfully logged in", {"authentication": auth_tokens, "role": role})
                return make_response(response_msg, 200)
            else:
                response_msg = helper.make_rest_fail_response("Please confirm your account before signing in.")
                return make_response(response_msg, 401)
        else:
            response_msg = helper.make_rest_fail_response(
                "Wrong credentials passed, please try again")
            return make_response(response_msg, 401)

    @staticmethod
    def get_user_role(user_id):
        role = UserRolePlacement.fetch_role_by_user_id(user_id)
        role_name = Role.fetch_role_by_id(role.role_id)

        return role_name


class CustomerOnBoarding(Resource):
    """
    An agent or broker may on-board a new customer into the system
    If the customer already exists in the system, we only associate them with the affiliated broker/agent
    otherwise we add a new user create a temporary password, generate customer number for them and associate the new
    user with the affiliated agent/broker
    """

    def post(self):
        # check whether customer exists
        customer_details = customer_parser.parse_args()
        customer_row = User.get_user_by_email(customer_details['email'])
        customer_number = self.create_customer_number(customer_details['org_type'],
                                                              customer_row.id, customer_details['country'])
        customer_id = customer_row.id

        if not customer_row:
            # create a new user account if not existing
            user_id = uuid.uuid4()
            # Create temporary seven digit password
            temporary_pass = helper.create_user_password()
            # create new user
            new_account = User(
                user_id,
                customer_details['email'],
                temporary_pass
            )
            new_account.save()

            # create individual customer's profile
            new_individual_profile = UserProfile(
                new_account.id,
                customer_details["first_name"],
                customer_details["last_name"],
                customer_details["phone"]
            )
            new_individual_profile.save()
            """
            # ToDo: send the temporary password and account activation email
            email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
                                                                  temporary_pass)
            subject = "Your Nexure Temporary Password"
            helper.send_email(customer_details['org_email'], subject, email_template)

            #  Generate a user account activation email
            confirmation_code = token_handler.user_account_confirmation_token(user_id)
            email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
                                                                  confirmation_code)
            subject = "Please confirm your account"
            helper.send_email(customer_details['org_email'], subject, email_template)
            """
            customer_id = new_account.id
        
        if customer_details['type'] == "Individual":
            #   create a new individual customer detail
            self.create_individual_customer(customer_row.id, customer_details['salutation'])
            self.role_placement(customer_row.id, "IND")
        elif customer_details['type'] == "Organization":
            new_org_customer = OrganizationCustomer(
                customer_details['org_type'],
                customer_details["org_name"],
                customer_details['org_phone'],
                customer_details['org_email'],
                customer_details['reg_number'],
                # customer_account_number,
                customer_details['physical_address'],
                customer_details['postal_code'],
                customer_details['postal_town'],
                customer_details['county'],
                customer_details['constituency'],
                customer_details['ward'],
                customer_details['facebook'],
                customer_details['instagram'],
                customer_details['twitter'],
                customer_row.id
            )
            new_org_customer.save()
            self.role_placement(customer_row.id, "ORG")
        # ToDo: Create a customer number and enter into affiliation
        # ToDo: create a staff model where we can get agent_broker id in case a staff member enrolled the customer
        # create a new affiliation between the customer and broker/agent
        # each affiliation must only exist once in the db
        # we need to fetch the role of the agent/broker and associate it into the affiliation

        """
        # If individual customer already created an account
        if customer_details["type"] == "Individual":
            if customer_row:
                # Create an individual customer
                customer_number = self.create_customer_number('IN', customer_row.id, customer_details['country'])
                self.create_individual_customer(customer_row.id, customer_details['salutation'], customer_number)
                # assign role
                self.role_placement(customer_row.id, "IND")
            else:
                # assign role
                self.role_placement(new_account.id, "IND")
                # Create individual customer
                customer_number = self.create_customer_number('IN', customer_row.id, customer_details['country'])
                self.create_individual_customer(new_individual_cust.id, customer_details['salutation'], customer_number)

                #  Send temporary password to user via email
                email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
                                                                      temporary_pass)
                subject = "Your Nexure Temporary Password"
                helper.send_email(customer_details['email'], subject, email_template)

                #  Generate a user account activation email
                confirmation_code = token_handler.user_account_confirmation_token(user_id)
                email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
                                                                      confirmation_code)
                subject = "Please confirm your account"
                helper.send_email(customer_details['email'], subject, email_template)

        # Customer on boarding for organizations
        if customer_details["type"] == "Organization":
            # create a new user account using the organization email
            # assign role
            self.role_placement(new_account.id, "ORG")

            # create a new "organization" customer account
            new_org_cust = OrganizationCustomer(
                customer_details['org_type'],
                customer_details["org_name"],
                customer_details['org_phone'],
                customer_details['org_email'],
                self.create_customer_number(customer_details['org_type'], customer_row.id, 'KE'),
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
                customer_details["email"]
            )
            new_org_cust.save()

            #  Send temporary password to user via email
            email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
                                                                  temporary_pass)
            subject = "Your Nexure Temporary Password"
            helper.send_email(customer_details['org_email'], subject, email_template)

            #  Generate a user account activation email
            confirmation_code = token_handler.user_account_confirmation_token(user_id)
            email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
                                                                  confirmation_code)
            subject = "Please confirm your account"
            helper.send_email(customer_details['org_email'], subject, email_template)

        # Send the user an email confirmation with their temporary password. Advice them to change it.
        response = helper.make_rest_success_response(
            f"Customer has been on boarded successfully. Please check your email for further instructions")
        return make_response(response, 200)
        """
        uid = get_jwt_identity()
        # we need to check whether the current user is a staff member or an agent/broker
        u_role = UserRolePlacement.fetch_role_by_user_id(uid)
        u_role_id = u_role.role_id
        role_name = Roles.fetch_role_by_id(u_role_id)
        if role_name == 'STF':
            staff_member = Staff.fetch_staff_by_id(uid)
            agent_broker_id = staff_member.agent_broker_id
            new_affiliation = CustomerAffiliation(customer_number, agent_broker_id, uid)
            new_affiliation.save()
        else:
            new_affiliation = CustomerAffiliation(customer_number, uid)
            new_affiliation.save()

        response_msg = helper.make_rest_success_response("New customer has been on boarded successfully!")
        return make_response(response_msg, 200)     

    @staticmethod
    def create_individual_customer(cust_id, salutation):
        new_individual_cust = IndividualCustomer(cust_id, salutation)
        new_individual_cust.save()

    @staticmethod
    def role_placement(role_id, role):
        new_user_role = UserRolePlacement(
            role_id,
            Role.fetch_role_by_name(role)
        )
        new_user_role.save()

    @staticmethod
    def create_customer_number(org_type, user_id, country):
        customer_helper = CustomerNumber(org_type, user_id, country)
        return customer_helper.generate_customer_number()


class OrganizationType(Resource):
    def get(self):
        data = OrganizationTypes.get_organization_customer_types()
        if data:
            message = "Request successful"
            response = helper.make_rest_success_response(message, data)
            return make_response(response, 200)

        message = "No data was found"
        response = helper.make_rest_fail_response(message)
        return make_response(response, 404)


class OrganizationCustomerResource(Resource):
    def get(self):
        data = OrganizationCustomer.get_all_organization_customers()
        if data:
            message = "success"
            response_msg = helper.make_rest_success_response(message, data)
            return make_response(response_msg, 200)

        message = "No data was found in database"
        response_msg = helper.make_rest_fail_response(message)

        return make_response(response_msg, 404)

class AddStaff(Resource):
    def post:
        # create a new user with log in details
        pass

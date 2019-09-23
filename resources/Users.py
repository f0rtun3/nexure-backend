from flask import current_app as application
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims, jwt_refresh_token_required
from models.User import User
from models.UserProfile import UserProfile
from models.IndependentAgent import IndependentAgent
from models.TiedAgent import TiedAgents
from models.Broker import Broker
from models.Role import Role
from models.UserRolePlacement import UserRolePlacement
from models.InsuranceCompany import InsuranceCompany
from models.UserPermissions import UserPermissions
#   from models.IndividualCustomer import IndividualCustomer
from helpers import helpers as helper
import helpers.tokens as token_handler
from helpers.parsers import user_parser
import uuid
from datetime import datetime


class UserRegister(Resource):
    def post(self):
        # get the user details from the request sent by the client
        user_details = user_parser.parse_args()
        # check if the user exists before registering them
        user_db_row = User.get_user_by_email(user_details['email'])
        if user_db_row:
            err_msg = f"{user_details['email']} already exists"
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

        # Account confirmation email generation
        # Save extra user details depending on their role
        role = user_details["role"]
        self.onboard_client(role, new_user_authentication.id, user_details)

        #   Send a confirmation link to the user for account confirmation
        confirmation_code = token_handler.user_account_confirmation_token(
            new_user_authentication.id)
        email_template = helper.generate_confirmation_template(application.config['CONFIRMATION_ENDPOINT'],
                                                               confirmation_code)
        subject = "Please confirm your account"
        email_text = f"Use this link {application.config['CONFIRMATION_ENDPOINT']}/{confirmation_code}" \
                     f" to confirm your account"
        # ToDo: Remember to uncomment the line below before commit to remote branch
        #   helper.send_email(user_details['email'], subject, email_template, email_text)

        response_msg = helper.make_rest_success_response("Registration successful, kindly"
                                                         " check your email for confirmation link")
        return make_response(response_msg, 200)

    @jwt_required
    def get(self):
        """
        get user profile details
        """
        user_id = get_jwt_identity()
        claims = get_jwt_claims()
        role = claims['role']
        profile_data = self.fetch_profile_data(role, user_id)
        if profile_data is None:
            response = helper.make_rest_fail_response("No user was found")
            return make_response(response, 404)

        response = helper.make_rest_success_response(None, {"profile_details": profile_data})
        return make_response(response, 200)

    def fetch_profile_data(self, role, user_id):
        profile_data = {}
        if role in ('IND', 'TA'):
            profile_data['profile_details'] = User.get_user_by_id(
                user_id).serialize()
        elif role == 'BR':
            profile_data = Broker.get_broker_by_contact_id(user_id).serialize()
        elif role == 'IA':
            profile_data = IndependentAgent.get_agency_by_contact_person(
                user_id).serialize()
        elif role == 'IC':
            profile_data = InsuranceCompany.get_company_by_contact_person(
                user_id).serialize()
        else:
            return None
        return profile_data

    @jwt_required
    def put(self):
        """
        registration completion of a user
        :return:
        """
        # get user id
        user_id = get_jwt_identity()
        # get the user details from the request sent by the client
        user_details = user_parser.parse_args()
        # check if the user exists
        user = User.get_user_by_id(user_id)
        # if user exists, then update their details
        if user:
            # get their role
            claims = get_jwt_claims()
            role = claims['role']
            birth_date = self.format_birth_date(user_details['birth_date'])
            if user_details['update_type'] == "password":
                if user_details['new_password']:
                    user = User.get_user_by_id(get_jwt_identity())
                    password = user.generate_password_hash(
                        user_details['new_password'])
                    user.update_password(password)

            elif user_details['update_type'] == "personal":
                personal_data = self.set_personal_data(user_details['first_name'], user_details['last_name'],
                                                       user_details['mob'], user_details['gender'],
                                                       user_details['occupation'],
                                                       user_details['id_passport'], user_details['kra_pin'],
                                                       birth_date
                                                       )
                self.update_profile(user_id, personal_data)

            elif user_details['update_type'] == "location":
                location_data = self.set_location_data(user_details['physical_address'],
                                                       user_details['postal_address'], user_details['postal_code'],
                                                       user_details['postal_town'], user_details['country'],
                                                       user_details['county'], user_details['constituency'],
                                                       user_details['ward']
                                                       )
                self.update_profile(user_id, location_data)

            elif user_details['update_type'] == "agency":

                profile_data = self.set_profile_data(user_details['first_name'], user_details['last_name'],
                                                     user_details['gender'], user_details['occupation'],
                                                     user_details['id_passport'], user_details['kra_pin'],
                                                     birth_date, user_details['physical_address'],
                                                     user_details['postal_address'], user_details['postal_code'],
                                                     user_details['postal_town'], user_details['country'],
                                                     user_details['county'], user_details['constituency'],
                                                     user_details['ward']
                                                     )
                self.update_profile(user_id, profile_data)
            """
            update the client account depending on their role: 
            Note: that for tied agents, we only update their profiles
            """
            client_row = self.get_client_row(role, user_id)
            if role == 'BR':
                agency = Broker.get_broker_by_contact_id(user_id)
                data = self.set_broker_data(self.check_updated_organization_detail(client_row.broker_name,
                                                                                   user_details['org_name']),
                                            self.check_updated_organization_detail(client_row.broker_phone_number,
                                                                                   user_details['org_phone']),
                                            self.check_updated_organization_detail(client_row.broker_email,
                                                                                   user_details['org_email']),
                                            user_details['ira_reg_no'], user_details['ira_license_no'],
                                            user_details['org_kra_pin'], user_details['website'],
                                            user_details['facebook'], user_details['instagram'],
                                            user_details['twitter']
                                            )
            elif role == 'IA':
                """
                One contact person only represents one entity. So, we fetch the agency using the contact person's id 
                """
                agency = IndependentAgent.get_agency_by_contact_person(
                    user_id)

                data = {
                    "agency_name": user_details['org_name'],
                    "agency_phone": user_details['org_phone_number'],
                    "agency_email": user_details['org_email'],
                    "ira_registration_number": user_details['ira_reg_no'],
                    "ira_license_number": user_details['ira_license_no'],
                    "kra_pin": user_details['org_kra_pin'],
                    "website": user_details['website'],
                    "facebook": user_details['facebook'],
                    "instagram": user_details['instagram'],
                    "twitter": user_details['twitter']
                }
            
            elif role == 'IC':
                agency = InsuranceCompany.get_company_by_contact_person(user_id)
                data = self.set_ic_data(user_details['bank_account_number'], user_details['mpesa_paybill'],
                                        user_details['ira_reg_no'], user_details['ira_license_no'],
                                        user_details['org_kra_pin'], user_details['website'],
                                        user_details['facebook'], user_details['instagram'],
                                        user_details['twitter']
                                        )
            agency.update(data)
        else:
            # if user does not exist
            response_msg = helper.make_rest_fail_response(
                "User does not exist")
            return make_response(response_msg, 404)

        # update was successful
        response_msg = helper.make_rest_success_response(
            f"Update successful.")
        return make_response(response_msg, 200)

    @staticmethod
    def check_updated_organization_detail(previous_detail, updated_org_detiail=None):
        if updated_org_detiail is None:
            return previous_detail

        return updated_org_detiail

    @staticmethod
    def get_client_row(role, user_id):
        if role == 'BR':
            client_row = Broker.get_broker_by_contact_id(user_id)
        elif role == 'IA':
            client_row = IndependentAgent.get_agency_by_contact_person(user_id)
        elif role == 'IC':
            client_row = InsuranceCompany.get_company_by_contact_person(
                user_id)
        else:
            return False

        return client_row

    @staticmethod
    def set_profile_data(first_name, last_name, gender, occupation, id_passport, kra_pin, birth_date, physical_address,
                         postal_address, postal_code, postal_town, country, county, constituency, ward):
        return {
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "occupation": occupation,
            "id_passport": id_passport,
            "kra_pin": kra_pin,
            "birth_date": birth_date
        }

    @staticmethod
    def set_location_data(physical_address, postal_address, postal_code, postal_town,country, county, constituency,
                          ward):
        return {
            "physical_address": physical_address,
            "postal_address": postal_address,
            "postal_code": postal_code,
            "postal_town": postal_town,
            "country": country,
            "county": county,
            "constituency": constituency,
            "ward": ward
        }

    @staticmethod
    def set_broker_data(org_name, org_phone_number, org_email, ira_reg_no, ira_license_no, org_kra_pin, website,
                        facebook, twitter, instagram):
        return {
            "broker_name": org_name,
            "broker_phone_number": org_phone_number,
            "broker_email": org_email,
            "ira_registration_number": ira_reg_no,
            "ira_license_number": ira_license_no,
            "kra_pin": org_kra_pin,
            "website": website,
            "facebook": facebook,
            "instagram": twitter,
            "twitter": instagram
        }

    @staticmethod
    def set_ia_data(org_name, org_phone_number, org_email, ira_reg_no, ira_license_no, org_kra_pin, website,
                    facebook, twitter, instagram):
        return {
            "agency_name": org_name,
            "agency_phone": org_phone_number,
            "agency_email": org_email,
            "ira_registration_number": ira_reg_no,
            "ira_licence_number": ira_license_no,
            "kra_pin": org_kra_pin,
            "website": website,
            "facebook": facebook,
            "instagram": instagram,
            "twitter": twitter
        }

    @staticmethod
    def set_ic_data(bank_account_number, company_phone, mpesa_paybill, ira_reg_no, ira_license_no, org_kra_pin, website,
                    facebook, twitter, instagram):
        return {
            "bank_account": bank_account_number,
            "company_phone": company_phone,
            "mpesa_paybill": mpesa_paybill,
            "ira_registration_number": ira_reg_no,
            "ira_license_number": ira_license_no,
            "kra_pin": org_kra_pin,
            "website": website,
            "facebook": facebook,
            "instagram": instagram,
            "twitter": twitter,
        }

    @staticmethod
    def format_birth_date(date_str):
        b_day = datetime.strptime(date_str, '%d/%m/%Y')
        return b_day.date()

    @staticmethod
    def update_profile(uid, data):
        profile = UserProfile.get_profile_by_user_id(uid)
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
                user_id,
                user_details['company_id'],
                user_details['org_phone']
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
                user_details["org_name"],
                user_details["org_phone"],
                user_details["org_email"],
                user_id
            )
            new_broker.save()
        else:
            return


class AccountConfirmation(Resource):
    """
    Handle user account activation
    if the sent token is expured, a request handler will send a fresh token
    """

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


class AccountConfirmationResource(Resource):
    def get(self, user_id):
        """
        If the jwt token has expired
        a user can request for another token here simple by passing in the user_id
        """
        user_row = User.get_user_by_id(user_id)
        if user_row:
            # awesome, user account exists, let's go ahead and resend the activation email to the user
            confirmation_code = token_handler.user_account_confirmation_token(
                user_id)
            email_template = helper.generate_confirmation_template(application.config['CONFIRMATION_ENDPOINT'],
                                                                   confirmation_code)
            subject = "Please confirm your account"
            email_text = f"Use this link {application.config['CONFIRMATION_ENDPOINT']}/{confirmation_code}" \
                         f" to confirm your account"
            helper.send_email(user_row.email, subject,
                              email_template, email_text)
            response = helper.make_rest_success_response(
                "Please check your email to confirm your account")
            return make_response(response, 200)

        response = helper.make_rest_fail_response(
            "User was not found, please try again or register a new account")
        return make_response(response, 404)


class UserLogin(Resource):
    """
    let's authenticate the user to the system upon sign in here
    """

    def post(self):
        # this is the POST request resource to handle user signin

        user_details = user_parser.parse_args()
        # check whether the user exists before confirming
        user_db_row = User.get_user_by_email(user_details['email'])

        if not user_db_row:
            response_msg = helper.make_rest_fail_response(
                "User email does not exist")
            return make_response(response_msg, 404)

        # good, let's go ahead and authenticate the user now
        # we also need to check whether the user account is verified or not
        # we don't want inactive accounts accessing our system
        if user_db_row.check_password_hash(user_details['password']):
            if user_db_row.is_active:
                # generate an access and refresh tokens for the user, for obvious reasons
                # also return the user role as a token claim, we'll need that for subsequent
                # requests from the client
                role = self.get_user_role(user_db_row.id)
                auth_tokens = token_handler.create_user_token(
                    user_db_row.id, role)
                response_dict = {
                    "authentication": auth_tokens,
                    "role": role
                }
                if role in ("BRSTF", "TASTF", "IASTF"):
                    # if the authenticated user is a staff member,
                    # get the corresponding permissions
                    response_dict['permission'] = UserPermissions.get_permission_by_user_id(
                        user_db_row.id)

                response_msg = helper.make_rest_success_response(
                    "Successfully logged in", response_dict)
                return make_response(response_msg, 200)
            else:
                response_msg = helper.make_rest_fail_response(
                    "Please confirm your account before signing in.")
                return make_response(response_msg, 401)
        else:
            # wrong credentials passed, return the appropriate message
            response_msg = helper.make_rest_fail_response(
                "Wrong credentials passed, please try again")
            return make_response(response_msg, 401)

    @staticmethod
    def get_user_role(user_id):
        """
        get the user role by id, this is needed to throttle permissions on modules to access
        """
        role = UserRolePlacement.fetch_role_by_user_id(user_id)
        role_name = Role.fetch_role_by_id(role)
        return role_name


class TokenRefresh(Resource):
    """
    A token refresh resource
    method['POST']
    obtain a fresh token after previous one has expired
    """
    @jwt_refresh_token_required
    def get(self):
        """
        generate an  unfresh token
        unfortunately this token is limited to certain CRUD operations
        """
        curr_user_id = get_jwt_identity()  # Fetch supervisor_id
        claims = get_jwt_claims()
        role = claims['role']
        new_token = token_handler.create_refresh_token(curr_user_id, role)
        response = {
            'access_token': new_token
        }
        return make_response(helper.make_rest_success_response("Success", response))


class AccountRecovery(Resource):
    """
    When the users forget their password, we need to take appropriate steps to recover their account
    """

    def post(self):
        """
        send the user an email containing a link to set a new password
        :arg email {string} user email whose account we intend to recover
        :return:
        """
        user_details = user_parser.parse_args()
        user_row = User.get_user_by_email(user_details['email'])
        if user_row:
            account_token = token_handler.user_account_confirmation_token(
                user_row.id)
            email_text = f"To Please follow this link to reset your password " \
                         f"{application.config['ACCOUNT_RESET_ENDPOINT']}/{account_token}"
            email_template = helper.generate_account_recovery_template(application.config['ACCOUNT_RESET_ENDPOINT'],
                                                                       account_token)
            subject = "Account Password Recovery"
            helper.send_email(
                user_details['email'], subject, email_template, email_text)
            response_msg = helper.make_rest_success_response("Successfully sent account recovery steps, check your"
                                                             " email")
            return make_response(response_msg, 200)

        response_msg = helper.make_rest_fail_response(
            "There is not account associated with this email")
        return make_response(response_msg, 404)

    @jwt_required
    def put(self):
        """
        when the user resets the password, 
        we will update the same here
        :return:
        """
        user_id = get_jwt_identity()
        user_details = user_parser.parse_args()
        user = User.get_user_by_id(user_id)
        if user:
            password = user.generate_password_hash(
                user_details['new_password'])
            user.update_password(password)
            response_msg = helper.make_rest_success_response(
                "Successfully recovered user account")
            return make_response(response_msg, 200)

        response_msg = helper.make_rest_fail_response(
            "Sorry, user does not exist in this database")
        return make_response(response_msg, 404)

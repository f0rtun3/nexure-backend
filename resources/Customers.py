"""
Cusomer resources handler
new customer onboarding
"""
from app import app
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.User import User
from models.IndividualCustomer import IndividualCustomer
from models.UserProfile import UserProfile
from models.IndependentAgent import IndependentAgent
from models.TiedAgent import TiedAgents
from models.Broker import Broker
from models.BRCustomer import BRCustomer
from models.TACustomer import TACustomer
from models.IACustomer import IACustomer
from models.BRStaff import BRStaff
from models.TAStaff import TAStaff
from models.IAStaff import IAStaff
from models.Role import Role
from models.UserRolePlacement import UserRolePlacement
from models.InsuranceCompany import InsuranceCompany
from models.OrganizationCustomer import OrganizationCustomer
from models.OrganizationTypes import OrganizationTypes
import helpers.helpers as helper
from helpers.parsers import customer_parser
from helpers.CustomerNumber import CustomerNumber
import helpers.tokens as token_handler
import uuid


class CustomerOnBoarding(Resource):
    """
    An agent or broker may on-board a new customer into the system
    If the customer already exists in the system, we only associate them with the affiliated broker/agent
    otherwise we add a new user create a temporary password, generate customer number for them and associate the new
    user with the affiliated agent/broker
    """
    @jwt_required
    def post(self):
        customer_details = customer_parser.parse_args()

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
        customer_id = new_account.id
        # create individual customer's profile
        new_individual_profile = UserProfile(
            customer_id,
            customer_details["first_name"],
            customer_details["last_name"],
            customer_details["phone"],
            customer_details["gender"],
            customer_details["avatar_url"],
            customer_details["occupation"],
            customer_details["id_passport"],
            customer_details["kra_pin"],
            customer_details["birth_date"],
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

        email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
                                                              temporary_pass)
        subject = "Nexure Temporary Password"
        helper.send_email(customer_details['org_email'], subject, email_template)

        #  Generate a user account activation email
        confirmation_code = token_handler.user_account_confirmation_token(customer_id)
        email_template = helper.generate_confirmation_template(app.config['CONFIRMATION_ENDPOINT'],
                                                              confirmation_code)
        subject = "Please confirm your account"
        helper.send_email(customer_details['org_email'], subject, email_template)

        customer_acc_number = ""
        if customer_details['type'] == "Individual":
            #   create a new individual customer detail
            customer_acc_number = self.create_customer_number("IN", customer_id, customer_parser['country'])
            customer_acc = self.create_individual_customer(customer_id, customer_details['salutation'], customer_acc_number)
            self.role_placement(customer_id, "IND")
        elif customer_details['type'] == "Organization":
            customer_acc_number = self.create_customer_number(customer_parser['org_type'],
                                                              customer_id, customer_parser['country'])
            new_org_customer = OrganizationCustomer(
                customer_details['org_type'],
                customer_details["org_name"],
                customer_details['org_phone'],
                customer_details['org_email'],
                customer_details['reg_number'],
                customer_acc_number,
                customer_details['physical_address'],
                customer_details['postal_code'],
                customer_details['postal_town'],
                customer_details['county'],
                customer_details['constituency'],
                customer_details['ward'],
                customer_details['facebook'],
                customer_details['instagram'],
                customer_details['twitter'],
                customer_id
            )
            new_org_customer.save()
            self.role_placement(customer_id, "ORG")

        # create a new affiliation between the customer and broker/agent
        # each affiliation must only exist once in the db
        # we need to fetch the role of the agent/broker and associate it into the affiliation

        uid = get_jwt_identity()
        # we need to check whether the current user is a staff member or an agent/broker
        role_name = self.get_role_name(uid)
        agent_broker = self.check_staff(uid, role_name)
        if agent_broker:
            self.register_customer(role_name, customer_acc_number, agent_broker, uid)
        else:
            self.register_customer(role_name, customer_acc_number, uid)

        response_msg = helper.make_rest_success_response("New customer has been on boarded successfully!")
        return make_response(response_msg, 200)

    @jwt_required
    def get(self):
        data = OrganizationTypes.get_organization_customer_types()
        if data:
            message = "Request successful"
            response = helper.make_rest_success_response(message, data)
            return make_response(response, 200)

        message = "No data was found"
        response = helper.make_rest_fail_response(message)
        return make_response(response, 404)

    @staticmethod
    def create_individual_customer(cust_id, salutation, customer_number):
        new_individual_cust = IndividualCustomer(cust_id, salutation, customer_number)
        new_individual_cust.save()

    def get_role_name(self, uid):
        u_role = UserRolePlacement.fetch_role_by_user_id(uid)
        u_role_id = u_role.role_id
        return Role.fetch_role_by_id(u_role_id)

    def check_staff(self, uid, role_name):
        """
        check whether the user on boarding the customer is a staff member or not
        :param role_name:
        :return:
        """
        roles = ["BRSTF", "IASTF", "TASTF"]
        if role_name in roles:
            if role_name == "BRSTF":
                return BRStaff.fetch_broker_by_staff(uid)
            elif role_name == "TASTF":
                return TAStaff.fetch_agent_by_staff(uid)
            elif role_name== "IASTF":
                return IAStaff.fetch_agent_by_staff(uid)

        return

    @staticmethod
    def register_customer(atype, customer_number, uid, staff_id=None):
        if atype == "BRSTF":
            new_customer = BRCustomer(customer_number, uid, staff_id)
            new_customer.save()
        elif atype == "TASTF":
            new_customer = TACustomer(customer_number, uid, staff_id)
            new_customer.save()
        else:
            new_customer = IACustomer(customer_number, uid, staff_id)
            new_customer.save()

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

    @jwt_required
    def put(self):
        """
        deactivate the user account
        :return:
        """
        pass

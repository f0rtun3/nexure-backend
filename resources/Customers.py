"""
Cusomer resources handler
new customer onboarding
"""
from flask import current_app as application
from flask import make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from Controllers import customer
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
from models.ChildPolicy import ChildPolicy
from models.OrganizationCustomer import OrganizationCustomer
from models.OrganizationTypes import OrganizationTypes
from helpers import helpers as helper
from helpers.parsers import customer_parser
from helpers.CustomerNumber import CustomerNumber
import helpers.tokens as token_handler
import uuid
import json


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
        customer = User.get_user_by_email(customer_details['email'])
        customer_acc_number = None
        if not customer:
            # Create temporary seven digit password
            temporary_pass = helper.create_user_password()
            # create a new user account if not existing
            user_id = uuid.uuid4()
            # create new user
            new_account = User(
                user_id,
                customer_details['email'],
                temporary_pass
            )
            new_account.save()
        
            # if onboarding an individual customer
            if customer_details['type'] == 'Individual':
                customer = User.get_user_by_email(customer_details['email'])
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
                    customer_details['postal_address'],
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

                #  create a new individual customer detail
                customer_number = self.create_customer_number(
                    "IN", customer_id, customer_details['country'])
                self.create_individual_customer(
                    customer_id, customer_number, customer_details['salutation'])
                self.role_placement(customer_id, "IND")

                # send activation email
                self.send_activation_email(customer_details['email'], customer_id, temporary_pass)

                # assign customer number to individual customer number
                customer_acc_number = customer_number

            # if onboarding an organization
            elif customer_details['type'] == "Organization":
                customer_id = new_account.id
                customer_number = self.create_customer_number(customer_details['org_type'],
                                                                customer_id, customer_details['country'])
                # Add contact person details
                contact_person = UserProfile(
                    customer_id,
                    customer_details['first_name'],
                    customer_details['last_name'],
                    customer_details["phone"]                
                )
                contact_person.save()

                new_org_customer = OrganizationCustomer(
                    customer_details['org_type'],
                    customer_details["org_name"],
                    customer_details['org_phone'],
                    customer_details['org_email'],
                    customer_details['reg_number'],
                    customer_details['physical_address'],
                    customer_details['postal_address'],
                    customer_details['postal_code'],
                    customer_details['postal_town'],
                    customer_details['county'],
                    customer_details['constituency'],
                    customer_details['ward'],
                    customer_details['facebook'],
                    customer_details['instagram'],
                    customer_details['twitter'],
                    customer_id,
                    customer_number
                )
                new_org_customer.save()
                self.role_placement(customer_id, "ORG")

                # send activation email
                self.send_activation_email(customer_details['email'], customer_id, temporary_pass)

                # assign customer number to individual customer number
                customer_acc_number = customer_number

        # create a new affiliation between the customer and broker/agent
        # each affiliation must only exist once in the db
        # we need to fetch the role of the agent/broker and associate it into the affiliation

        uid = get_jwt_identity()
        # we need to check whether the current user is a staff member or an agent/broker
        role_name = self.get_role_name(uid)
        agent_broker = self.check_staff(uid, role_name)

        if agent_broker:
            # the current user is not a staff member
            # we also need to ensure the affiliation created is not a duplicate one
            if not self.is_affiliation_duplicate(role_name, agent_broker, customer_acc_number):
                self.register_customer(
                    role_name, customer_acc_number, agent_broker, uid)
            else:
                response_msg = helper.make_rest_fail_response(
                    "This affiliation was already created")
                return make_response(response_msg, 409)
        else:
            broker_agent_id = self.get_broker_agent_id(uid, role_name)
            if not self.is_affiliation_duplicate(role_name, broker_agent_id, customer_acc_number):
                self.register_customer(
                    role_name, customer_acc_number, broker_agent_id)
            else:
                response_msg = helper.make_rest_fail_response(
                    "This affiliation was already created")
                return make_response(response_msg, 409)

        response_msg = helper.make_rest_success_response(
            "Customer has been onbarded successfully", {"customer_number": customer_acc_number})
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

    @jwt_required
    def delete(self):
        """
        deactivate the user account
        :return:
        """
        role = get_jwt_claims()['role']
        customer = json.dumps(customer_parser.parse_args())
        cust_no = customer['cust_no']

        # update the customer agency relationship if activated
        self.delete_cust_agency_relationship(role, cust_no)
        response = helper.make_rest_success_response("User was deleted")
        return make_response(response, 200)

    @jwt_required
    def put(self):
        """
        Update customer details
        activate or deactivate customer permissions
        """
        role = get_jwt_claims()['role']
        cust_info = customer_parser.parse_args()
        cust_no = cust_info['cust_no']
        cust_id = helper.get_customer_id(cust_no)
        cust_profile = UserProfile.get_profile_by_user_id(cust_id)
        cust_auth = User.get_user_by_id(cust_id)
        cust_profile.update(cust_info)
        cust_auth.update(cust_info)

        # update the respective organization or individual details
        self.update_cust_details(cust_id, cust_no, cust_info)
        self.update_cust_agency_relationship(
            role, cust_no, cust_info['status'])
        response = helper.make_rest_success_response("Update was successful")
        return make_response(response, 200)

    @staticmethod
    def send_activation_email(email, customer_id, temporary_pass):
        email_template = helper.generate_confirmation_template(application.config['LOGIN_ENDPOINT'],
                                                               temporary_pass)
        subject = "Nexure Temporary Password"
        email_text = f"Follow {application.config['LOGIN_ENDPOINT']} to login and use {temporary_pass} " \
            f"as your temporary password"
        helper.send_email(
            email, subject, email_template, email_text)

        #  Generate a user account activation email
        confirmation_code = token_handler.user_account_confirmation_token(
            customer_id)
        email_template = helper.generate_confirmation_template(application.config['CONFIRMATION_ENDPOINT'],
                                                               confirmation_code)
        subject = "Please confirm your account"
        email_text = f"Use this link {application.config['CONFIRMATION_ENDPOINT']}/{confirmation_code}" \
            f" to confirm your account"
        helper.send_email(
            email, subject, email_template, email_text)

    @staticmethod
    def create_individual_customer(cust_id, customer_number, salutation):
        new_individual_cust = IndividualCustomer(
            cust_id, customer_number, salutation)
        new_individual_cust.save()

    def get_role_name(self, uid):
        u_role = UserRolePlacement.fetch_role_by_user_id(uid)
        return Role.fetch_role_by_id(u_role)

    def get_broker_agent_id(self, contact_id, atype):
        agent_broker_id = None
        if atype == "BR":
            agent_broker_id = Broker.get_broker_by_contact_id(contact_id)
            return agent_broker_id.broker_id
        elif atype == "TA":
            agent_broker_id = TiedAgents.get_tied_agent_by_user_id(contact_id)
            return agent_broker_id.id
        else:
            agent_broker_id = IndependentAgent.get_agency_by_contact_person(
                contact_id)
            return agent_broker_id.id

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
            elif role_name == "IASTF":
                return IAStaff.fetch_agent_by_staff(uid)

        return

    @staticmethod
    def register_customer(atype, customer_number, uid, staff_id=None):
        if atype in ("BRSTF", "BR"):
            if BRCustomer.check_duplicate_affiliation(uid, customer_number):
                new_customer = BRCustomer(customer_number, uid, staff_id)
                new_customer.save()
            else:
                return False
        elif atype in ("TASTF", "TA"):
            new_customer = TACustomer(customer_number, uid, staff_id)
            new_customer.save()
        else:
            new_customer = IACustomer(customer_number, uid, staff_id)
            new_customer.save()

    @staticmethod
    def is_affiliation_duplicate(atype, agent_broker_id, customer_number):
        if atype in ("BRSTF", "BR"):
            return BRCustomer.check_duplicate_affiliation(agent_broker_id, customer_number)
        elif atype in ("TASTF", "TA"):
            return IACustomer.check_duplicate_affiliation(agent_broker_id, customer_number)
        elif atype in ("IASTF", "TA"):
            return TACustomer.check_duplicate_affiliation(agent_broker_id, customer_number)

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

    def update_cust_agency_relationship(self, role, cust_no, status):
        customer = self.fetch_customer_by_relationship(role, cust_no)
        customer.status = status
        customer.update()

    @staticmethod
    def fetch_customer_by_relationship(role, cust_no):
        customer = None
        if role in ("BR", "BRSTF"):
            customer = BRCustomer.get_affiliation_by_customer(cust_no)
        elif role in ("TA", "TASTF"):
            customer = TACustomer.get_affiliation_by_customer(cust_no)
        elif role in ("IA", "IASTF"):
            customer = IACustomer.get_affiliation_by_customer(cust_no)

        return customer

    def delete_cust_agency_relationship(self, role, cust_no):
        customer = self.fetch_customer_by_relationship(role, cust_no)
        customer.delete()

    @staticmethod
    def update_cust_details(cust_id, cust_no, cust_info):
        customer_type = helper.get_customer_type(cust_no)
        if customer_type == 'IN':
            customer_details = IndividualCustomer.get_customer_by_user_id(cust_id)
            customer_details.update(cust_info)
        else:
            customer_details = OrganizationCustomer.get_customer_by_contact(cust_id)
            customer_details.update(cust_info)


class AgencyCustomers(Resource):
    """
    Handles agency customer details
    """
    @jwt_required
    def get(self):
        """
        get agent specific customers
        :return:
        """
        current_user = get_jwt_identity()
        current_user_claims = get_jwt_claims()
        current_user_role = current_user_claims['role']
        agency_id = customer.get_agent_id(current_user_role, current_user)
        agency_customers = customer.get_customer_details(current_user_role, agency_id)

        if agency_customers:
            return make_response(helper.make_rest_success_response("Success", agency_customers),
                                 200)
        else:
            return make_response(helper.make_rest_fail_response("No customers, better get to work!"),
                                 404)


class CustomerPolicyHandler(Resource):
    """
    handles customer specific policies
    """
    #   @jwt_required
    def get(self, customer_number):
        """
        get the customer active child policies
        this is needed for the payments module where user's active policy payments will be tracked
        :return:
        """
        customers = ChildPolicy.get_child_policies(customer_number)
        if customers:
            return make_response(helper.make_rest_success_response("success", customers), 200)

        return make_response(helper.make_rest_fail_response("No customer policies were found"), 404)




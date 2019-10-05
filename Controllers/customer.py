"""
customer controller functions
"""
from models.BRStaff import BRStaff
from models.TAStaff import TAStaff
from models.IAStaff import IAStaff
from models.BRCustomer import BRCustomer
from models.TACustomer import TACustomer
from models.IACustomer import IACustomer


def get_agent_id(user_role, user_id):
    """
    from the jwt, we need to get the organization specific id
    this is necessary to get the agent specific customers
    :param user_role:
    :param user_id:
    :return {number}:
    """
    if user_role == 'IA':
        agency_id = IAStaff.query.filter_by(user_id=user_id).first().agent_id

    elif user_role == 'BR':
        agency_id = BRStaff.query.filter_by(user_id=user_id).first().broker_id

    elif user_role == 'TA':
        agency_id = TAStaff.query.filter_by(user_id=user_id).first().agent_id

    else:
        return None

    return agency_id


def get_customer_details(user_role, agency_id):
    """
    get all the agency specific customers
    :param user_role:
    :param agency_id:
    :return:
    """
    if user_role == 'IA':
        customers = IACustomer.get_customers(agency_id)

    elif user_role == 'BR':
        customers = BRCustomer.get_customers(agency_id)

    elif user_role == 'TA':
        customers = TACustomer.get_customers(agency_id)

    else:
        return None

    return customers

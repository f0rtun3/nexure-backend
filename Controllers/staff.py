from models.IndependentAgent import IndependentAgent
from models.TiedAgent import TiedAgents
from models.Broker import Broker
from models.BRStaff import BRStaff
from models.TAStaff import TAStaff
from models.IAStaff import IAStaff


def update_account_status(role, staff_id, status):
    if role == "BR":
        staff_acc = BRStaff.get_staff_by_user_id(staff_id)
        staff_acc.update({"active": status})
        return True
    elif role == "TA":
        staff_acc = TAStaff.get_staff_by_user_id(staff_id)
        staff_acc.update({"active": status})
        return True
    elif role == "IA":
        staff_acc = IAStaff.get_staff_by_user_id(staff_id) 
        staff_acc.update({"active": status})
        return True
    
    return False

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

def check_account_status(role, staff_id):
    account_status = True # this is the account status
    if role == "BRSTF":
        account_status = BRStaff.check_account(staff_id)
    elif role == "TASTF":
        account_status = TAStaff.check_account(staff_id)
    elif role == "IASTF":
        account_status = IAStaff.check_account(staff_id)
    
    return account_status

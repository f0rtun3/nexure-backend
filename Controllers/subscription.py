"""
user subscription handler script algorithm (python specific)
A scheduled task script that will run on a monthly basis.
Serves to deactivate the user accounts that have not been paid for as per their subscription plan.
Unsettled accounts and subsequent accounts(child accounts eg. staff accounts) will be marked as inactive
until recurring amount is settled in full.

1) START
2) users = get_all_users()
3) for user in users:
    3.1) if user.is_paid == False:
            3.1.1)  User.update({is_active: False})
            3.1.2)  role_name = user_role.get_role_name(user.id)
                    if role_name == 'BR':
                        broker_id = Broker.get_staff_member(user.id)
                        broker_staff = BRStaff.get_staff_members(broker_id)
                        for staff in broker_staff:
                            staff_auth = User.get_user_by_id(staff.id)
                            staff.update({is_active: False})
                    elif role_name == 'IA':
                        ia_id = IndependentAgent.get_staff_member(user.id)
                        ia_staff = IAStaff.get_staff_members(ia_id)
                        for staff in ia_staff:
                            staff_auth = User.get_user_by_id(staff.id)
                            staff.update({is_active: False})
4) END
"""
from models.User import User
from models.Broker import Broker
from models.BRStaff import BRStaff
from models.IndependentAgent import IndependentAgent
from models.IAStaff import IAStaff

user_accounts = User.get_all_users()

for acc in user_accounts:
    # add a subscription and billing model
    # model description
    # user_id (INT) REFERENCES User(id) - the user account
    # subscription_plan (String) - the billing frequency(may be yearly or monthly)
    # discount (INT) - this may be a discount offered upon renewal or first time subscription
    # amount (INT) - the recurring billing amount
    # date_paid (Date) - the last time the subscription was paid
    # due_date (Date) - The expiry date of the subscription plan

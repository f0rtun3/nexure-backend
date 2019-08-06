#  ToDo: set up email server
#  ToDo: complete_user_profile/edit_user_profile/reset_user_password
#  ToDO: add staff member
#  ToDo: assign module permissions (customer, claims, policies, payments)
#  ToDo: select companies to work with (agencies & brokers): approved by insurance companies
"""
Customer on boarding logic
1. Fetch customer from user table
2. If customer does not exist:
        2.1 generate a temporary password for the user account
        2.2 generate a customer number for user account
        2.3 create a new user account
        2.4 send activation link and temporary password to the new customer
        2.5 create an affiliation between the new customer and the agent/broker
3. Else:
        3.1 create an affiliation between the existing customer and the agent/broker

function save the organization_details:
    if the cust_type = 'Individual':
        save the new customer to the individual customer table
    else:
        save the customer to the organization customer details
"""

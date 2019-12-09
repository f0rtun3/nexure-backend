"""
user subscription handler script
A scheduled task script that will run on a monthly basis.
Serves to deactivate the user accounts that have not been paid for as per their subscription plan.
Unsettled accounts and subsequent accounts(child accounts eg. staff accounts) will be marked as inactive
until recurring amount is settled in full.
"""

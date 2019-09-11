"""
Handles master policy, updating(endorsing), renewal etc.
"""
from models.MasterPolicy import MasterPolicy
from models.InsuranceCompany import InsuranceCompany
from datetime import datetime


class MasterController:
    @staticmethod
    def create_master_policy(policy_number, customer_number, date_expiry, insurance_company):
        # Get insurance company given the company details
        new_company = InsuranceCompany.get_by_associated_company(
            insurance_company)
        # create new master policy
        master = MasterPolicy(policy_number,
                              customer_number,
                              date_expiry,
                              new_company.id)
        master.save()
        return master

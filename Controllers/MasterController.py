"""
Handles master policy, updating(endorsing), renewal etc.
"""
from models.MasterPolicy import MasterPolicy
from Controllers.ChildController import ChildController
from models.InsuranceCompany import InsuranceCompany


class MasterController:
    @staticmethod
    def renew_transaction(master_policy_id, expiry_date, transaction_type):
        """
        Policy renewal transaction (REN)
        :param transaction_type:
        :param master_policy_id:
        :param expiry_date  the date in which the master policy will expire
        :return:
        """
        master_policy = MasterPolicy.get_policy_by_id(master_policy_id)
        master_policy_details = MasterController.fetch_latest_master_policy_details(
            master_policy.mp_number)
        if not master_policy_details:
            return None

        # add same master policy with a new id
        ren_policy_details = MasterController.create_master_policy(master_policy_details.mp_number,
                                                                   master_policy_details.customer, expiry_date,
                                                                   master_policy_details.company
                                                                   )

        child_policies = [child for child in master_policy_details['child_policies']
                          if child["transaction_type"] != 'CNC']
        for child_policy in child_policies:
            child_policy['master_policy'] = ren_policy_details
            child_policy['transaction_type'] = transaction_type
            ChildController.create_child_policy(child_policy.cp_number, child_policy.customer_number,
                                                child_policy.rate, child_policy.date_expiry,
                                                child_policy.premium_amount, child_policy.transaction_type,
                                                child_policy.agency_id, child_policy.company,
                                                child_policy.pricing_model,
                                                child_policy.master_policy, child_policy.subclass,
                                                child_policy.vehicle)
        return True

    @staticmethod
    def fetch_latest_master_policy_details(master_policy_code):
        policy_details = MasterPolicy.get_latest_policy_details(
            master_policy_code)
        return policy_details

    @staticmethod
    def fetch_master_policy(policy_id):
        policy = MasterPolicy.get_policy_by_id(policy_id)
        if not policy:
            return None

        return policy.serialize()

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

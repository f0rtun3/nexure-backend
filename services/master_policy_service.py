"""
master policy service
handles all the logic pertaining to the master policy model
"""
from models.MasterPolicy import MasterPolicy
from models.ChildPolicy import ChildPolicy
from models.PolicyBenefits import PolicyBenefits
from models.PolicyExtensions import PolicyExtensions
from models.ICBenefits import ICBenefits
from models.ICExtensions import ICExtensions


def get_single_policy_details(policy_id):
    """
    get the master policy details by id
    :param policy_id {Integer}
    :return policy_details {Object}:
    """
    policy_row = MasterPolicy.query.filter_by(id=policy_id, status=True).first()
    if policy_row:
        return policy_row.serialize()

    return None


def renew_transaction(master_policy_id, expiry_date):
    """
    Policy renewal transaction (REN)
    :param master_policy_id:
    :param expiry_date  the date in which the master policy will expire
    :return:
    """
    master_policy_details = get_single_policy_details(master_policy_id)
    if not master_policy_details:
        return None

    # add same master policy with a new id
    master = master_policy_details['master_policy']
    ren_policy_details = MasterPolicy(master.mp_number, master.customer,
                                      expiry_date, master.company
                                      )
    ren_policy_details.save()

    child_policies = master_policy_details['child_policies']
    for child_policy in child_policies:
        child_policy['master_policy'] = ren_policy_details.id
        new_child_policy = ChildPolicy(child_policy.cp_number, child_policy.vehicle,
                                       child_policy.customer_number, child_policy.rate,
                                       child_policy.date_expiry, child_policy.premium_amount,
                                       child_policy.transaction_type, child_policy.agency_id,
                                       child_policy.company, child_policy.pricing_model,
                                       child_policy.master_policy, child_policy.subclass
                                       )
        new_child_policy.save()

    return True


def get_unselected_benefits_extensions(child_policy_id):
    """
    We need to exclude the benefits and extensions that the user
    has not selected from the insurance company
    :param child_policy_id:
    :return:
    """
    child_policy = ChildPolicy.get_child_by_id(child_policy_id)
    if not child_policy:
        return None

    return {
        'extensions': get_unselected_extensions(child_policy_id),
        'benefits': get_unselected_benefits(child_policy_id)
    }


def get_unselected_benefits(child_policy_id):
    """
    unselected policy holder benefits from an insurance company
    :param child_policy_id:
    :return:
    """
    current_benefits = PolicyBenefits.get_policy_benefit_by_policy(child_policy_id)
    return ICBenefits.get_unselected_benefits(current_benefits)


def get_unselected_extensions(child_policy_id):
    """
    unselected policy holder benefits from an insurance company
    :param child_policy_id:
    :return:
    """
    current_extensions = PolicyExtensions.get_policy_ext_by_policy(child_policy_id)
    return ICExtensions.get_unselected_extensions(current_extensions)

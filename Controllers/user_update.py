"""
Profile update controller
handles complete profile and profile update
"""
from models.User import User
from models.UserProfile import UserProfile
from models.IndependentAgent import IndependentAgent
from models.InsuranceCompany import InsuranceCompany
from models.Broker import Broker
from models.UserPermissions import UserPermissions


def update_personal_details(data, user_id):
    profile_row = UserProfile.get_profile_by_user_id(user_id)
    personal_data = {
        "first_name": verify_updated_details(profile_row.first_name, data['first_name']),
        "last_name": verify_updated_details(profile_row.last_name, data['last_name']),
        "gender": data['gender'],
        "occupation": data['occupation'],
        "id_passport": data['id_passport'],
        "kra_pin": data['kra_pin'],
        "phone": verify_updated_details(profile_row.phone, data['mob']),
        "birth_date": data['birth_date']
    }
    user_auth_detail = User.get_user_by_id(user_id)
    contact_email = {"email": verify_updated_details(user_auth_detail.email, data['email'])}
    user_auth_detail.update(contact_email)
    return profile_row.update(personal_data)


def update_location_details(data, user_id):
    profile_row = UserProfile.get_profile_by_user_id(user_id)
    location_data = {
        "physical_address": data['physical_address'],
        "postal_address": data['postal_address'],
        "postal_code": data['postal_code'],
        "postal_town": data['postal_town'],
        "country": data['country'],
        "county": data['county'],
        "constituency": data['constituency'],
        "ward": data['ward']
    }
    return profile_row.update(location_data)


def update_user_password(new_password, user_id):
    profile_row = User.get_user_by_id(user_id)
    pwd_hash = profile_row.generate_password_hash(new_password)
    return profile_row.update_password(pwd_hash)


def update_agency_details(data, role, user_id):
    if role == 'BR':
        return update_broker_agent(data, user_id)
    elif role == 'IA':
        return update_independent_agent(data, user_id)
    elif role == 'IC':
        return update_insurance_company(data, user_id)
    else:
        return


def complete_user_profile(data, user_id, role):
    if role in ('IA', 'BR', 'IC'):
        update_agency_details(data, role, user_id)
    update_personal_details(data, user_id)
    update_location_details(data, user_id)
    update_social_profile(data, user_id, role)
    user = User.get_user_by_id(user_id)
    user.update({'is_complete': True})

def update_avatar_name(avatar_name, user_id, role):
    """
    image upload and update function
    :param avatar_name {string} the resource name
    :param user_id {int} the user account ID
    :param role {string} the account role of the image uploader
    """
    if role in ('IA', 'BR'):
        update_agency_avatar(avatar_name,role, user_id)
    else:
        user_acc = UserProfile.get_profile_by_user_id(user_id)
        user_acc.update({'avatar_url': avatar_name})
    return

def update_agency_avatar(avatar_name, role, user_id):
    """
    each agency needs to have their own avatar
    which is separate from the account_profile avatar
    :param avatar_name {string} the resource name
    :param user_id {int} the user account ID
    :param role {string} the account role of the image uploader
    """
    if role == 'IA':
        ia_account = IndependentAgent.get_agency_by_contact_person(user_id)
        ia_account.update({'avatar_url': avatar_name})
    elif role == 'BR':
        br_account = Broker.get_broker_by_contact_id(user_id)
        br_account.update({'avatar_url': avatar_name})
    return

def update_independent_agent(data, user_id):
    agency = IndependentAgent.get_agency_by_contact_person(user_id=user_id)
    agency_data = {
        "agency_name": verify_updated_details(agency.agency_name, data['org_name']),
        "agency_phone": verify_updated_details(agency.agency_phone, data['org_phone']),
        "agency_email": verify_updated_details(agency.agency_email, data['org_email']),
        "ira_registration_number": data['ira_reg_no'],
        "ira_license_number": data['ira_license_no'],
        "website": data['website'],
        "kra_pin": data['org_kra_pin'],
        "facebook": data['facebook'],
        "instagram": data['instagram'],
        "twitter": data['twitter']
    }
    return agency.update(agency_data)


def update_social_profile(data, user_id, role):
    social_data = {
        "facebook": data['facebook'],
        "twitter": data['twitter'],
        "instagram": data['instagram']
    }
    if role == 'IC':
        agency = InsuranceCompany.get_company_by_contact_person(user_id)
        return agency.update(social_data)
    elif role == 'IA':
        social_data['avatar_url'] = data['avatar_url']
        agency = IndependentAgent.get_agency_by_contact_person(user_id)
        return agency.update(social_data)
    elif role == 'BR':
        social_data['avatar_url'] = data['avatar_url']
        agency = Broker.get_broker_by_contact_id(user_id)
        return agency.update(social_data)
    elif role in ('TA', 'IND'):
        social_data['avatar_url'] = data['avatar_url']
        user = UserProfile.get_profile_by_user_id(user_id)
        user.update(social_data)


def update_broker_agent(data, user_id):
    agency = Broker.get_broker_by_contact_id(user_id=user_id)
    agency_data = {
        "broker_name": verify_updated_details(agency.broker_name, data['org_name']),
        "broker_phone_number": verify_updated_details(agency.broker_phone_number, data['org_phone']),
        "broker_email": verify_updated_details(agency.broker_email, data['org_email']),
        "ira_registration_number": data['ira_reg_no'],
        "ira_license_number": data['ira_license_no'],
        "website": data['website'],
        "kra_pin": data['org_kra_pin']
    }
    return agency.update(agency_data)


def update_insurance_company(data, user_id):
    agency = InsuranceCompany.get_company_by_contact_person(
        user_id)
    agency_data = {
        "bank_account": data['bank_account_number'],
        "company_phone": data['org_phone'],
        "mpesa_paybill": data['mpesa_paybill'],
        "ira_registration_number": data['ira_reg_no'],
        "ira_license_number": data['ira_license_no'],
        "website": data['website'],
        "kra_pin": data['org_kra_pin']
    }
    return agency.update(agency_data)


def verify_updated_details(current_set_data, new_data=None):
    if new_data is None:
        return current_set_data

    return new_data


def block_user_account(account_id):
    """
    block the user account as requested.
    accounts may be blocked by a broker or independent
    agent or sys admin if:
    1) Subscription fees is not duly paid
    2) The agent/broker has willfully blocked a staff account
    """
    user_account = User.get_user_by_id(account_id)
    if user_account:
        deactivate_data = {"is_active": False}
        user_account.update(deactivate_data)
        return True
    
    return False

def update_staff_permissions(staff_id, permissions):
    """
    :param staff_id staff user id
    :param permissions set of user permissions
    """
    curr_permissions = set(UserPermissions.get_permission_by_user_id(staff_id))
    new_permissions = permissions-curr_permissions
    old_permissions = curr_permissions-permissions
    if bool(old_permissions) == True:
        UserPermissions.delete_user_permissions(staff_id, old_permissions)

    for x in new_permissions:
        new_permission = UserPermissions(staff_id, x)
        new_permission.save()
    return True

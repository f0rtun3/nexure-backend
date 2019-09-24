"""
Profile update controller
handles complete profile and profile update
"""
from models.User import User
from models.UserProfile import UserProfile
from models.IndependentAgent import IndependentAgent
from models.InsuranceCompany import InsuranceCompany
from models.Broker import Broker


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
        "birth_date": data['birth_date'],
        "facebook": data['facebook'],
        "twitter": data['twitter'],
        "instagram": data['instagram']
    }
    user_auth_detail = User.get_user_by_id(user_id)
    contact_email = {"email": verify_updated_details(user_auth_detail.email, data['email'])}
    return profile_row.update(personal_data) and user_auth_detail.update(contact_email)


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


def update_independent_agent(data, user_id):
    agency = IndependentAgent.get_agency_by_contact_person(user_id=user_id)
    agency_data = {
        "agency_name": verify_updated_details(agency.agency_name, data['org_name']),
        "agency_phone": verify_updated_details(agency.agency_phone, data['org_phone']),
        "agency_email": verify_updated_details(agency.agency_email, data['org_email']),
        "ira_registration_number": data['ira_reg_no'],
        "ira_licence_number": data['ira_license_no'],
        "kra_pin": data['org_kra_pin']
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
        agency = IndependentAgent.get_agency_by_contact_person(user_id)
        return agency.update(social_data)
    elif role == 'BR':
        agency = Broker.get_broker_by_contact_id(user_id)
        return agency.update(social_data)
    elif role in ('TA', 'IND'):
        user = User.get_user_by_id(user_id)
        user.update(social_data)


def update_broker_agent(data, user_id):
    agency = Broker.get_broker_by_contact_id(user_id=user_id)
    agency_data = {
        "broker_name": verify_updated_details(agency.broker_name, data['org_name']),
        "broker_phone_number": verify_updated_details(agency.broker_phone_number, data['org_phone']),
        "broker_email": verify_updated_details(agency.broker_email, data['org_email']),
        "ira_registration_number": data['ira_reg_no'],
        "ira_licence_number": data['ira_license_no'],
        "website": data['website'],
        "kra_pin": data['org_kra_pin']
    }
    return agency.update(agency_data)


def update_insurance_company(data, user_id):
    agency = InsuranceCompany.get_company_by_contact_person(
        user_id)
    agency_data = {
        "bank_account": data['bank_account_number'],
        "company_phone": data['company_phone'],
        "mpesa_paybill": data['mpesa_paybill'],
        "ira_registration_number": data['ira_reg_no'],
        "ira_licence_number": data['ira_license_no'],
        "website": data['website'],
        "kra_pin": data['org_kra_pin']
    }
    return agency.update(agency_data)


def verify_updated_details(current_set_data, new_data=None):
    if new_data is None:
        return current_set_data

    return new_data

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
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "gender": data['gender'],
        "occupation": data['occupation'],
        "id_passport": data['id_passport'],
        "kra_pin": data['kra_pin'],
        "phone": data['mob'],
        "birth_date": data['birth_date'],
        "facebook": verify_updated_details(profile_row.facebook, data['facebook']),
        "twitter": verify_updated_details(profile_row.twitter, data['twitter']),
        "instagram": verify_updated_details(profile_row.instagram, data['instagram'])
    }
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
        return False

def complete_user_profile(data, user_id, role):
    if update_personal_details(data, user_id) and\
        update_location_details(data, user_id) and\
        update_agency_details(data, role, user_id):
        return True

    return False

def update_independent_agent(data, user_id):
    agency = IndependentAgent.get_agency_by_contact_person(user_id=user_id)
    agency_data = {
        "agency_name": data['org_name'],
        "agency_phone": verify_updated_details(agency.agency_phone, data['org_phone']),
        "agency_email": verify_updated_details(agency.agency_email, data['org_email']),
        "ira_registration_number": data['ira_reg_no'],
        "ira_license_number": data['ira_license_no'],
        "kra_pin": data['org_kra_pin'],
        "website": data['website'],
        "facebook": data['facebook'],
        "instagram": data['instagram'],
        "twitter": data['twitter']
    }
    return agency.update(agency_data)

def update_broker_agent(data, user_id):
    agency = Broker.get_broker_by_contact_id(user_id=user_id)
    agency_data = {
        "broker_name": data['org_name'],
        "broker_phone_number": verify_updated_details(agency.broker_phone_number, data['org_phone']),
        "broker_email": verify_updated_details(agency.broker_email, data['org_email']),
        "ira_registration_number": data['ira_reg_no'],
        "ira_license_number": data['ira_license_no'],
        "kra_pin": data['org_kra_pin'],
        "website": data['website'],
        "facebook": data['facebook'],
        "instagram": data['twitter'],
        "twitter": data['instagram']
    }
    return agency.update(agency_data)

def update_insurance_company(data, user_id):
    agency = InsuranceCompany.get_company_by_contact_person(
        user_id)
    agency_data = {
        "bank_account": data['bank_account_number'],
        "company_phone": verify_updated_details(agency.company_phone, data['company_phone']),
        "mpesa_paybill": data['mpesa_paybill'],
        "ira_registration_number": data['ira_reg_no'],
        "ira_license_number": data['ira_license_no'],
        "kra_pin": data['org_kra_pin'],
        "website": data['website'],
        "facebook": data['facebook'],
        "instagram": data['instagram'],
        "twitter": data['twitter']
    }
    return agency.update(agency_data)

def verify_updated_details(current_set_data, new_data = None):
    if new_data is None:
        return current_set_data

    return new_data

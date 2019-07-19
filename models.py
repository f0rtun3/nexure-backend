from app import db
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    User authentication details
    """
    __tablename__ = 'user'

    # we need to identify the user whose authentication
    # details is stored
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # for exposing data, we'll user a uuid
    user_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    # user email for login and all subsequent communication to the same
    email = db.Column(db.String(100), unique=True)
    # authentication field for login
    password = db.Column(db.String(255), nullable=False)
    # an account, once created must be activated by the user
    # through an email sent
    is_active = db.Column(db.Boolean, default=False)
    # define the relationship to user_profile
    # this allows us access the generated user uuid for exposure
    user_profile = db.relationship("UserProfile", backref="user")
    # define the relationship to the individual customer
    individual_customer = db.relationship("IndividualCustomer", backref="user")
    # define the relationship to the organization customer
    organization_customer = db.relationship(
        "OrganizationCustomer", backref="user")
    # define the relationship to the tied agent
    tied_agent = db.relationship("TiedAgents", backref="user")
    # define the relationship to the independent agent
    independent_agent = db.relationship("IndependentAgent", backref="user")
    # define the relationship to the insurance company
    insurance_company = db.relationship("InsuranceCompany", backref="user")
    # define the relationship to the broker
    broker = db.relationship("Broker", backref="user")
    # define the relationship to the staff
    staff = db.relationship("Staff", backref="user")

    def __init__(self, user_id, email, password):
        self.user_id = user_id
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"{self.email}"

    @staticmethod
    def generate_password_hash(password):
        return generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "email": self.email
        }, 200

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def update_password(self, password):
        setattr(self, "password", password)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    # for normal indexing
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # we need to know user whose profile we are storing
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1))
    # we need to store the user mobile number
    # for subsequent communication
    phone = db.Column(db.BIGINT, unique=True)
    avatar_url = db.Column(db.String(150))
    occupation = db.Column(db.String(100))
    id_passport = db.Column(db.String(30), unique=True)
    kra_pin = db.Column(db.String(15), unique=True)
    birth_date = db.Column(db.Date)
    physical_address = db.Column(db.String(100))
    postal_code = db.Column(db.Integer)
    postal_town = db.Column(db.String(30))
    county = db.Column(db.String(30))
    constituency = db.Column(db.String(30))
    ward = db.Column(db.String(30))

    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, user_id, first_name, last_name, phone, gender=None, avatar_url=None, occupation=None,
                 id_passport=None, kra_pin=None, birth_date=None, physical_address=None, postal_code=None,
                 postal_town=None, county=None, constituency=None, ward=None, facebook=None, twitter=None,
                 instagram=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.gender = gender
        self.avatar_url = avatar_url
        self.occupation = occupation
        self.id_passport = id_passport
        self.kra_pin = kra_pin
        self.birth_date = birth_date
        self.physical_address = physical_address
        self.postal_code = postal_code
        self.postal_town = postal_town
        self.county = county
        self.constituency = constituency
        self.ward = ward
        self.facebook = facebook
        self.twitter = twitter
        self.instagram = instagram

    def __repr__(self):
        return f"{self.id_passport}"

    def serialize(self):
        return {
            "user_id": self.user.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "phone": self.phone,
            "avatar_url": self.avatar_url,
            "occupation": self.occupation,
            "id_passport": self.id_passport,
            "kra_pin": self.kra_pin,
            "birth_date": self.birth_date,
            "physical_address": self.physical_address,
            "postal_code": self.postal_code,
            "postal_town": self.postal_town,
            "county": self.county,
            "constituency": self.constituency,
            "ward": self.ward,
            "facebook": self.facebook,
            "twitter": self.twitter,
            "instagram": self.instagram,
            "created_on": self.created_on,
            "updated_on": self.updated_on
        }, 200

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.flush()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_profiles(cls):
        all_profiles = [user.serialize() for user in cls.query.all()]
        return all_profiles

    @classmethod
    def get_profile_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()


class Roles(db.Model):
    """
    Pre defined list of roles in nexure for permission throttling
    """
    __tablename__ = 'role'

    # the role name will help us know what permissions to grant the user
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    role_name = db.Column(db.String(3), nullable=False)
    # define the relationship to the user role placement
    user_role = db.relationship("UserRolePlacement", backref="role")
    # define the relationship to the customer affiliations
    customer_affiliation = db.relationship(
        "CustomerAffiliation", backref="role")

    def __init__(self, role_name):
        self.role_name = role_name

    def __repr__(self):
        return f"{self.role_name}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def fetch_all_roles(cls):
        role_rows = cls.query.all()
        roles = [{
            "role_name": role.role_name
        } for role in role_rows]

        return roles

    @classmethod
    def fetch_role_by_id(cls, id):
        # Get user role by name
        role_row = cls.query.filter_by(id=id).first()
        return role_row.role_name

    @classmethod
    def fetch_role_by_name(cls, name):
        # Get user role by name
        role_row = cls.query.filter_by(role_name=name).first()
        return role_row.id


class Permissions(db.Model):

    __tablename__ = 'permission'
    #  stores the list of permissions
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    permission_name = db.Column(db.String(100))
    user_permission = db.Relationship('UserPermissions', backref='permissions')

    def __init__(self, permission_name, user_id):
        self.permission_name = permission_name
        self.user_id = user_id

    def __str__(self):
        return f"{self.id}"


class UserPermissions(db.Model):
    __tablename__ = 'user_permission'

    id = db.Columbn(db.Integer, primary_key=True, auto_increment=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', onupdate='CASCADE', ondelete='CASCADE'))
    permission_id = db.Column(db.Integer, db.ForeignKey(
        'permissions.id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, user_id, permission_id):
        self.user_id = user_id
        self.permission_id = permission_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    @classmethod
    def get_permission_by_id(cls, id):
        permissions_list = cls.query.filter_by(user_id=id).all()
        permission_ids = []
        for i in permissions_list:
            permission_ids.append(str(i.permission_id))
        return ''.join(permission_ids)

class UserRolePlacement(db.Model):
    """
    Place users to a specified role
    """
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', onupdate='CASCADE', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey(
        'role.id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return f"{self.user_id}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def fetch_role_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()


class Broker(db.Model):
    broker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    broker_name = db.Column(db.String(100), unique=True, nullable=False)
    broker_phone_number = db.Column(db.BIGINT, nullable=False, unique=True)
    broker_email = db.Column(db.String(100), nullable=False, unique=True)
    contact_person = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'),
                               nullable=False)
    ira_registration_number = db.Column(db.String(15), unique=True)
    ira_license_number = db.Column(db.String(15), unique=True)
    kra_pin = db.Column(db.String(15), unique=True)
    website = db.Column(db.String(150), unique=True)
    mpesa_paybill = db.Column(db.BIGINT, nullable=False)

    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    avatar_url = db.Column(db.String(150))

    def __init__(self, broker_name, broker_phone_number, broker_email, contact_person, ira_registration_number=None,
                 ira_licence_number=None, kra_pin=None, website=None, facebook=None, instagram=None, twitter=None,
                 avatar_url=None, mpesa_paybill=None):
        self.broker_name = broker_name
        self.broker_email = broker_email
        self.broker_phone_number = broker_phone_number
        self.contact_person = contact_person
        self.ira_registration_number = ira_registration_number
        self.ira_license_number = ira_licence_number
        self.kra_pin = kra_pin
        self.website = website
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter
        self.avatar_url = avatar_url
        self.mpesa_paybill = mpesa_paybill

    def __repr__(self):
        return f"{self.broker_name}"

    def serializers(self):
        return {
            "broker_name": self.broker_name,
            "contact_person": self.contact_person,
            "broker_phone_number": self.broker_phone_number,
            "broker_email": self.broker_email,
            "ira_registration_number": self.ira_registration_number,
            "ira_license_number": self.ira_license_number,
            "kra_pin": self.kra_pin,
            "website": self.website,
            "facebook": self.facebook,
            "instagram": self.instagram,
            "twitter": self.twitter
        }, 200

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_brokers(cls):
        broker_rows = cls.query.all()
        brokers = [{
            "broker_name": broker.broker_name,
            "contact_person": broker.contact_person,
            "broker_phone_number": broker.broker_phone_number,
            "broker_email": broker.broker_email,
            "ira_registration_number": broker.ira_registration_number,
            "ira_license_number": broker.ira_license_number,
            "kra_pin": broker.kra_pin,
            "website": broker.website,
            "facebook": broker.facebook,
            "instagram": broker.instagram,
            "twitter": broker.twitter
        } for broker in broker_rows]

        return brokers

    @classmethod
    def get_broker_by_id(cls, broker_id):
        return cls.query.filter_by(broker_id=broker_id).first()

    @classmethod
    def get_broker_by_contact_id(cls, user_id):
        return cls.query.filter_by(contact_person=user_id).first()


class InsuranceCompany(db.Model):
    insurance_company_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    company_name = db.Column(db.String(100), unique=True, nullable=False)
    contact_person = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'))
    company_phone = db.Column(db.BIGINT, unique=True, nullable=False)
    company_email = db.Column(db.String(100), nullable=False, unique=True)
    ira_registration_number = db.Column(db.String(15), unique=True)
    ira_license_number = db.Column(db.String(15), unique=True)
    kra_pin = db.Column(db.String(15), unique=True)
    website = db.Column(db.String(150), unique=True)
    bank_account = db.Column(db.BIGINT, nullable=True)
    mpesa_paybill = db.Column(db.BIGINT, nullable=True, unique=True)

    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    avatar_url = db.Column(db.String(150))

    def __init__(self, company_name, company_email, company_phone, contact_person, ira_registration_number=None,
                 ira_licence_number=None, kra_pin=None, website=None, facebook=None, instagram=None, twitter=None,
                 avatar_url=None, mpesa_paybill=None):
        self.company_name = company_name
        self.company_email = company_email
        self.company_phone = company_phone
        self.contact_person = contact_person
        self.ira_registration_number = ira_registration_number
        self.ira_license_number = ira_licence_number
        self.kra_pin = kra_pin
        self.website = website
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter
        self.avatar_url = avatar_url
        self.mpesa_paybill = mpesa_paybill

    def __repr__(self):
        return f"{self.company_name}"

    def serialize(self):
        return{
            "company_name": self.company_name,
            "contact_person": self.contact_person,
            "company_number": self.company_number,
            "company_email": self.company_email,
            "bank_account": self.bank_account,
            "mpesa_paybill": self.mpesa_paybill,
            "ira_registration_number": self.ira_registration_number,
            "ira_license_number": self.ira_license_number,
            "kra_pin": self.kra_pin,
            "website": self.website,
            "facebook": self.facebook,
            "instagram": self.instagram,
            "twitter": self.twitter
        }, 200

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_company_by_id(cls, insurance_company_id):
        return cls.query.filter_by(insurance_company_id=insurance_company_id).first()

    @classmethod
    def get_company_by_contact_person(cls, user_id):
        return cls.filter_by(contact_person=user_id).first()

    @classmethod
    def get_all_companies(cls):
        company_rows = cls.query.all()
        companies = [{
            "company_name": company.company_name,
            "contact_person": company.contact_person,
            "company_number": company.company_number,
            "company_email": company.company_email,
            "ira_registration_number": company.ira_registration_number,
            "ira_license_number": company.ira_license_number,
            "kra_pin": company.kra_pin,
            "website": company.website,
            "facebook": company.facebook,
            "instagram": company.instagram,
            "twitter": company.twitter
        } for company in company_rows]

        return companies


class IndependentAgent(db.Model):
    """
    Independent agent
    """
    __tablename__ = 'independent_agent'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    agency_name = db.Column(db.String(100), nullable=False)
    agency_phone = db.Column(db.BIGINT, nullable=False, unique=True)
    agency_email = db.Column(db.String(100), nullable=False, unique=True)
    contact_person = db.Column(db.Integer, db.ForeignKey(
        'user.id', onupdate='CASCADE', ondelete='CASCADE'))
    ira_registration_number = db.Column(db.String(15))
    ira_licence_number = db.Column(db.String(15))
    kra_pin = db.Column(db.String(15))
    mpesa_paybill = db.Column(db.BIGINT, nullable=True, unique=True)
    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    avatar_url = db.Column(db.String(150))

    def __repr__(self):
        return f"{self.agency_name}"

    def __init__(self, agency_name, agency_phone, agency_email, contact_person, ira_registration_number=None,
                 ira_licence_number=None, kra_pin=None, website=None, facebook=None, instagram=None, twitter=None,
                 avatar_url=None, mpesa_paybill=None):
        self.agency_name = agency_name
        self.agency_email = agency_email
        self.agency_phone = agency_phone
        self.contact_person = contact_person
        self.ira_registration_number = ira_registration_number
        self.ira_license_number = ira_licence_number
        self.kra_pin = kra_pin
        self.website = website
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter
        self.avatar_url = avatar_url
        self.mpesa_paybill = mpesa_paybill

    def serialize(self):
        return {
            "agency_name": self.agency_name,
            "agency_email": self.agency_email,
            "agency_phone": self.agency_phone,
            "contact_person": self.contact_person,
            "ira_registration_number": self.ira_registration_number,
            "ira_licence_number": self.ira_licence_number,
            "kra_pin": self.kra_pin,
            "facebook": self.facebook,
            "instagram": self.instagram,
            "twitter": self.twitter
        }, 200

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_agencies(cls):
        agency_rows = cls.query.all()
        agencies = [{
            "agency_name": agency.agency_name,
            "contact_person": agency.contact_person,
            "agency_email": agency.agency_email,
            "agency_phone": agency.agency_phone,
            "ira_registration_number": agency.ira_registration_number,
            "ira_licence_number": agency.ira_licence_number,
            "kra_pin": agency.kra_pin,
            "facebook": agency.facebook,
            "instagram": agency.instagram,
            "twitter": agency.twitter
        } for agency in agency_rows]

        return agencies

    @classmethod
    def get_agency_by_id(cls, agency_id):
        return cls.query.filter_by(id=agency_id).first()

    @classmethod
    def get_agency_by_contact_person(cls, user_id):
        return cls.filter_by(contact_person=user_id).first()


class TiedAgents(db.Model):
    """
    Tied Agents model
    """
    __tablename__ = 'tied_agent'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # The tied agent is linked to a user profile since they have common details
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"{self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
        }, 200

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_tied_agents(cls):
        tied_agents_rows = cls.query.all()
        tied_agents = [{
            "id": agent.id,
            "user": agent.user
        } for agent in tied_agents_rows]

        return tied_agents

    @classmethod
    def get_tied_agent_by_id(cls, agent_id):
        return cls.query.filter_by(id=agent_id).first()


class IndividualCustomer(db.Model):
    """
    Individual customer user
    linked to the UserProfile
    """
    # ToDo: Serialize the individual customer data
    __tablename__ = 'individual_customer'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'))
    salutation = db.Column(db.String(4), nullable=False)
    # customer_number = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"{self.user}"

    def __init__(self, user_id, salutation):
        self.user_id = user_id
        self.salutation = salutation
        # self.customer_number = customer_number

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class OrganizationCustomer(db.Model):
    """
    Organization Customer
    """
    __tablename__ = 'organization_customer'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    org_type = db.Column(db.String(100), nullable=False)
    # org_customer_number = db.Column(db.String(50), unique=True, nullable=True)
    org_name = db.Column(db.String(100), unique=True)
    org_phone = db.Column(db.BIGINT)
    org_email = db.Column(db.String(100))
    org_registration_number = db.Column(db.String(50))
    physical_address = db.Column(db.String(100))
    postal_code = db.Column(db.Integer)
    postal_town = db.Column(db.String(30))
    county = db.Column(db.String(30))
    constituency = db.Column(db.String(30))
    ward = db.Column(db.String(30))
    # organization contact person details
    contact_person = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'))
    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, org_type, org_name, org_phone, email, org_registration_number, physical_address,
                 postal_code, postal_town, county, facebook, instagram, twitter, constituency,
                 ward, contact_person):
        self.org_type = org_type
        self.org_name = org_name
        self.org_phone = org_phone
        self.email = email
        self.org_registration_number = org_registration_number
        # self.org_customer_number = org_customer_number
        self.physical_address = physical_address
        self.postal_code = postal_code
        self.postal_town = postal_town
        self.county = county
        self.constituency = constituency
        self.ward = ward
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter
        self.contact_person = contact_person

    def __repr__(self):
        return f"{self.org_name}"

    def serialize(self):
        return {
            "org_customer_number": self.org_customer_number,
            "org_type": self.org_type,
            "org_name": self.org_name,
            "org_phone": self.org_phone,
            "email": self.email,
            "org_registration_number": self.org_registration_number,
            "physical_address": self.physical_address,
            "postal_code": self.postal_code,
            "postal_town": self.postal_town,
            "county": self.county,
            "constituency": self.constituency,
            "ward": self.ward,
            "contact_first_name": self.user.user_profile.first_name,
            "contact_last_name": self.user.user_profile.last_name,
            "contact_phone_number": self.user.user_profile.phone,
            "contact_email": self.user.user_profile.email,
            "facebook": self.facebook,
            "instagram": self.instagram,
            "twitter": self.twitter
        }, 200

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_organization_by_id(cls, org_id):
        return cls.query.filter_by(id=org_id).first()

    @classmethod
    def get_organization_by_number(cls, org_number):
        return cls.query.filter_by(org_customer_number=org_number).first()

    @classmethod
    def get_all_organization_customers(cls):
        results = [org.serialize() for org in cls.query.all()]
        return results


class OrganizationTypes(db.Model):
    """
    Holds the customer organization types
    """
    __tablename__ = 'organization_type'

    id = db.Column(db.Integer, autoincrement=True,
                   nullable=False, primary_key=True)
    type_name = db.Column(db.String(20), nullable=False, unique=True)
    type_acronym = db.Column(db.String(5), nullable=False, unique=True)

    def __init__(self, type_name, type_acronym):
        self.type_name = type_name
        self.type_acronym = type_acronym

    def serialize(self):
        return {
            "label": self.type_name,
            "value": self.type_acronym
        }, 200

    def save(self):
        db.session.add(self)
        db.session.comit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_organization_customer_types(cls):
        all_types = [types.serialize() for types in cls.query.all()]
        return all_types


class CustomerAffiliation(db.Model):
    """
    Create an affiliation between the customer and the agent or broker
    """
    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    customer_number = db.Column(db.String(50), unique=True, nullable=True)
    broker_agent_id = db.Column(db.Integer, nullable=False)
    staff_id = db.Column(db.Integer, nullable=True)
    date_affiliated = db.Column(db.DateTime, default=db.func.now())
    # we need to know whether the affiliation is active or not
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, customer_number, broker_agent_id, staff_id=None):
        self.customer_number = customer_number
        self.broker_agent_id = broker_agent_id
        self.staff_id = staff_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def filter_agent_broker(cls, role_id, broker_agent_id):
        agent_broker_data = cls.query.filter_by(
            broker_agent_id=broker_agent_id).all()
        return agent_broker_data


class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True, auto_increment=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    agent_broker_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, user_id, agent_broker_id):
        self.user_id = user_id
        self.agent_broker_id = agent_broker_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()    
    
    @classmethod
    def fetch_staff_by_id(cls, id):
        return cls.query.filter_by(user_id=id).first()
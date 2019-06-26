from app import db
from sqlalchemy.dialects.postgresql import UUID


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

    def __init__(self, user_id, email, password):
        self.user_id = user_id
        self.email = email
        self.password = password

    def __repr__(self):
        return f"{self.email}"

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
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
    address_line_1 = db.Column(db.String(100))
    address_line_2 = db.Column(db.String(100))
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
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, user_id, first_name, last_name, phone):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        """
        self.user_id = user_id
        self.gender = gender
        self.avatar_url = avatar_url
        self.occupation = occupation
        self.id_passport = id_passport
        self.kra_pin = kra_pin
        self.birth_date = birth_date
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.postal_code = postal_code
        self.postal_town = postal_town
        self.county = county
        self.constituency = constituency
        self.ward = ward
        self.facebook = facebook
        self.twitter = twitter
        self.instagram = instagram
        """

    def __repr__(self):
        return f"{self.id_passport}"

    def serialize(self):
        return {
           "user_id": self.user_id,
           "first_name": self.first_name,
           "last_name": self.last_name,
           "gender": self.gender,
           "phone": self.phone,
           "avatar_url": self.avatar_url,
           "occupation": self.occupation,
           "id_passport": self.id_passport,
           "kra_pin": self.kra_pin,
           "birth_date": self.birth_date,
           "address_line_1": self.address_line_1,
           "address_line_2": self.address_line_2,
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
        """
        profiles = cls.query.all()
        all_profiles = [{
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "gender": user.gender,
            "phone": user.phone,
            "avatar_url": user.avatar_url,
            "occupation": user.occupation,
            "id_passport": user.id_passport,
            "kra_pin": user.kra_pin,
            "birth_date": user.birth_date,
            "address_line_1": user.address_line_1,
            "address_line_2": user.address_line_2,
            "postal_code": user.postal_code,
            "postal_town": user.postal_town,
            "county": user.county,
            "constituency": user.constituency,
            "ward": user.ward,
            "facebook": user.facebook,
            "twitter": user.twitter,
            "instagram": user.instagram,
            "created_on": user.created_on,
            "updated_on": user.updated_on
        } for user in profiles]
        """
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
    role_name = db.Column(db.String(2), nullable=False)

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
    def fetch_role_by_name(cls, name):
        role_row = cls.query.filter_by(role_name=name).first()
        return role_row.id


class UserRolePlacement(db.Model):
    """
    Place users to a specified role
    """
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', onupdate='CASCADE', ondelete='CASCADE'))

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
    broker_phone_number = db.Column(db.Integer, nullable=False, unique=True)
    broker_email = db.Column(db.String(100), nullable=False, unique=True)
    b_contact_person = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'),
                                 nullable=False)
    b_contact_number = db.Column(db.Integer, unique=True, nullable=False)
    b_contact_email = db.Column(db.String(100), unique=True, nullable=False)
    ira_registration_number = db.Column(db.String(15), unique=True)
    ira_license_number = db.Column(db.String(15), unique=True)
    kra_pin = db.Column(db.String(15), unique=True)
    website = db.Column(db.String(150), unique=True)

    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    avatar_url = db.Column(db.String(150))

    def __init__(self, broker_name, b_contact_person, b_contact_number, b_contact_email):
        self.broker_name = broker_name
        self.b_contact_person = b_contact_person
        self.b_contact_number = b_contact_number
        self.b_contact_email = b_contact_email
        """
        self.ira_registration_number = ira_registration_number
        self.ira_license_number = ira_license_number
        self.kra_pin = kra_pin
        self.website = website
        """

    def __repr__(self):
        return f"{self.broker_name}"

    def serializers(self):
        return {
            "broker_name":self.broker_name,
            "b_contact_person":self.b_contact_person,
            "b_contact_number":self.b_contact_number,
            "b_contact_email":self.b_contact_email,
            "ira_registration_number":self.ira_registration_number,
            "ira_license_number":self.ira_license_number,
            "kra_pin":self.kra_pin,
            "website":self.website
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
            "b_contact_person": broker.b_contact_person,
            "b_contact_number": broker.b_contact_number,
            "b_contact_email": broker.b_contact_email,
            "ira_registration_number": broker.ira_registration_number,
            "ira_license_number": broker.ira_license_number,
            "kra_pin": broker.kra_pin,
            "website": broker.website
        } for broker in broker_rows]

        return brokers

    @classmethod
    def get_broker_by_id(cls, broker_id):
        return cls.query.filter_by(broker_id=broker_id).first()


class InsuranceCompany(db.Model):
    insurance_company_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_name = db.Column(db.String(100), unique=True, nullable=False)
    contact_person = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    contact_first_name = db.Column(db.String(50), nullable=False)
    contact_last_name = db.Column(db.String(50), nullable=False)
    contact_phone = db.Column(db.Integer, nullable=False)
    company_phone = db.Column(db.Integer, unique=True, nullable=False)
    company_email = db.Column(db.String(100), nullable=False, unique=True)
    ira_registration_number = db.Column(db.String(15), unique=True)
    ira_license_number = db.Column(db.String(15), unique=True)
    kra_pin = db.Column(db.String(15), unique=True)
    website = db.Column(db.String(150), unique=True)

    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    avatar_url = db.Column(db.String(150))

    def __init__(self, company_name, company_email, company_phone, contact_person, contact_first_name,
                 contact_last_name, contact_phone):
        self.company_name = company_name
        self.company_email = company_email
        self.company_phone = company_phone
        self.contact_person = contact_person
        self.contact_first_name = contact_first_name
        self.contact_last_name = contact_last_name
        self.contact_phone = contact_phone

    def __repr__(self):
        return f"{self.company_name}"

    def serialize(self):
        return{
          "company_name": self.company_name,
          "c_contact_person": self.c_contact_person,
          "company_number": self.company_number,
          "company_email": self.company_email,
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
        cls.query.filter_by(insurance_company_id=insurance_company_id).first()

    @classmethod
    def get_all_companies(cls):
        company_rows = cls.query.all()
        companies = [{
            "company_name": company.company_name,
            "c_contact_person": company.c_contact_person,
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
    agency_phone = db.Column(db.Integer, nullable=False, unique=True)
    agency_email = db.Column(db.String(100), nullable=False, unique=True)
    contact_person = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    contact_first_name = db.Column(db.String(50), nullable=False)
    contact_last_name = db.Column(db.String(50), nullable=False)
    contact_phone = db.Column(db.Integer, nullable=False)
    ira_registration_number = db.Column(db.String(15))
    ira_licence_number = db.Column(db.String(15))
    kra_pin = db.Column(db.String(15))

    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    avatar_url = db.Column(db.String(150))

    def __repr__(self):
        return f"{self.agency_name}"

    def __init__ (self, agency_name, agency_phone, agency_email, contact_person, contact_first_name, contact_last_name,
                  contact_phone):
        self.agency_name = agency_name
        self.agency_email = agency_email
        self.agency_phone = agency_phone
        self.contact_person = contact_person
        self.contact_phone = contact_phone
        self.contact_first_name = contact_first_name
        self.contact_last_name = contact_last_name

    def serialize(self):
        return {
            "agency_name": self.agency_name,
            "contact_person": self.contact_person,
            "contact_phone": self.contact_phone,
            "contact_first_name": self.contact_first_name,
            "contact_last_name": self.contact_last_name,
            "ira_registration_number": self.ira_registration_number,
            "ira_licence_number": self.ira_licence_number,
            "kra_pin": self.kra_pin
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
            "a_contact_person": agency.a_contact_person,
            "a_contact_number": agency.a_contact_number,
            "a_contact_email": agency.a_contact_email,
            "ira_registration_number": agency.ira_registration_number,
            "ira_licence_number": agency.ira_licence_number,
            "kra_pin": agency.kra_pin
        } for agency in agency_rows]

        return agencies

    @classmethod
    def get_agency_by_id(cls, agency_id):
        return cls.query.filter_by(id=agency_id).first()


class TiedAgents(db.Model):
    """
    Tied Agents model
    """
    __tablename__ = 'tied_agent'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # we need to know user whose profile we are storing
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1))
    # we need to store the user mobile number
    # for subsequent communication
    phone = db.Column(db.Integer, unique=True, nullable=False)
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
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, first_name, last_name, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

    def __repr__(self):
        return f"{self.id_passport}"

    def serialize(self):
        return {
           "id": self.id,
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
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "gender": user.gender,
            "phone": user.phone,
            "avatar_url": user.avatar_url,
            "occupation": user.occupation,
            "id_passport": user.id_passport,
            "kra_pin": user.kra_pin,
            "birth_date": user.birth_date,
            "physical_address": user.physical_address,
            "postal_code": user.postal_code,
            "postal_town": user.postal_town,
            "county": user.county,
            "constituency": user.constituency,
            "ward": user.ward,
            "facebook": user.facebook,
            "twitter": user.twitter,
            "instagram": user.instagram,
            "created_on": user.created_on,
            "updated_on": user.updated_on
        } for user in tied_agents_rows]

        return tied_agents

    @classmethod
    def get_tied_agent_by_id(cls, agent_id):
        return cls.query.filter_by(user_id=agent_id).first()


class IndividualCustomer(db.Model):
    """
    Individual customer user
    linked to the UserProfile
    """
    __tablename__ = 'individual_customer'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    customer_number = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"{self.user}"

    def __init__(self, user):
        self.user = user

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
    org_customer_number = db.Column(db.String(50), unique=True)
    org_name = db.Column(db.String(100), unique=True)
    org_phone = db.Column(db.Integer)
    email = db.Column(db.String(100))
    org_registration_number = db.Column(db.String(50))
    physical_address = db.Column(db.String(100))
    postal_code = db.Column(db.Integer)
    postal_town = db.Column(db.String(30))
    county = db.Column(db.String(30))
    constituency = db.Column(db.String(30))
    ward = db.Column(db.String(30))

    # organization contact person details
    """
    contact_first_name = db.Column(db.String(50))
    contact_last_name = db.Column(db.String(50))
    contact_phone_number = db.column(db.Integer)
    contact_email = db.Column(db.String(100))
    """
    contact_person = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))

    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, org_customer_number, org_name, org_phone, email, org_registration_number, physical_address,
                 postal_code, postal_town, county, constituency, ward, contact_person, facebook, instagram, twitter):
        self.org_customer_number = org_customer_number
        self.org_name = org_name
        self.org_phone = org_phone
        self.email = email
        self.org_registration_number = org_registration_number
        self.physical_address = physical_address
        self.postal_code = postal_code
        self.postal_town = postal_town
        self.county = county
        self.constituency = constituency
        self.ward = ward
        """
        self.contact_first_name = contact_first_name
        self.contact_last_name = contact_last_name
        self.contact_phone_number = contact_phone_number
        self.contact_email = contact_email
        """
        self.contact_person = contact_person
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter

    def __repr__(self):
        return f"{self.org_name}"

    def serialize(self):
        return {
             "org_customer_number" : self.org_customer_number,
             "org_name" : self.org_name,
             "org_phone" : self.org_phone,
             "email" : self.email,
             "org_registration_number" : self.org_registration_number,
             "physical_address" : self.physical_address,
             "postal_code" : self.postal_code,
             "postal_town" : self.postal_town,
             "county" : self.county,
             "constituency" : self.constituency,
             "ward" : self.ward,
             "contact_first_name" : self.contact_first_name,
             "contact_last_name" : self.contact_last_name,
             "contact_phone_number" : self.contact_phone_number,
             "contact_email" : self.contact_email,
             "facebook" : self.facebook,
             "instagram" : self.instagram,
             "twitter" : self.twitter
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
        organization_customer_rows = cls.query.all()
        organizations = [{
            "org_customer_number": organization.org_customer_number,
            "org_name": organization.org_name,
            "org_phone": organization.org_phone,
            "email": organization.email,
            "org_registration_number": organization.org_registration_number,
            "physical_address": organization.physical_address,
            "postal_code": organization.postal_code,
            "postal_town": organization.postal_town,
            "county": organization.county,
            "constituency": organization.constituency,
            "ward": organization.ward,
            "contact_first_name": organization.contact_first_name,
            "contact_last_name": organization.contact_last_name,
            "contact_phone_number": organization.contact_phone_number,
            "contact_email": organization.contact_email,
            "facebook": organization.facebook,
            "instagram": organization.instagram,
            "twitter": organization.twitter
        } for organization in organization_customer_rows]

        return organizations

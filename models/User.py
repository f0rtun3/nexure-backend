from database.db import db
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
    user_profile = db.relationship("UserProfile", backref="user", uselist=False)
    # define the relationship to the individual customer
    individual_customer = db.relationship("IndividualCustomer", backref="user")
    # define the relationship to the organization customer
    organization_customer = db.relationship("OrganizationCustomer", backref="user")
    # define the relationship to the tied agent
    tied_agent = db.relationship("TiedAgents", backref="user")
    # define the relationship to the independent agent
    independent_agent = db.relationship("IndependentAgent", backref="user")
    # define the relationship to the insurance company
    insurance_company = db.relationship("InsuranceCompany", backref="user")
    # define the relationship to the broker
    broker = db.relationship("Broker", backref="user")
    # define the relationship to broker staff members
    br_staff = db.relationship("BRStaff", backref="br_staff_member")
    ta_staff = db.relationship("TAStaff", backref="ta_staff_member")
    ia_staff = db.relationship("IAStaff", backref="ia_staff_member")

    def __init__(self, user_id, email, password):
        self.user_id = user_id
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"{self.email}"

    def serialize(self):
        return self.user_profile.serialize()

    @staticmethod
    def generate_password_hash(password):
        return generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

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

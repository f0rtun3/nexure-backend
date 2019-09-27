from database.db import db


class OrganizationCustomer(db.Model):
    """
    Organization Customer
    """
    __tablename__ = 'organization_customer'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    customer_number = db.Column(db.String(50))
    org_type = db.Column(db.String(100), nullable=False)
    org_name = db.Column(db.String(100), unique=True)
    org_phone = db.Column(db.BIGINT)
    org_email = db.Column(db.String(100))
    org_reg_number = db.Column(db.String(50))
    physical_address = db.Column(db.String(150))
    postal_address = db.Column(db.String(100))
    postal_code = db.Column(db.Integer)
    postal_town = db.Column(db.String(30))
    county = db.Column(db.String(30))
    constituency = db.Column(db.String(30))
    ward = db.Column(db.String(30))
    # organization contact person details
    contact_person = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, org_type, org_name, org_phone, org_email, org_reg_number, physical_address, postal_address,
                 postal_code, postal_town, county, constituency, ward, facebook, instagram, twitter, contact_person,
                 customer_number):
        self.org_type = org_type
        self.org_name = org_name
        self.org_phone = org_phone
        self.org_email = org_email
        self.org_reg_number = org_reg_number
        self.physical_address = physical_address
        self.postal_address = postal_address
        self.postal_code = postal_code
        self.postal_town = postal_town
        self.county = county
        self.constituency = constituency
        self.ward = ward
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter
        self.contact_person = contact_person
        self.customer_number = customer_number

    def __repr__(self):
        return f"{self.org_name}"

    def serialize(self):
        return {
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

    @classmethod
    def get_customer_by_contact(cls, uid):
        return cls.query.filter_by(contact_person=uid).first()

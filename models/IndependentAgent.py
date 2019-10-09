from database.db import db


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
    ira_license_number = db.Column(db.String(15))
    kra_pin = db.Column(db.String(15))
    mpesa_paybill = db.Column(db.BIGINT, nullable=True, unique=True)
    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    website = db.Column(db.String(150), unique=True)
    avatar_url = db.Column(db.String(150))
    ia_customer = db.relationship("IACustomer", backref="ia_affiliation")

    def __repr__(self):
        return f"{self.agency_name}"

    def __init__(self, agency_name, agency_phone, agency_email, contact_person, ira_registration_number=None,
                 ira_license_number=None, kra_pin=None, website=None, facebook=None, instagram=None, twitter=None,
                 avatar_url=None, mpesa_paybill=None):
        self.agency_name = agency_name
        self.agency_email = agency_email
        self.agency_phone = agency_phone
        self.contact_person = contact_person
        self.ira_registration_number = ira_registration_number
        self.ira_license_number = ira_license_number
        self.kra_pin = kra_pin
        self.website = website
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter
        self.avatar_url = avatar_url
        self.mpesa_paybill = mpesa_paybill

    def serialize(self):
        org_details = {
            "organization": {
                "org_name": self.agency_name,
                "org_email": self.agency_email,
                "org_phone": self.agency_phone,
                "ira_registration_number": self.ira_registration_number,
                "ira_license_number": self.ira_license_number,
                "org_kra_pin": self.kra_pin,
                "website": self.website
            }
        }
        user_profile = self.user.serialize()
        user_profile['social_media']['facebook'] = self.facebook
        user_profile['social_media']['twitter'] = self.twitter
        user_profile['social_media']['instagram'] = self.instagram
        org_details.update(user_profile)

        return org_details

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
            "org_name": agency.agency_name,
            "org_person": agency.contact_person,
            "org_email": agency.agency_email,
            "org_phone": agency.agency_phone,
            "ira_registration_number": agency.ira_registration_number,
            "ira_license_number": agency.ira_licence_number,
            "org_kra_pin": agency.kra_pin,
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
        return cls.query.filter_by(contact_person=user_id).first()

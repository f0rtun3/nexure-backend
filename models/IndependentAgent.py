from app import db


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
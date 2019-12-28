from flask import current_app as app
from database.db import db
from helpers.file_handler import S3FileHandler

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
    website = db.Column(db.String(150))
    mpesa_paybill = db.Column(db.BIGINT, nullable=True)

    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    avatar_url = db.Column(db.String(150), unique=True)
    br_customer = db.relationship("BRCustomer", backref="br_affiliation")
    br_staff = db.relationship("BRStaff", backref="broker")

    def __init__(self, broker_name, broker_phone_number, broker_email, contact_person, ira_registration_number=None,
                 ira_license_number=None, kra_pin=None, website=None, facebook=None, instagram=None, twitter=None,
                 avatar_url=None, mpesa_paybill=None):
        self.broker_name = broker_name
        self.broker_phone_number = broker_phone_number
        self.broker_email = broker_email
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

    def __repr__(self):
        return f"{self.broker_id}"

    def serialize(self):
        avatar_url = ""
        if self.avatar_url is not None:
            s3_handler = S3FileHandler(app.config['S3_BUCKET'], self.avatar_url)
            avatar_url = s3_handler.generate_pre_signed_url()
        org_details = {
            "organization": {
                "broker_id": self.broker_id,
                "org_name": self.broker_name,
                "org_contact": self.contact_person,
                "org_phone": self.broker_phone_number,
                "org_email": self.broker_email,
                "ira_registration_number": self.ira_registration_number,
                "ira_license_number": self.ira_license_number,
                "org_kra_pin": self.kra_pin,
                "avatar_url": avatar_url,
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
    def get_all_brokers(cls):
        broker_rows = cls.query.all()
        brokers = [{
            "org_name": broker.broker_name,
            "org_contact": broker.contact_person,
            "org_phone": broker.broker_phone_number,
            "org_email": broker.broker_email,
            "ira_registration_number": broker.ira_registration_number,
            "ira_license_number": broker.ira_license_number,
            "org_kra": broker.kra_pin,
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
        brokerage = cls.query.filter_by(contact_person=user_id).first()
        return brokerage

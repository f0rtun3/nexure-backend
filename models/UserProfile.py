from flask import current_app as app
from database.db import db
from datetime import datetime
from sqlalchemy import or_
from helpers.file_handler import S3FileHandler

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
    phone_2 = db.Column(db.BIGINT, unique=True)
    email_2 = db.Column(db.String(100), unique=True)
    avatar_url = db.Column(db.String(150), unique=True)
    occupation = db.Column(db.String(100))
    id_passport = db.Column(db.String(30), unique=True)
    kra_pin = db.Column(db.String(15), unique=True)
    birth_date = db.Column(db.Date)
    physical_address = db.Column(db.String(100))
    postal_address = db.Column(db.String(100))
    postal_code = db.Column(db.Integer)
    postal_town = db.Column(db.String(30))
    country = db.Column(db.String(3))
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
                 id_passport=None, kra_pin=None, birth_date=None, physical_address=None, postal_address=None,
                 postal_code=None, postal_town=None, country=None, county=None, constituency=None, ward=None,
                 facebook=None,
                 twitter=None, instagram=None, phone_2=None, email_2=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.gender = gender
        self.avatar_url = avatar_url
        self.occupation = occupation
        self.id_passport = id_passport
        self.kra_pin = kra_pin
        self.birth_date = self.convert_date(birth_date)
        self.physical_address = physical_address
        self.postal_address = postal_address
        self.postal_code = postal_code
        self.postal_town = postal_town
        self.country = country
        self.county = county
        self.constituency = constituency
        self.ward = ward
        self.facebook = facebook
        self.twitter = twitter
        self.instagram = instagram
        self.phone_2 = phone_2
        self.email_2 = email_2

    def __repr__(self):
        return f"{self.id_passport}"

    def serialize(self):
        avatar_url = ""
        if self.avatar_url is not None:
            s3_handler = S3FileHandler(app.config['S3_BUCKET'], self.avatar_url)
            avatar_url = s3_handler.generate_pre_signed_url()
        return {
            "profile_details": {
                "user_id": self.user_id,
                "email": self.user.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "gender": self.gender,
                "phone": self.phone,
                "phone_2": self.phone_2,
                "email_2": self.email_2,
                "avatar_url": avatar_url,
                "occupation": self.occupation,
                "id_passport": self.id_passport,
                "kra_pin": self.kra_pin,
                "birth_date": self.birth_date,
                "physical_address": self.physical_address,
                "postal_address": self.postal_address,
                "postal_code": self.postal_code,
                "postal_town": self.postal_town,
                "country": self.country,
                "county": self.county,
                "constituency": self.constituency,
                "ward": self.ward,
                "created_on": self.created_on.strftime('%m/%d/%Y'),
                "updated_on": self.updated_on.strftime('%m/%d/%Y')
            },
            "social_media": {
                "facebook": self.facebook,
                "twitter": self.twitter,
                "instagram": self.instagram
            }
        }

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

    def convert_date(self, date=None):
        """birthdate should be in accepted format"""
        if date is not None:
            format_str = '%d/%m/%Y'
            converted_date = datetime.strptime(date, format_str)
            return converted_date.date()

    @classmethod
    def get_profile_by_phone_number(cls, phone):
        profile = cls.query.filter_by(phone=phone).first()
        return profile

    @classmethod
    def check_account_duplicate(cls, user_phone, user_id_passport, user_kra_pin):
        return cls.query.filter(or_(cls.phone == user_phone, cls.id_passport == user_id_passport,
                                    cls.kra_pin == user_kra_pin)).first()

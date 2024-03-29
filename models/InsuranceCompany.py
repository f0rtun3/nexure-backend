from database.db import db


class InsuranceCompany(db.Model):
    __tablename__ = "insurance_company"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    contact_person = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'))
    company_phone = db.Column(db.BIGINT, unique=True, nullable=True)
    ira_registration_number = db.Column(db.String(50), unique=True)
    ira_license_number = db.Column(db.String(50), unique=True)
    kra_pin = db.Column(db.String(50), unique=True)
    website = db.Column(db.String(150), unique=True)
    bank_account = db.Column(db.String(50), unique=True)
    mpesa_paybill = db.Column(db.String(50), unique=True)
    associated_company = db.Column(db.Integer, db.ForeignKey(
        'company_details.id', ondelete='CASCADE', onupdate='CASCADE'))
    rate = db.Column(db.Float, nullable=True)
    ncd_rate = db.Column(db.Float, nullable=True)
    year = db.Column(db.Float, nullable=True)
    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))
    master_policy = db.relationship(
        "MasterPolicy", backref="insurance_company", lazy='dynamic')
    ic_benefit = db.relationship(
        'ICBenefits', backref="insurance_company", lazy='dynamic')
    ic_extension = db.relationship(
        'ICExtensions', backref="insurance_company", lazy='dynamic')
    child_policy = db.relationship(
        'ChildPolicy', backref="insurance_company", lazy='dynamic')
    ic_loadings = db.relationship(
        'ICLoadings', backref='insurance_company', lazy='dynamic')

    def __init__(self, contact_person, associated_company, company_phone=None, ira_registration_number=None,
                 ira_licence_number=None, kra_pin=None, website=None, facebook=None, instagram=None, twitter=None,
                 mpesa_paybill=None, rate=None, ncd_rate=None):
        self.company_phone = company_phone
        self.contact_person = contact_person
        self.ira_registration_number = ira_registration_number
        self.ira_license_number = ira_licence_number
        self.kra_pin = kra_pin
        self.website = website
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter
        self.mpesa_paybill = mpesa_paybill
        self.associated_company = associated_company
        self.rate = rate
        self.ncd_rate = ncd_rate

    def __repr__(self):
        return f"{self.id}"

    def serialize(self):
        org_details = {
            "organization": {
                "id": self.id,
                "org_name": self.company_details.company_name,
                "org_email": self.company_details.company_email,
                "org_kra_pin": self.kra_pin,
                "org_phone": self.company_phone,
                "bank_account": self.bank_account,
                "mpesa_paybill": self.mpesa_paybill,
                "ira_registration_number": self.ira_registration_number,
                "ira_license_number": self.ira_license_number,
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
    def get_company_by_id(cls, insurance_company_id):
        company = cls.query.filter_by(id=insurance_company_id).first()
        return company

    @classmethod
    def get_company_by_contact_person(cls, user_id):
        company = cls.query.filter_by(contact_person=user_id).first()
        return company

    @classmethod
    def get_all_companies(cls):
        companies = [company.serialize() for company in cls.query.all()]
        return companies

    @classmethod
    def get_by_associated_company(cls, assoc_id):
        company = cls.query.filter_by(associated_company=assoc_id).first()
        return company

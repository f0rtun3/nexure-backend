from app import db


class InsuranceCompany(db.Model):
    __tablename__ = "insurance_company"
    id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    contact_person = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'))
    company_phone = db.Column(db.BIGINT, unique=True, nullable=False)
    ira_registration_number = db.Column(db.String(15), unique=True)
    ira_license_number = db.Column(db.String(15), unique=True)
    kra_pin = db.Column(db.String(15), unique=True)
    website = db.Column(db.String(150), unique=True)
    bank_account = db.Column(db.BIGINT, nullable=True)
    mpesa_paybill = db.Column(db.BIGINT, nullable=True, unique=True)
    company_details = db.Column(db.Integer, db.ForeignKey(
        'company_details.id', ondelete='CASCADE', onupdate='CASCADE'))
    rate = db.Column(db.Float, nullable=False)

    # social media handles
    facebook = db.Column(db.String(150))
    instagram = db.Column(db.String(150))
    twitter = db.Column(db.String(150))

    def __init__(self, company_phone, contact_person, company_details, ira_registration_number=None,
                 ira_licence_number=None, kra_pin=None, website=None, facebook=None, instagram=None, twitter=None,
                 mpesa_paybill=None, rate=None):

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
        self.company_details = company_details
        self.rate = rate

    def __repr__(self):
        return f"{self.company_details}"

    def serialize(self):
        return{
            "contact_person": self.contact_person,
            "company_number": self.company_phone,
            "bank_account": self.bank_account,
            "mpesa_paybill": self.mpesa_paybill,
            "ira_registration_number": self.ira_registration_number,
            "ira_license_number": self.ira_license_number,
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
    def get_company_by_id(cls, insurance_company_id):
        return cls.query.filter_by(insurance_company_id=insurance_company_id).first()

    @classmethod
    def get_company_by_contact_person(cls, user_id):
        company = cls.filter_by(contact_person=user_id).first()
        return company

    @classmethod
    def get_all_companies(cls):
        company_rows = cls.query.all()
        companies = [{
            "contact_person": company.contact_person,
            "company_number": company.company_phone,
            "ira_registration_number": company.ira_registration_number,
            "ira_license_number": company.ira_license_number,
            "kra_pin": company.kra_pin,
            "website": company.website,
            "facebook": company.facebook,
            "instagram": company.instagram,
            "twitter": company.twitter
        } for company in company_rows]

        return companies

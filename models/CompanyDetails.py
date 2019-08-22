from app import db


class CompanyDetails(db.Model):
    """Store info about the insurance company, to be associated at login"""
    __tablename__ = "company_details"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_name = db.Column(db.String(100), unique=True, nullable=False)
    company_email = db.Column(db.String(100), nullable=False, unique=True)
    physical_address = db.Column(db.String(300))
    website = db.Column(db.String(150))
    avatar = db.Column(db.String(50), nullable=True)
    # company = db.relationship("InsuranceCompany", backref="insurance_company")

    def __init__(self, company_name, company_email, physical_address, website, avatar=None):
        self.company_name = company_name
        self.company_email = company_email
        self.physical_address = physical_address
        self.website = website
        self.avatar = avatar

    def __repr__(self):
        return f"{self.company_name}"

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

    def get_companies(self):
        return self.query.all()

    @classmethod
    def get_company_by_id(cls, id):
        company = cls.query.filter_by(id=id).first()
        return company

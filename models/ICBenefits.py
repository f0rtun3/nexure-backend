from database.db import db


class ICBenefits(db.Model):
    __tablename__ = 'ic_benefit'

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    insurance_company_id = db.Column(db.Integer, db.ForeignKey(
        'insurance_company.id', onupdate='CASCADE', ondelete='CASCADE'))
    benefit_id = db.Column(db.Integer, db.ForeignKey(
        'benefit.id', onupdate='CASCADE', ondelete='CASCADE'))
    # links to the association table for benefits
    policy_benefit = db.relationship('PolicyBenefits', backref="ic_benefit")
    free_limit = db.Column(db.Float, nullable=False)
    max_limit = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)

    def __init__(self, insurance_company, benefit_id, free_limit, max_limit, rate):
        self.insurance_company = insurance_company
        self.benefit = benefit_id
        self.get_benefit_id = benefit_id
        self.free_limit = free_limit
        self.max_limit = max_limit
        self.rate = rate

    def serialize(self):
        return {
            "insurance_company": self.insurance_company.company_details.company_name,
            "name": self.benefit.name,
            "free_limit": self.free_limit,
            "max_limit": self.max_limit,
            "rate": self.rate
        }

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
    def get_benefits_by_company_id(cls, company_id):
        """
        Returns id, benefit_id, free_limit, max_limit and rate for
        every list of benefits under a particular company 
        """
        benefit_rows = cls.query.filter_by(insurance_company=company_id).all()
        return benefit_rows

    @classmethod
    def get_ic_benefit(cls, benefit_id):
        benefit = cls.query.filter_by(benefit=benefit_id).first()
        return benefit

    @classmethod
    def get_benefit_id(cls, id):
        """
        Gets the IC benefit given the object id
        """
        ic_benefit = cls.query.filter_by(id=id).first()
        return ic_benefit

    @classmethod
    def get_unselected_benefits(cls, excluded_benefits):
        """
        get the unselected benefits of a customer
        """
        benefits = cls.query.filter(cls.id.notin_(excluded_benefits))
        return [benefit.serialize() for benefit in benefits]

from app import db


class ICBenefits(db.Model):
    __tablename__ = 'ic_benefit'

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    insurance_company = db.Column(db.Integer, db.ForeignKey(
        'insurance_company.id', onupdate='CASCADE', ondelete='CASCADE'))
    benefit = db.Column(db.Integer, db.ForeignKey(
        'benefit.id', onupdate='CASCADE', ondelete='CASCADE'))
    # links to the association table for benefits
    policy_benefit = db.relationship('ChildPolicy', secondary='policy_benefits',
                                     lazy='dynamic', backref=db.backref('allbenefits', lazy='dynamic'))
    free_limit = db.Column(db.Float, nullable=False)
    max_limit = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)

    def __init__(self, insurance_company, benefit, free_limit, max_limit, rate):
        self.insurance_company = insurance_company
        self.benefit = benefit
        self.free_limit = free_limit
        self.max_limit = max_limit
        self.rate = rate

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

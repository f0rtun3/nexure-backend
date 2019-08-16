from app import db

class ICBenefits(db.Model):
    __tablename__ = 'ic_benefit'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    insurance_company = db.Column(db.Integer, db.ForeignKey('insurance_company.company_id', onupdate='CASCADE', ondelete='CASCADE'))
    benefit = db.Column(db.Integer, db.ForeignKey(
        'benefit.id', onupdate='CASCADE', ondelete='CASCADE'))
    free_limit = db.Column(db.Float, nullable=False)
    max_limit = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)

    def __init__(self, insurance_company, free_limit, max_limit, rate ):
        self.insurance_company = insurance_company
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
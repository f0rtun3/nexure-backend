from database.db import db


class SumInsuredRates(db.Model):
    """
    Stores sum insured rates, with their band limits and relativity
    """
    id = db.Column(db.Integer, primary_key=True,
                   auto_increment=True, nullable=False)
    lower_limit = db.Column(db.Integer, nullable=False)
    upper_limit = db.Column(db.Integer, nullable=False)
    relativity = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)

    def __init__(self, lower_limit, upper_limit, relativity, rate):
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.relativity = relativity
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
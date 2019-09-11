"""
Insurance rate discount model description
"""
from app import db


class ICRateDiscount(db.Model):
    __tablename__ = 'ic_rate_discount'
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    ic_company_id = db.Column(db.Integer, db.ForeignKey('insurance_company.id', onupdate='CASCADE',
                                                        ondelete='CASCADE'))
    rates = db.Column(db.String(20), nullable=False)

    def __init__(self, ic_company_id, rates):
        self.ic_company_id = ic_company_id
        self.rates = rates

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, val in data.items():
            setattr(self, key, val)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_company_discount(cls, company_id):
        """
        get the company discounted rates in an
        :param company_id:
        :return {List(Integer)}:
        """
        discount_rate_rows = cls.query.filter_by(ic_company_id=company_id).first().rates.split(',')
        return [int(rate) for rate in discount_rate_rows]

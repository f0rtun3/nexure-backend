from app import db

class ICProducts(db.Model):
    """
    Stores the company and the products it sells
    """

    __tablename__ = 'ic_products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    company = db.Column(db.Integer, db.ForeignKey('insurance_company.id', onupdate='CASCADE', ondelete='CASCADE'))
    insurance_class = db.Column(db.Integer, db.ForeignKey('insurance_class.class_id', onupdate='CASCADE', ondelete='CASCADE'))
    sub_class = db.Column(db.Integer, db.ForeignKey('insurance_subclass.class_code', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, company, insurance_class, sub_class):
        self.company = company
        self.insurance_class = insurance_class
        self.sub_class = sub_class
    
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
    def get_products_by_company(cls, company_id):
        products = cls.query.filter_by(company=company_id).all()
        return products
from app import db

class ICLoadings(db.Model):
    """Stores the loadings offered by a company, for a particular policy, together with the rate"""

    __tablename__ = 'ic_loadings'

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    insurance_company = db.Column(db.Integer, db.ForeignKey(
        'insurance_company.id', onupdate='CASCADE', ondelete='CASCADE'))
    loading = db.Column(db.Integer, db.ForeignKey(
        'loading.id', onupdate='CASCADE', ondelete='CASCADE'))
    rate = db.Column(db.Float, nullable=False)

    def __init__(self, insurance_company, loading, rate):
        self.insurance_company = insurance_company
        self.loading = loading
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
    def get_loadings_by_company_id(cls, company_id):
        """
        Returns id, loading_id and rate for
        every list of loadings under a particular company 
        """
        loading_rows = cls.query.filter_by(insurance_company=company_id).all()
        return loading_rows

    
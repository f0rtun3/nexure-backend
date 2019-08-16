from app import db


class ICExtensions(db.Model):
    """Stores the extensions that offered by a company, for a particular policy, together with the rate and limits for them"""

    __tablename__ = 'ic_extension'

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    insurance_company = db.Column(db.Integer, db.ForeignKey(
        'insurance_company.company_id', onupdate='CASCADE', ondelete='CASCADE'))
    extension = db.Column(db.Integer, db.ForeignKey(
        'extension.id', onupdate='CASCADE', ondelete='CASCADE'))
    free_limit = db.Column(db.Float, nullable=False)
    max_limit = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)

    def __init__(self, insurance_company, extension, free_limit, max_limit, rate):
        self.insurance_company = insurance_company
        self.extension = extension
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

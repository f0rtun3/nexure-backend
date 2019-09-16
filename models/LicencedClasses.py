from database.db import db


class LicencedClasses(db.Model):
    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    company = db.Column(db.Integer, db.ForeignKey(
        'company_details.id', onupdate='CASCADE', ondelete='CASCADE'))
    insurance_class = db.Column(db.Integer, db.ForeignKey(
        'insurance_class.class_id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, company, insurance_class):
        self.company = company
        self.insurance_class = insurance_class

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
    def get_company_classes(cls, company_id):
        classes = cls.query.filter_by(company=company_id).all()
        class_list = [i.insurance_class for i in classes]
        return class_list

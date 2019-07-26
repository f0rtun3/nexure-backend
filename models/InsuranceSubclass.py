from app import db

class InsuranceSubclass(db.Model):
    __tablename__ = 'insurance_subclass'

    class_code = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    parent_class = db.Column(db.Integer, db.ForeignKey('insurance_class.class_id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, name, class_code, parent_class):
        self.name = name
        self.class_code = class_code
        self.parent_class = parent_class

    def save(self):
        db.session.add(self)
        db.session.commit()

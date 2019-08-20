from app import db

class InsuranceSubclass(db.Model):
    __tablename__ = 'insurance_subclass'

    class_code = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    parent_class = db.Column(db.Integer, db.ForeignKey('insurance_class.class_id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, class_code, name, parent_class):
        self.name = name
        self.class_code = class_code
        self.parent_class = parent_class

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_class_by_name(cls, name):
        subclass = cls.query.filter_by(name=name).first()
        return subclass

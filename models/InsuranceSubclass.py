from app import db


class InsuranceSubclass(db.Model):
    __tablename__ = 'insurance_subclass'

    class_code = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    parent_class = db.Column(db.Integer, db.ForeignKey(
        'insurance_class.class_id', ondelete='CASCADE', onupdate='CASCADE'))
    acronym = db.Column(db.String(50), nullable=True)

    def __init__(self, class_code, name, parent_class, acronym):
        self.name = name
        self.class_code = class_code
        self.parent_class = parent_class
        self.acronym = acronym

    def save(self):
        db.session.add(self)
        db.session.commit()    

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    @classmethod
    def get_class_by_id(cls, code):
        subclass = cls.query.filter_by(class_code=code).first()
        return subclass

    @classmethod
    def get_acronym(cls, id):
        subclass = cls.query.filter_by(class_code=id).first()
        return subclass.acronym

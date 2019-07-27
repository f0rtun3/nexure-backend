from app import db
    
class InsuranceClass(db.Model):
    """
    Insurance class
    """
    __tablename__ = 'insurance_class'

    class_id = db.Column(db.Integer, primary_key=True, nullable=False)
    class_name = db.Column(db.String(50), unique=True, nullable=False)
    acronym = db.Column(db.String(3), unique=True, nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    subclass = db.relationship("InsuranceSubclass", backref="subclass")

    def __init__(self, class_id, class_name, acronym, sector):
        self.class_id = class_id
        self.class_name = class_name
        self.acronym = acronym
        self.sector = sector

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_class_by_name(cls, name):
        parent_class = cls.query.filter_by(class_name=name).first()
        return parent_class.class_id
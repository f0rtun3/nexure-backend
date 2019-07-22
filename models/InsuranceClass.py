from app import db
    
class InsuranceClass(db.Model):
    """
    Insurance class
    """
    __tablename__ = 'insurance_class'

    serial_number = db.Column(db.Integer, primary_key=True, nullable=False)
    class_name = db.Column(db.String(50), unique=True, nullable=False)
    acronym = db.Column(db.String(3), unique=True, nullable=False)
    sector = db.Column(db.String(100), unique=True, nullable=False)
    subclass = db.relationship("InsuranceSubclass", backref="subclass")

    def __init__(self, serial_number, class_name, acronym, sector):
        self.serial_number = serial_number
        self.class_name = class_name
        self.acronym = acronym
        self.sector = sector

    def save(self):
        db.session.add(self)
        db.session.commit()

class InsuranceSubclass(db.Model):
    __tablename__ = 'insurance_subclass'

    class_code = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    parent_class = db.Column(db.Integer, db.ForeignKey('insurance_class.serial_number', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, name, class_code, parent_class):
        self.name = name
        self.class_code = class_code
        self.parent_class = parent_class

    def save(self):
        db.session.add(self)
        db.session.commit()
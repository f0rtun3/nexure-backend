from app import db

class Benefits(db.Model):
    __tablename__ = 'benefit'
    "A list of benefits to be added by insurance companies for various policies"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100))
    class_code = db.Column(db.Integer, db.ForeignKey('insurance_class.class_id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, name, class_code):
        self.name = name
        self.class_code = class_code
    
    def __repr__(self):
        return f"{self.name}"
    
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
from app import db


class Benefit(db.Model):
    __tablename__ = 'benefit'
    "A list of benefits to be added by insurance companies for various policies"
    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    name = db.Column(db.String(100))
    # class_code = db.Column(db.Integer, db.ForeignKey('insurance_class.class_id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, name):
        self.name = name
        # self.class_code = class_code

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

    @classmethod
    def get_benefit_by_name(cls, benefit_name):
        benefit = cls.query.filter_by(name=benefit_name).first()
        return benefit.id
    
    @classmethod
    def get_name_by_id(cls, benefit_id):
        benefit = cls.query.filter_by(id=benefit_id).first()
        return benefit.name
        
    @classmethod
    def get_all_benefits(cls):
        benefit_rows = cls.query.all()
        benefits = []
        for i in benefit_rows:
            benefits.append(i.name)
        return benefits


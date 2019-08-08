from app import db

class Constituency(db.Model):
    __tablename__ = 'constituency'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    county = db.Column(db.Integer, db.ForeignKey('county.id', ondelete='CASCADE', onupdate='CASCADE'))
    ward = db.relationship("Ward", backref="constituency_ward")

    def __init__(self, name, county):
        self.name = name
        self.county = county
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_constituency_by_name(cls, name):
        consituency = cls.query.filter_by(name=name).first()
        return consituency.id

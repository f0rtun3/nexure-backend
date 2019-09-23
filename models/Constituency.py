from database.db import db

class Constituency(db.Model):
    __tablename__ = 'constituency'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    county_id = db.Column(db.Integer, db.ForeignKey('county.id', ondelete='CASCADE', onupdate='CASCADE'))
    ward = db.relationship("Ward", backref="constituency")

    def __init__(self, name, county):
        self.name = name
        self.county = county

    def serialize(self):
        return{
            "id": self.id
            "name": self.name,
            "county": self.county.county_name,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_constituency_by_name(cls, name):
        constituency = cls.query.filter_by(name=name).first()
        return constituency.id

    @classmethod
    def get_all_constituencies(cls):
        return [constituency.serialize() for constituency in cls.query.all()]

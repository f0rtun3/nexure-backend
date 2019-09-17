from database.db import db


class County(db.Model):
    __tablename__ = 'county'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    county_name = db.Column(db.String(50), unique=True, nullable=False)
    constituency = db.relationship("Constituency", backref="county_constituency")
    ward = db.relationship("Ward", backref="county_ward")

    def __init__(self, county_name):
        self.county_name = county_name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.county_name,
            "constituencies": [constituency.serialize() for
                             constituency in self.constituency]
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_county_by_name(cls, name):
        county = cls.query.filter_by(county_name=name).first()
        return county.id

    @classmethod
    def get_county_by_id(cls, id):
        county = cls.query.filter_by(id=id).first()
        return county
    
    @classmethod
    def get_all_counties(cls):
        counties = [c.serialize() for c in cls.query.all()]
        return counties

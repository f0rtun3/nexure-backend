from app import db
  
class County(db.Model):
    __tablename__ = 'county'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    county_name = db.Column(db.String(50), unique=True, nullable=False)
    constituency = db.relationship("Constituency", backref="county_constituency")
    ward = db.relationship("Ward", backref="county_ward")

    def __init__(self, county_name):
        self.county_name = county_name

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_county_by_name(cls, name):
        county = cls.query.filter_by(county_name=name).first()
        return county.id
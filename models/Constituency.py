from app import db
  
class Constituency(db.Model):
    __tablename__ = 'constituency'

    id = db.Column(db.Integer, primary_key=True, auto_increment=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    county = db.Column(db.Integer, db.ForeignKey('county.id', ondelete='CASCADE', onupdate='CASCADE'))
    ward = db.relationship("Ward", backref="ward")

    def __init__(self, name, county):
        self.name = name
        self.county = county
    
    def save(self):
        db.session.add(self)
        db.session.commit()

from app import db

class Ward(db.Model):
    __tablename__ = 'ward'

    id = db.Column(db.Integer, primary_key=True, auto_increment=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    constituency = db.Column(db.Integer, db.ForeignKey('constituency.id', ondelete='CASCADE', onupdate='CASCADE'))
    county = db.Column(db.Integer, db.ForeignKey('county.id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, name, constituency, county):
        self.name = name
        self.constituency = constituency
        self.county = county
    
    def save(self):
        db.session.add(self)
        db.session.commit()
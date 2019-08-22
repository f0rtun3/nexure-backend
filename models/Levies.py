from app import db

class Levies(db.Model):
    __tablename__ = 'levies'

    """Contains levies for a particular child policy"""
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100))
    rate = db.Column(db.Float, nullable=False)

    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
    
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
    def get_all_levies(cls):
        levies = cls.query.all
        return levies

    
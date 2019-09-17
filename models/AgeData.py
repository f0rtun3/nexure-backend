from database.db import db


class AgeData(db.Model):
    """
    Stores age bands, their data and the relativity.
    """
    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    data = db.Column(db.Integer, nullable=False)
    lower_limit = db.Column(db.Integer, nullable=False)
    upper_limit = db.Column(db.Integer, nullable=False)
    relativity = db.Column(db.Float, nullable=False)

    def __init__(self, data, lower_limit, upper_limit, relativity):
        self.data = data
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.relativity = relativity
    
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
